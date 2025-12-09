# Technical Specification Document
Bookstore Application - Version 1.0 (Fixed)

## 1. System Architecture

SPEC-001: The system implements a microservices architecture with the following services:
- API Gateway Service (port 8080)
- Products Service (port 8081)
- Cart Service (port 8082)
- Checkout Service (port 8083)
- Login Service (port 8084)

Addresses: REQ-100, REQ-101

SPEC-002: Services communicate via REST APIs with JSON payloads

SPEC-003: The system uses YugabyteDB as a distributed database solution
Addresses: REQ-102

## 2. Search and Product Discovery

SPEC-010: The search endpoint is available at `/api/products/search`
- Accepts query parameters: `q` (search term), `page` (integer), `limit` (integer, max 100)
- Supports exact and fuzzy matching on title, author, and ISBN fields
- Returns paginated results with metadata including: totalResults, currentPage, totalPages

Addresses: REQ-001, REQ-003

SPEC-011: Search results include product information with cover image URLs
- Each result includes: title, author, ISBN, price, rating, coverImageUrl
- Images are served via CDN with HTTPS
- Missing images fall back to placeholder

Addresses: REQ-002

SPEC-012: The system provides filtering capabilities through query parameters:
- category: String enum (Fiction, Non-Fiction, Science, Technology, etc.)
- minPrice/maxPrice: Decimal values in USD
- minRating: Integer 1-5
- Filter results must match ALL specified criteria

Addresses: REQ for filtering by category, price range, and rating

SPEC-013: Search response time must be under 2 seconds measured at 95th percentile
- Database queries use indexed fields
- Results are cached for 5 minutes
- Query optimization with EXPLAIN analysis

Addresses: REQ "Search function must return results within 2 seconds"

## 3. Shopping Cart

SPEC-020: Cart management endpoints:
- POST `/api/cart/items` - Add item to cart (returns 201 Created)
- PUT `/api/cart/items/{id}` - Update quantity (returns 200 OK)
- DELETE `/api/cart/items/{id}` - Remove item (returns 204 No Content)
- GET `/api/cart` - Get cart contents (returns 200 OK)

Addresses: REQ "Users must be able to add books to shopping cart"

SPEC-021: Cart data persistence:
- Cart contents stored in database table linked to user session ID
- Cart survives browser closure and page refresh
- Cart expires after 30 days of inactivity
- Guest carts converted to user carts upon login

Addresses: REQ "The system shall persist cart contents across sessions"

SPEC-022: Cart displays running totals:
- Subtotal: Sum of all item prices × quantities
- Tax: Calculated based on user's shipping state tax rate
- Shipping: Calculated based on weight and destination
- Total: Subtotal + Tax + Shipping
- All amounts shown with 2 decimal places

Addresses: REQ "Cart must show running total including tax"

SPEC-023: Cart quantity modification:
- Users can set quantity from 1 to 99
- Quantity field validates input and rejects non-numeric values
- Quantity 0 removes item from cart
- Updates are persisted immediately

Addresses: REQ "Users should be able to modify quantities in the cart"

## 4. User Authentication

SPEC-030: User registration endpoint at `/api/auth/register`
- Required fields: email (valid format), password (min 8 chars), name
- Password requirements: minimum 8 characters, at least 1 uppercase, 1 lowercase, 1 number
- Passwords are hashed using bcrypt with cost factor 12 before storage
- Returns 201 Created with user ID on success
- Returns 400 Bad Request if email already exists

Addresses: REQ-010, REQ-020

SPEC-031: Login endpoint at `/api/auth/login`
- Accepts email and password in request body
- Returns JWT token valid for 8 hours on success
- Token includes user ID, email, and role claims
- Failed login attempts are logged with: timestamp, email (not password), IP address, user-agent
- After 5 failed attempts in 15 minutes, account is temporarily locked for 15 minutes

Addresses: REQ-011, REQ "Failed login attempts should be logged for security"

SPEC-032: Session management:
- JWT tokens include expiration time (exp claim)
- Sessions automatically timeout after 30 minutes of inactivity
- Timeout duration configurable via SESSION_TIMEOUT_MINUTES environment variable
- Client receives 401 Unauthorized when token expires

Addresses: REQ "User sessions must timeout after 30 minutes of inactivity"

SPEC-033: Password reset functionality:
- POST `/api/auth/password-reset/request` - Initiates password reset
- Sends email with secure token valid for 1 hour
- POST `/api/auth/password-reset/confirm` - Completes reset with token and new password
- Tokens are single-use and cryptographically secure (256-bit random)
- Old password is invalidated immediately

Addresses: REQ-012 "The system needs to provide password reset functionality via email"

SPEC-034: Security measures:
- All passwords hashed with bcrypt (never stored plaintext)
- Session tokens use cryptographically secure random generation (crypto.randomBytes)
- Sensitive data (passwords, tokens, credit cards) never logged
- Failed authentication attempts trigger monitoring alerts after threshold

Addresses: REQ-020, REQ-021, REQ "Session tokens need to be cryptographically secure", 
          REQ "Sensitive data must never appear in logs"

## 5. Checkout and Payment

SPEC-040: Checkout process endpoint at `/api/checkout/process`
- Accepts: payment method, billing address, shipping address
- Validates card via payment gateway before processing
- Calculates tax based on shipping address state using TaxJar API
- Calculates shipping via USPS API based on weight and distance
- All payment data transmitted over HTTPS/TLS 1.3
- Credit card numbers and CVV never stored or logged

Addresses: REQ "Users must be able to complete purchases with credit card payment",
          REQ "Tax calculation must be accurate for user's state",
          REQ "The system should calculate shipping costs based on location",
          REQ-021, PRINCIPLE about not logging credit cards

SPEC-041: Order confirmation emails:
- Sent immediately after successful order processing
- Includes: order number, items, quantities, prices, total, shipping address, estimated delivery
- Email sent via SendGrid API
- Failure to send email does not block order (logged for retry)

Addresses: REQ "The system shall send order confirmation emails"

SPEC-042: Order history:
- GET `/api/orders/history` returns paginated list of user's orders
- Each order includes: orderNumber, date, items, total, status, trackingNumber
- Orders sorted by date descending
- Pagination: 20 orders per page

Addresses: REQ "Order history needs to be accessible to users"

## 6. Performance Optimizations

SPEC-050: Product catalog caching:
- Redis cache with 1 hour TTL for product details
- Cache key format: `product:{productId}`
- Cache miss triggers database query and cache population
- Cache invalidated on product updates via pub/sub
- Cache hit rate monitored (target: >90%)

Addresses: REQ-110

SPEC-051: Database connection pool configuration:
- Minimum connections: 10
- Maximum connections: 100
- Connection timeout: 30 seconds
- Idle timeout: 10 minutes
- Connection validation query: SELECT 1

Addresses: REQ-111

SPEC-052: Homepage performance optimization:
- Lazy loading for images below the fold
- Critical CSS inlined in HTML head
- JavaScript bundles code-split by route
- CDN for static assets with cache headers
- Target: First Contentful Paint < 1.5s, Total load time < 3 seconds

Addresses: REQ "The homepage must load in under 3 seconds"

SPEC-053: Concurrent user handling:
- Load balancer distributes requests across multiple service instances
- Horizontal auto-scaling triggers at 70% CPU utilization
- Database read replicas for query load distribution
- Tested to handle 1000 concurrent users (exceeds requirement of 500)

Addresses: REQ "The system needs to handle at least 500 concurrent users"

SPEC-054: API performance targets:
- 95th percentile response time < 200ms
- 99th percentile response time < 500ms
- Monitored via Prometheus with alerts at thresholds
- Performance dashboards in Grafana

Addresses: REQ "API response times should be under 200ms for 95% of requests"

## 7. API Design

SPEC-060: All APIs follow RESTful conventions:
- GET for retrieval (idempotent)
- POST for creation (returns 201 Created)
- PUT for full updates (idempotent)
- PATCH for partial updates
- DELETE for removal (idempotent, returns 204 No Content)
- Resource-based URLs: `/api/{resource}/{id}`

Addresses: REQ-120, REQ-121

SPEC-061: Standard HTTP status codes:
- 200 OK - Successful GET/PUT
- 201 Created - Successful POST
- 204 No Content - Successful DELETE
- 400 Bad Request - Invalid input
- 401 Unauthorized - Missing/invalid auth
- 403 Forbidden - Insufficient permissions
- 404 Not Found - Resource doesn't exist
- 500 Internal Server Error - Server failure

Addresses: REQ-121

SPEC-062: Rate limiting implementation:
- Implemented at API Gateway level using Redis
- Default: 100 requests per minute per IP address
- Configurable per endpoint in gateway configuration
- Returns 429 Too Many Requests when limit exceeded
- Response includes Retry-After header

Addresses: REQ-122

## 8. Error Handling

SPEC-070: Standardized error response format:
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid email format",
    "field": "email",
    "timestamp": "2025-12-08T10:30:00Z"
  }
}
```
- Error messages user-friendly and actionable
- No internal system details exposed in production
- Stack traces only in development environment

Addresses: REQ-131 "Error messages shall not expose sensitive system information"

SPEC-071: Transaction management:
- All database mutations wrapped in transactions
- Automatic rollback on any error during transaction
- Savepoints for nested transactions
- Transaction timeout: 30 seconds

Addresses: REQ-132 "Failed transactions must be rolled back completely"

SPEC-072: Error notification system:
- Critical errors trigger PagerDuty alerts immediately
- High severity errors logged and aggregated
- User-facing errors provide clear recovery instructions
- Example: "Payment failed. Please check your card details and try again."

Addresses: REQ "Critical errors need to trigger immediate notifications",
          REQ "User-facing errors should provide helpful recovery instructions"

## 9. Monitoring and Logging

SPEC-080: Authentication logging:
- All login attempts logged with structured format
- Fields: timestamp, email, ipAddress, userAgent, result (success/failure/locked)
- Passwords NEVER logged (security violation)
- Logs sent to centralized logging (ELK stack)
- Retention: 90 days

Addresses: REQ-140, REQ "Failed login attempts should be logged for security"

SPEC-081: API performance metrics:
- Metrics collected for every API endpoint
- Captured: response time, status code, endpoint, method
- Aggregated as: min, max, mean, p50, p95, p99
- Error rate calculated per endpoint
- Request volume tracked per minute

Addresses: REQ-141

SPEC-082: Distributed tracing:
- OpenTelemetry instrumentation for all services
- Trace ID propagated through all service calls
- Trace data exported to Jaeger
- Enables end-to-end request tracking

Addresses: REQ-142

SPEC-083: Log retention and monitoring:
- Application logs retained for 90 days
- Audit logs retained for 7 years (compliance)
- Real-time monitoring dashboard shows: request rate, error rate, response times, active users
- Health checks for all services every 30 seconds

Addresses: REQ "Log retention must be at least 90 days",
          REQ "Monitoring dashboards should display real-time system health"

## 10. Integrations

SPEC-090: Payment gateway integration:
- Stripe API for credit card processing
- PCI DSS Level 1 certified
- Card data tokenized (never stored)
- 3D Secure support for fraud prevention
- Webhook for asynchronous payment notifications

Addresses: REQ-150

SPEC-091: Email service integration:
- SendGrid API for transactional emails
- Templates: order confirmation, password reset, shipping notification
- Track email delivery status and bounces
- Retry logic for failed sends (max 3 retries)

Addresses: REQ-151

SPEC-092: Inventory management integration:
- Real-time sync via REST API to external inventory system
- Updates pushed when: order placed, order cancelled, manual adjustment
- Polling fallback every 5 minutes for resilience
- Inventory levels cached with 1-minute TTL

Addresses: REQ-152 "The system needs to integrate with inventory management system"

## 11. Data Management

SPEC-100: Automated backup strategy:
- Full database backup daily at 2:00 AM UTC
- Incremental backups every 6 hours
- Backups stored in S3 with encryption
- Retention: 30 days for daily, 90 days for monthly
- Backup restoration tested monthly

Addresses: REQ-112

SPEC-101: Real-time inventory updates:
- Event-driven architecture using Kafka
- Events: ORDER_PLACED, ORDER_CANCELLED, INVENTORY_ADJUSTED
- Consumers update product inventory table
- Eventual consistency with conflict resolution

Addresses: REQ "Product inventory must be updated in real-time"

SPEC-102: Data export functionality:
- Users can export their data in JSON format
- Includes: profile, order history, cart data
- Available at GET `/api/users/export`
- Complies with GDPR data portability requirements

Addresses: REQ "The system needs to support data export in JSON format",
          PRINCIPLE "The system must comply with GDPR requirements"

## 12. Accessibility

SPEC-110: WCAG 2.1 AA compliance:
- Color contrast ratio minimum 4.5:1 for normal text
- All interactive elements keyboard accessible
- ARIA labels on all form inputs
- Skip navigation links for screen readers
- Alt text on all images
- Focus indicators visible on all interactive elements

Addresses: REQ "The UI should be accessible to screen readers",
          REQ "Color contrast needs to meet WCAG 2.1 AA standards"

SPEC-111: Screen reader support:
- Semantic HTML5 elements used throughout
- Dynamic content updates announced via ARIA live regions
- Form validation errors announced to screen readers
- Loading states communicated accessibly

Addresses: REQ "The UI should be accessible to screen readers"

## 13. Mobile Responsiveness

SPEC-120: Responsive design implementation:
- Breakpoints: 320px (mobile), 768px (tablet), 1024px (desktop)
- Fluid typography scales between breakpoints
- Touch targets minimum 44x44 pixels
- Mobile-first CSS approach
- Tested on: iOS Safari, Chrome Android, Samsung Internet

Addresses: PRINCIPLE "The system should work on mobile devices"

SPEC-121: Mobile optimizations:
- Images served in multiple sizes via srcset
- Reduced motion for users with vestibular disorders
- Touch-friendly spacing and button sizes
- Mobile navigation with hamburger menu


