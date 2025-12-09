# High-Level Features - Yugastore E-Commerce Platform

This document outlines the major features and subfeatures of the Yugastore application, derived from analysis of the React frontend components, API controllers, and backend microservices.

---

## 1. Product Catalog

The core product browsing and discovery feature of the platform.

### 1.1 Product Listing
- Browse all products with pagination (12 items per page)
- Navigate between pages (Previous/Next)
- View product thumbnails, titles, prices, and star ratings
- Quick "Add to Cart" button on each product card

### 1.2 Category Navigation
Primary categories displayed in the navigation bar:
- Books
- Music
- Beauty
- Electronics

Extended categories available in footer:
- Kitchen & Dining
- Toys & Games
- Pet Supplies
- Grocery & Gourmet Food
- Video Games
- Movies & TV
- Arts, Crafts & Sewing
- Home & Kitchen
- Patio, Lawn & Garden
- Health & Personal Care
- Cell Phones & Accessories
- Industrial & Scientific
- Sports & Outdoors

### 1.3 Product Details Page
- Full product image display
- Product title and description
- Price display
- Star rating visualization (5-star system with half-stars)
- Number of reviews and total stars
- Brand information
- "Add to Cart" button

### 1.4 Product Recommendations
- "Also Bought" section showing related products
- Based on `also_bought`, `also_viewed`, `bought_together`, and `buy_after_viewing` data

### 1.5 Product Sorting
Available sort options:
- By highest rating (`num_stars`)
- By most reviews (`num_reviews`)
- By best selling (`num_buys`)
- By most pageviews (`num_views`)

---

## 2. Shopping Cart

Persistent shopping cart functionality across the user session.

### 2.1 Cart Management
- Add items to cart from product listings or detail pages
- Remove items from cart
- View cart contents with product images and details
- Real-time cart count display in navigation bar
- Visual feedback on cart errors

### 2.2 Cart Display
- Product image, title, and link to product page
- Individual product price
- Quantity of each item
- Running subtotal calculation
- Tax display (currently $0.00)

### 2.3 Cart Persistence
- Cart data persisted per user session
- Cart automatically fetched on page load
- Cart state maintained during navigation

---

## 3. Checkout & Orders

Complete order processing workflow.

### 3.1 Checkout Process
- Single-click checkout from cart page
- Inventory validation before purchase
- Out-of-stock detection with appropriate messaging
- Transactional order creation (using Cassandra transactions)

### 3.2 Order Confirmation
- Order number generation (UUID-based)
- Order details summary (products, quantities, total)
- "Thank you" confirmation message
- Order number displayed as `#kmp-{orderNumber}`

### 3.3 Inventory Management
- Real-time inventory quantity tracking
- Automatic inventory deduction on successful checkout
- Validation against available stock

### 3.4 Order Records
- Order ID
- User ID association
- Order details (items purchased)
- Order timestamp
- Order total amount

---

## 4. User Authentication

User registration and login system (via login-microservice).

### 4.1 User Registration
- Registration form with validation
- Username and password fields
- Password confirmation
- Redirect to login after successful registration

### 4.2 User Login
- Username/password authentication
- Error messaging for invalid credentials
- Logout functionality with confirmation message
- Session-based authentication

### 4.3 User Management
- User role support (role-based access)
- User validation (via UserValidator)
- Secure password handling

---

## 5. Homepage & Marketing

Landing page experience with promotional content.

### 5.1 Hero Section
- Full-width promotional banner/image
- Brand showcase area

### 5.2 Bestseller Highlights
- Featured products from each major category:
  - Bestsellers in Books (4 items)
  - Bestsellers in Music (4 items)
  - Bestsellers in Beauty (4 items)
  - Bestsellers in Electronics (4 items)
- Quick links to category pages

### 5.3 Newsletter Subscription
- Email subscription form
- Marketing messaging ("Let's keep the conversation going")
- Call-to-action for newsletter signup

---

## 6. Navigation & UI

Site-wide navigation and user interface elements.

### 6.1 Navigation Bar
- Logo with link to homepage
- Category links with icons (Books, Music, Beauty, Electronics)
- Shopping cart icon with item count badge
- Scroll-responsive styling (transparent to solid)
- Active state highlighting for current category

### 6.2 Footer
- Logo display
- Brand attribution (YugaByte DB)
- Copyright notice
- Extended category links (18 categories)
- External link to yugabyte.com

### 6.3 Responsive Design
- Mobile-friendly layouts (Bootstrap grid)
- Adaptive navigation
- Responsive product grids (1-4 columns based on viewport)

---

## 7. Microservices Architecture

Backend services supporting the features above.

| Service | Port | Responsibility |
|---------|------|----------------|
| Eureka Server | 8761 | Service discovery and registration |
| API Gateway | 8081 | Request routing and API aggregation |
| Products | 8082 | Product catalog and metadata |
| Cart | 8083 | Shopping cart operations |
| Login | 8085 | User authentication |
| Checkout | 8086 | Order processing and inventory |
| React UI | 8080 | Frontend web application |

---

## 8. Data Storage

Database layer powered by YugabyteDB.

### 8.1 YCQL (Cassandra-compatible)
- Products table (metadata, images, pricing)
- Product inventory tracking
- Product rankings by category
- Orders table
- Shopping cart storage

### 8.2 YSQL (PostgreSQL-compatible)
- User authentication data
- Role-based permissions

---

## Feature Summary Matrix

| Feature Area | Implemented | Partially Implemented | Not Implemented |
|--------------|-------------|----------------------|-----------------|
| Product Browsing | Yes | - | - |
| Category Filtering | Yes | - | - |
| Product Search | - | - | No search bar |
| Shopping Cart | Yes | - | - |
| Checkout | Yes | - | - |
| User Auth | Yes | - | - |
| Product Reviews | Display only | Write reviews | - |
| Wishlists | - | - | No |
| Order History | - | - | No user-facing view |
| Product Recommendations | Yes | - | - |
| Newsletter | UI only | Backend integration | - |

