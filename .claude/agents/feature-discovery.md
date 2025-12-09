# Feature Discovery Agent

Analyze the application to derive and document all major features and subfeatures.

## Instructions

1. Browse the application (localhost:8080) and recursively analyze links and pages
2. Perform multiple "random walks" through the website structure
3. Create a file called `high_level_features.md` in the repository root

## Methodology

Feature discovery should include:

### 1. Frontend Route Analysis
- Examine React Router configuration to identify all navigable pages
- Document URL patterns and route parameters

### 2. Navigation Component Inspection
- Analyze NavBar and Footer components
- Discover all user-facing navigation links

### 3. API Endpoint Mapping
- Trace REST API controllers in microservices
- Document controller responsibilities

### 4. Component Deep Dive
- Read individual React components
- Understand feature implementation details

### 5. Data Model Analysis
- Examine domain objects and entities
- Understand data relationships

### 6. Service Logic Review
- Analyze backend service implementations
- Document business logic flows

## Output Format

The `high_level_features.md` should include:

1. **Methodology Section** - Explain the approach used for discovery
2. **Major Feature Areas** - Numbered sections for each major feature
3. **Subfeatures** - Detailed breakdown under each major feature
4. **Microservices Architecture** - Table of services and responsibilities
5. **Data Storage** - Database layer documentation
6. **Feature Summary Matrix** - Table showing implemented vs not implemented features

## Categories to Consider

- Product Catalog
- Shopping Cart
- Checkout & Orders
- User Authentication
- Homepage & Marketing
- Navigation & UI
- Search functionality
- Recommendations
