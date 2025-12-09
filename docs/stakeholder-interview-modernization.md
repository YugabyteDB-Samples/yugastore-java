# Stakeholder Interview: Yugastore Modernization Initiative

**Date:** December 9, 2024  
**Duration:** ~20 minutes  
**Participants:**
- **Sarah Mitchell** — VP of Digital Experience, Cronos Retail Group
- **Dev Team Lead** — Technical Lead / Business Analyst

---

## Interview Transcript

**[00:00]**

**Dev Lead:** Hey Sarah, thanks for making time today. I know you've been wanting to chat about the store app for a while now.

**Sarah:** Yeah, absolutely. I've been looking at what our competitors are doing, and honestly, I think we're falling behind. When was the last time we did a real refresh on Yugastore?

**Dev Lead:** The core architecture? That'd be... probably three, four years ago? We've been patching things here and there but nothing major.

**Sarah:** Yeah, that's what I figured. Look, I pulled up the site on my phone the other day to show it to a vendor, and I was kind of embarrassed. The homepage still has that static banner image—it's nice and all, but every other site these days has these beautiful animations, smooth transitions. Ours just feels... I don't know, like an early 2010s website?

**[01:45]**

**Dev Lead:** That's fair feedback. The hero section is literally just a PNG right now. No interactivity at all.

**Sarah:** Right! And the product cards—they work, don't get me wrong—but they're just kind of... there. No hover effects, no subtle animations. When I add something to cart on Amazon or Target, there's this satisfying little animation, you know? It feels modern. Ours just kind of... blinks?

**Dev Lead:** *laughs* Yeah, we have a basic star rating display but it's using an older icon library. The add-to-cart is pretty bare bones too.

**Sarah:** Exactly. And the fonts! I'm not a designer but even I can tell we're just using Roboto everywhere. It's fine, it's readable, but it doesn't have any personality. Some of our competitors have these really distinctive typography choices that make them feel premium.

**[03:30]**

**Dev Lead:** So you're looking for more of a design refresh then? New typography, animations, that sort of thing?

**Sarah:** That's part of it, but here's the thing—I was talking to Marcus in IT security last week, and he mentioned something about our checkout that concerned me. He said something about the system not really knowing who's checking out?

**Dev Lead:** Oh... yeah. I know exactly what he's referring to.

**Sarah:** Can you explain that to me? Because that sounds bad.

**Dev Lead:** So, when the checkout happens, the system is supposed to associate the order with a logged-in user. But right now there's this hardcoded user ID—"u1001"—that gets used for everyone. It was probably a development shortcut that never got fixed.

**[04:45]**

**Sarah:** Wait, so everyone's orders are going to the same fake user?

**Dev Lead:** For the checkout service, yes. The cart itself tracks things separately, but when it comes to actually placing the order, there's no real user identity flowing through. It's a gap.

**Sarah:** Okay, that's... that's definitely something we need to fix. What about the login itself? Is that secure?

**Dev Lead:** The login service uses BCrypt for password hashing, which is good—that's industry standard. But there are some concerns. We're using some older Spring Security patterns, and there's no multi-factor authentication. No "remember me" functionality that's properly secured. And the session management could be tightened up.

**Sarah:** So we're not going to end up on the news for a data breach, but we could do better?

**Dev Lead:** *laughs* I mean, I never want to say never, but yeah—the fundamentals are okay, we're just missing modern security features that users expect in 2024. Things like OAuth integration so people can log in with Google or Apple, proper JWT tokens for the API calls, rate limiting to prevent abuse...

**[06:30]**

**Sarah:** Okay. So let me think about this. From my side, here's what I'm hearing from customers and from our executive team. The app looks dated. People are used to these really polished experiences now, and ours feels like we haven't invested in it. That affects brand perception.

**Dev Lead:** Makes sense.

**Sarah:** Second thing is mobile. I know we have a responsive layout, but have you actually used it on a phone lately?

**Dev Lead:** Not recently, honestly.

**Sarah:** It's rough. The navigation bar gets cramped, the cart icon is hard to tap, and the product grid doesn't really adapt well. My daughter showed me how Sephora's app works and it's night and day compared to ours.

**[08:00]**

**Dev Lead:** So we need better mobile responsiveness, or are you thinking a dedicated mobile experience?

**Sarah:** I don't think we need a native app—that's a whole other budget conversation—but the mobile web experience needs to be first-class. A lot of our customers browse on their phones during commutes or lunch breaks. If the experience is clunky, they're going to go somewhere else.

**Dev Lead:** Got it. So responsive design overhaul, touch-friendly interactions, that kind of thing.

**Sarah:** Yeah. And speaking of interactions—the category navigation is kind of hidden right now. We have Books, Music, Beauty, Electronics, but they're just text links in a nav bar. I'd love to see something more visual. Maybe category cards with nice imagery? Something that helps people explore.

**[09:30]**

**Dev Lead:** That's a good point. Right now the nav is very utilitarian. Just icons and text.

**Sarah:** And the search! Do we even have search?

**Dev Lead:** We have products organized by category, and you can browse by bestsellers, but there's no actual search functionality on the frontend.

**Sarah:** *sighs* Okay, that's definitely a gap. People expect to type in what they want and find it. We have what, 6,000 products? Customers aren't going to browse through pages and pages.

**[10:15]**

**Dev Lead:** Fair point. Adding search would mean some backend work too—we'd need to integrate a search service, maybe Elasticsearch or something similar. But it's doable.

**Sarah:** I trust you on the technical side. Just flag if anything's going to be a huge lift. Now, let me ask you something—and be honest with me—how bad is the code? Like, is this a "repaint the house" situation or a "tear it down and rebuild" situation?

**Dev Lead:** *pauses* It's somewhere in between, honestly. The backend services—the microservices architecture—that's actually pretty solid. Spring Boot, well-separated concerns, talks to the database properly. We could keep most of that.

**[11:30]**

**Sarah:** Okay, good.

**Dev Lead:** The frontend is where the age shows. We're using React, which is great, but we're using older patterns. Class components instead of functional components with hooks, older state management patterns, the styling is scattered across a bunch of CSS files with no real design system.

**Sarah:** What does that mean for us practically?

**Dev Lead:** It means if we want to modernize the look and feel, we probably want to do a frontend rebuild. Not throwing everything away, but migrating to more modern React patterns, implementing a proper design system, maybe using a UI framework that gives us nice components out of the box.

**[12:45]**

**Sarah:** And how long does something like that take?

**Dev Lead:** Depends on scope. If we're talking about a visual refresh with better mobile support, modern interactions, but keeping the same basic functionality? Maybe two to three months with a small team. If we're adding features like search, enhanced security, user profiles, wishlists... we're looking at longer.

**Sarah:** What about doing it in phases? Like, could we ship the visual refresh first and then add features?

**Dev Lead:** Absolutely. That's probably the smartest approach. Get the foundation right, ship something that looks modern and feels good on mobile, then iterate from there.

**[14:00]**

**Sarah:** Okay, I like that. Let me give you my priority list, just off the top of my head. Tell me if I'm crazy.

**Dev Lead:** Go for it.

**Sarah:** Number one—and this is tied—the app needs to look modern and the security stuff you mentioned needs to get fixed. I don't want customers thinking we're behind the times, and I definitely don't want that hardcoded user thing hanging over us.

**Dev Lead:** Agreed. Visual refresh and security hardening as the foundation.

**Sarah:** Number two is mobile. If someone pulls up our site on their phone, it should feel like it was designed for their phone, not like a desktop site that got squeezed.

**[15:15]**

**Dev Lead:** Touch targets, better responsive layouts, maybe a mobile-first approach to the redesign.

**Sarah:** Exactly. Number three is the navigation and discovery piece. Better category browsing, and eventually search. I know search is bigger, so maybe we do the category improvements first?

**Dev Lead:** That makes sense. We could add nice category tiles on the homepage, improve the nav to be more touch-friendly with bigger tap targets and maybe a mobile menu drawer. Search can be phase two.

**Sarah:** And then number four would be the nice-to-haves. Things like wishlists, better user profiles, order history. Stuff that makes people want to come back.

**[16:30]**

**Dev Lead:** What about checkout? You want to keep the flow basically the same, or are there pain points there?

**Sarah:** Good question. The checkout is... fine? I think? But now that you mention it, it feels very bare bones. Just your items, a total, and a checkout button. No guest checkout option, no saved payment methods, no estimated delivery. 

**Dev Lead:** Some of those are bigger features—saved payments means PCI compliance considerations.

**Sarah:** Right, right. Let's not boil the ocean. For phase one, just make it look better. More visual feedback, maybe a progress indicator so people know where they are in the flow. The actual payment processing can stay the same for now.

**[17:45]**

**Dev Lead:** Makes sense. Can I ask about timeline? Is there an event or deadline driving this?

**Sarah:** Not a hard deadline, but we're presenting to the board in Q2 and I'd love to show them something impressive. Shows we're investing in digital, which is a whole initiative the CEO cares about.

**Dev Lead:** So ideally phase one done by... April? May?

**Sarah:** May would be great. That gives us a month buffer before the board presentation.

**[18:30]**

**Dev Lead:** Okay. Let me summarize what I'm hearing and you tell me if I'm missing anything:

Phase one priority is a modern visual redesign—new typography, colors, animations, microinteractions—combined with security fixes including proper user authentication through the checkout flow. Mobile responsiveness is part of this, so the site feels native on phones.

**Sarah:** Yes, exactly.

**Dev Lead:** Phase two would be enhanced navigation—visual category browsing, improved product discovery, and search functionality.

**Sarah:** Right.

**Dev Lead:** And future phases could tackle things like wishlists, user profiles, order history, and checkout enhancements beyond visual improvements.

**[19:30]**

**Sarah:** That's it. You've got it. Oh, one more thing—

**Dev Lead:** Sure.

**Sarah:** I don't want it to look like every other website. You know how all these sites now have the same kind of look? White background, blue buttons, very... corporate? I want ours to have personality. We sell books, we sell music—there should be some warmth to it. Some character.

**Dev Lead:** A distinctive visual identity, not just "generic modern."

**Sarah:** Exactly. Like, obviously it needs to be clean and professional, but if it could feel like walking into a nice bookstore? That vibe? That would be amazing.

**[20:15]**

**Dev Lead:** I love that direction. We can definitely explore color palettes and typography that feel more warm and inviting. Maybe some cream tones, richer accent colors, serif fonts for that bookish feel.

**Sarah:** Yes! That's what I'm talking about. Okay, I think we've covered a lot. Can you put together a rough proposal or plan we can review next week?

**Dev Lead:** Absolutely. I'll write up the requirements from this conversation and put together some initial thoughts on approach. We should probably get design involved too.

**Sarah:** Great. Thanks for this—I feel a lot better knowing we're actually going to tackle this.

**Dev Lead:** Thanks Sarah. Talk soon.

---

## Summary of Informal Requirements

### Phase 1 (Target: Q2 2024)
- **Visual Modernization**
  - Modern typography (warm, bookish feel—move away from generic Roboto)
  - New color palette (warm tones, distinctive brand identity, avoid generic corporate look)
  - Animations and microinteractions (page transitions, hover effects, add-to-cart feedback)
  - Updated product cards with better visual hierarchy
  - Improved hero/banner section with interactivity

- **Security Hardening**
  - Fix hardcoded user ID issue in checkout service
  - Proper user authentication flow through all services
  - Session management improvements
  - Consider OAuth/social login for future

- **Mobile Experience**
  - Mobile-first responsive redesign
  - Touch-friendly tap targets
  - Mobile navigation (drawer/hamburger menu)
  - Better cart accessibility on small screens

### Phase 2
- **Navigation & Discovery**
  - Visual category browsing (category cards with imagery)
  - Improved homepage product discovery
  - Search functionality (requires backend integration)

### Future Phases
- Wishlists
- Enhanced user profiles
- Order history
- Checkout improvements (progress indicator, visual feedback)
- Guest checkout option
- Saved payment methods (PCI compliance required)

### Constraints & Notes
- Board presentation in Q2—need something impressive to show
- Avoid "generic AI/corporate" look—want personality and warmth
- Backend microservices are solid, frontend needs rebuild
- Phased approach preferred—ship MVP, iterate
- No native mobile app needed—mobile web should be first-class

