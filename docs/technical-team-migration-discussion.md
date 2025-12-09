# Technical Team Discussion: Stack Migration Planning

**Date:** December 11, 2024  
**Duration:** ~20 minutes  
**Participants:**
- **Mike Chen** — Technical Lead, Platform Engineering
- **Priya Sharma** — Senior Backend Developer
- **Jordan Brooks** — Full-Stack Developer  
- **Alex Kim** — DevOps Engineer

---

## Meeting Transcript

**[00:00]**

**Mike:** Alright, thanks everyone for coming in. I know it's been a crazy week, but we need to have this conversation about Yugastore. As you probably heard through the grapevine, there's a new directive from architecture governance.

**Priya:** The Python thing?

**Mike:** *sighs* Yeah. The Python thing. Starting Q1, all new development and major refactors need to align with the "unified stack"—React frontends, Python backends. FastAPI specifically.

**Jordan:** Wait, we're throwing out the entire Spring Boot stack? That's like... six microservices.

**Mike:** Look, I'm not thrilled about it either. This is a solid Java codebase. Spring Boot, Eureka for service discovery, Feign clients—it works. But the mandate came from above my pay grade, and honestly, my job security depends on us executing this.

**[01:30]**

**Alex:** What's the rationale? Did they actually give one?

**Mike:** *reading from notes* "Reduce technology fragmentation across the organization, standardize on a single backend language to improve hiring efficiency, leverage Python's ecosystem for future AI/ML integration." That's the official line.

**Priya:** I mean... the AI/ML thing isn't nothing. But we have a working system here. The products service handles 6,000 SKUs without breaking a sweat.

**Mike:** I know. And for what it's worth, I pushed back. Hard. But the decision's been made. So let's focus on how we do this without breaking everything and losing our minds.

**[02:45]**

**Jordan:** Can we at least keep the frontend? The React UI is already React.

**Mike:** That's actually one bright spot. The frontend is React, so we're already aligned there. Although...

**Jordan:** Although what?

**Mike:** Have you looked at that code recently? Class components everywhere, `componentWillReceiveProps`, inline CSS files scattered across forty directories. Sarah from Digital Experience wants a complete visual refresh anyway. We might as well modernize the React code while we're at it.

**Priya:** So we're rebuilding everything.

**Mike:** *pauses* Yes. Essentially, yes. But we can be smart about it. Let's map out what we have and figure out a migration path.

**[04:00]**

**Mike:** Alex, can you pull up the architecture diagram? Let's walk through the services.

**Alex:** *shares screen* Okay, so we've got six Spring Boot services. Eureka server for discovery, API gateway, products, cart, checkout, and login.

**Mike:** Right. Let's start with products. Priya, you know that service best.

**Priya:** So it's a pretty standard Spring Boot setup. `ProductCatalogController` handles three main endpoints—get a single product by ASIN, list all products with pagination, and list products by category with pagination. Uses JPA repositories under the hood.

**Mike:** And the data model?

**Priya:** `ProductMetadata` is the main entity. Has the product ID, title, description, price, image URL, categories, review stats—num_reviews, num_stars, avg_stars—and then all these recommendation fields like `also_bought`, `also_viewed`, `bought_together`. Those are stored as element collections.

**[05:30]**

**Jordan:** Element collections... that's going to be interesting to migrate. Those become separate tables in JPA, right?

**Priya:** Yeah, there's a `productmetadata_also_bought` table, `productmetadata_categories`, all that. We'll need to think about how to model that in Python. SQLAlchemy can do it but it's different.

**Mike:** We could simplify and just store those as JSON arrays. Postgres handles that well, and it's probably cleaner than junction tables for this use case.

**Priya:** That's... actually not a bad idea. Simplify the schema while we migrate.

**[06:30]**

**Mike:** What about the ranking service?

**Priya:** `ProductRankingService` is used for the bestsellers by category. There's a `ProductRanking` entity with a composite key—category and sales rank. The category page uses this to pull top products ordered by rank.

**Alex:** That's hitting YCQL right now, yeah? The Cassandra API?

**Priya:** Yeah, the products service is a weird hybrid. Metadata is in YSQL via JPA, but rankings were originally YCQL. Honestly, we should consolidate that anyway.

**Mike:** Good. Add that to the list—unify on YSQL. PostgreSQL dialect. FastAPI with SQLAlchemy or SQLModel.

**[07:45]**

**Mike:** Jordan, walk us through the cart service.

**Jordan:** Sure. `ShoppingCartController` has four endpoints: add product, get products in cart, remove product, clear cart. The service layer is `ShoppingCartImpl`, and there's this weird pattern where it's session-scoped with a proxy mode.

**Mike:** Oh god, the session-scoped beans.

**Jordan:** Yeah. It's using WebApplicationContext.SCOPE_SESSION. Which I guess made sense when this was maybe a monolith? But in a microservices world it's... questionable.

**Priya:** Does it even work right now? With multiple instances behind a load balancer?

**Jordan:** Honestly? I'm not sure. There's no sticky session configuration that I can see.

**[09:00]**

**Mike:** Okay, so the cart service needs rethinking anyway. In the Python version, we should just make it stateless. User ID comes in on every request, cart state lives in the database, done.

**Jordan:** The `ShoppingCart` entity is actually pretty simple. Cart key, user ID, ASIN, quantity, timestamp. Primary storage is PostgreSQL via JPA.

**Mike:** Great. That's an easy port. SQLModel, FastAPI, maybe an hour of work for the basic CRUD.

**Jordan:** The repository has some custom queries though—`updateQuantityForShoppingCart`, `decrementQuantityForShoppingCart`, `findProductsInCartByUserId`. Those are @Query annotations with native SQL.

**Mike:** We'll write those as raw SQL or SQLAlchemy queries. Not a blocker.

**[10:30]**

**Mike:** Now the fun one. Checkout.

**Priya:** *groans* The checkout service.

**Mike:** Yeah. Talk us through it.

**Priya:** `CheckoutServiceImpl` is where the magic happens. It's transactional, session-scoped—same pattern as cart. On checkout, it:
1. Calls the cart service via REST to get products in cart
2. Iterates through each product
3. Checks inventory via `ProductInventoryRepository`
4. Gets product details via REST from the product catalog
5. Builds up a CQL transaction statement—BEGIN TRANSACTION, UPDATE inventory, INSERT order, END TRANSACTION
6. Executes the whole thing as raw CQL
7. Clears the cart

**Jordan:** Wait, it's building SQL strings with concatenation?

**Priya:** CQL strings, but yes.

**Mike:** *rubbing temples* Let me guess—no parameterized queries?

**Priya:** `"UPDATE product_inventory SET quantity = quantity - " + entry.getValue() + " where asin = '" + entry.getKey() + "'"`. Direct string interpolation.

**[12:00]**

**Alex:** That's... that's not great from a security standpoint.

**Mike:** Add it to the list of things we fix during migration. The Python version will use proper parameterized queries. This is non-negotiable.

**Priya:** The other issue is the REST calls. It's using Feign clients to call other services. `ShoppingCartRestClient`, `ProductCatalogRestClient`. In Python we'll need something equivalent.

**Mike:** HTTPX for async HTTP calls. FastAPI is async-native, so we lean into that.

**Jordan:** What about service discovery? We're using Eureka right now.

**Alex:** Do we need Eureka in the Python world? We could just use environment variables for service URLs when running in Docker or Kubernetes. Service mesh handles the rest.

**[13:15]**

**Mike:** That's a good point. Let's simplify. For local dev and Docker Compose, environment variables. For production on Kubernetes, we let the service mesh handle discovery. Drop Eureka entirely.

**Alex:** That actually makes the deployment story cleaner.

**Priya:** One less thing to maintain.

**Mike:** Exactly. Okay, what about the order creation? That hardcoded user_id...

**Priya:** Oh yeah. `order.setUser_id(1)`. It's just hardcoded to 1. The `userId` parameter comes in as "u1001" but the order always saves with user_id 1.

**Jordan:** How is that even... how has nobody noticed this?

**Mike:** Because nobody's looking at order history. The frontend doesn't have that feature. It just says "Order #xyz received" and moves on.

**[14:30]**

**Jordan:** So every order in the database looks like it came from the same user.

**Mike:** Yep. The Python version will fix that. Proper user authentication, user ID flows through from the auth token to the order record.

**Priya:** Speaking of auth—the login service.

**Mike:** Right. What's the situation there?

**Jordan:** It's Spring Security with `WebSecurityConfigurerAdapter`. BCrypt for password hashing, which is good. Form-based login, session-based auth. The `User` entity has username, password, passwordConfirm as transient, and a many-to-many with `Role`.

**Mike:** So basic role-based access. No JWT, no OAuth.

**Jordan:** Nope. Old school sessions.

**[15:45]**

**Mike:** For the Python version, let's do JWT. FastAPI has great JWT support. We can add OAuth later for social login, but for now, JWT with proper token refresh.

**Priya:** Are we keeping the same database schema for users?

**Mike:** We can. BCrypt hashes are BCrypt hashes. We'd just need to verify the password the same way. Existing users could log in without resetting passwords.

**Jordan:** That's actually smooth. I was worried about a password migration nightmare.

**[16:30]**

**Mike:** Alright, let's talk about the API gateway.

**Alex:** That's a beefy one. `YugastoreApiGateway` has Feign clients for all the downstream services—products, cart, checkout. It basically proxies everything.

**Mike:** In Python, we have options. We could use FastAPI as a gateway with HTTPX calls to downstream services, or we could go with something like Kong or Traefik and have the frontend call services directly through it.

**Priya:** I'd vote for keeping the gateway pattern but making it thinner. Just routing, maybe some request transformation, auth validation. No business logic.

**Mike:** Agreed. The Java gateway has duplicate domain classes—`ProductMetadata`, `Order`, etc.—that mirror the ones in the downstream services. That's a maintenance headache. Python gateway should just pass through JSON.

**[17:45]**

**Alex:** What about the frontend build? The current setup has Maven building the React app and bundling it into a JAR.

**Mike:** Yeah, the `frontend-maven-plugin` thing. We'll decouple that. Next.js or Vite for the frontend, containerized separately. API gateway is its own container. Clean separation.

**Jordan:** Next.js would give us server-side rendering. Could help with SEO for product pages.

**Mike:** Good point. Let's go Next.js. Modern React, server components, app router. Kill the class components, use hooks.

**Priya:** And Tailwind for styling instead of those scattered CSS files?

**Mike:** Absolutely. Tailwind, shadcn/ui for components. Modern stack.

**[18:45]**

**Mike:** Alright, let me summarize what we're looking at:

**Backend Migration:**
- Products service: Spring Boot → FastAPI + SQLModel
- Cart service: Spring Boot → FastAPI + SQLModel, drop session-scoped pattern
- Checkout service: Spring Boot + raw CQL → FastAPI + SQLAlchemy with proper transactions
- Login service: Spring Security → FastAPI with JWT auth
- API Gateway: Spring Cloud Gateway → FastAPI or lightweight reverse proxy
- Kill Eureka, use env vars + Kubernetes service discovery

**Frontend Migration:**
- React class components → Next.js with React hooks
- Scattered CSS → Tailwind CSS
- Old libraries → shadcn/ui component library

**Security Fixes:**
- Fix hardcoded user IDs
- Parameterized queries everywhere
- Proper JWT authentication flow
- Add CSRF protection back

**[19:45]**

**Priya:** That's a lot.

**Mike:** It is. But here's the thing—we're not doing this overnight. We can run both stacks in parallel. Start with products service since it's the simplest. Get that working in Python, deploy it alongside the Java version, route traffic gradually.

**Jordan:** Strangler fig pattern.

**Mike:** Exactly. We strangle the old system one service at a time. Cart next, then checkout—that's the hardest—then login, then we can shut down the Java services.

**Alex:** What's the timeline looking like?

**Mike:** Sarah wants something impressive by Q2 for a board presentation. So we need at least the frontend refresh and the security fixes done by then. The full backend migration... maybe end of Q2, early Q3 realistically.

**[20:30]**

**Priya:** I still think this is a lot of risk for questionable benefit. The Java code works.

**Mike:** *sighs* I know. Believe me, I know. If it were up to me, we'd clean up the security issues, modernize the frontend, and call it a day. But it's not up to me. The org has decided Python is the future, and we either get on the train or get run over by it.

**Jordan:** Well, at least we'll have job security for the next six months.

**Mike:** *laughs darkly* Silver linings, Jordan. Silver linings.

**Alex:** Should we set up a Jira board or something to track all this?

**Mike:** Yeah. Let's break it down into epics—one per service migration, one for frontend, one for infrastructure. We'll groom next week. For now, everyone review the Java code you're going to own. Priya, you've got products and checkout. Jordan, cart and login. Alex, infrastructure and gateway. I'll handle coordination and keep management off your backs as much as I can.

**Priya:** Thanks, Mike. I know this isn't what you wanted either.

**Mike:** It's the job. Alright, we're over time. Let's reconvene Thursday to start breaking down the products service migration. Good work, everyone.

---

## Meeting Summary

### Services to Migrate

| Service | Current Stack | Target Stack | Complexity | Owner |
|---------|--------------|--------------|------------|-------|
| Products | Spring Boot + JPA + YCQL | FastAPI + SQLModel | Medium | Priya |
| Cart | Spring Boot + JPA (session-scoped) | FastAPI + SQLModel (stateless) | Low | Jordan |
| Checkout | Spring Boot + CQL Templates | FastAPI + SQLAlchemy | High | Priya |
| Login | Spring Security + Sessions | FastAPI + JWT | Medium | Jordan |
| API Gateway | Spring Cloud + Feign | FastAPI or lightweight proxy | Medium | Alex |
| Eureka | Spring Cloud Netflix | Remove (use env vars/k8s) | Low | Alex |

### Frontend Migration

| Current | Target |
|---------|--------|
| React class components | Next.js with React hooks |
| componentWillReceiveProps | useEffect, custom hooks |
| Scattered CSS files | Tailwind CSS |
| react-materialize, react-bootstrap | shadcn/ui |
| Maven-built bundle in JAR | Standalone Next.js container |

### Critical Security Fixes

1. **Hardcoded user_id in checkout** — Order.setUser_id(1) always sets to 1
2. **Hardcoded userId in checkout controller** — Always uses "u1001"
3. **SQL/CQL injection risk** — String concatenation in transaction building
4. **No CSRF protection** — Explicitly disabled in SecurityConfiguration
5. **Session management** — Session-scoped beans may not work correctly with load balancing

### Architecture Decisions

- Drop Eureka in favor of environment variables + Kubernetes service mesh
- Unify database on YSQL (PostgreSQL) — eliminate YCQL complexity
- JWT-based authentication instead of session-based
- Async HTTP calls with HTTPX for inter-service communication
- Strangler fig migration pattern — gradual service replacement

### Timeline

- **Q2 Target:** Frontend refresh + security fixes + at least Products service migrated
- **Q2-Q3:** Complete backend migration
- **Parallel deployment** during transition period

