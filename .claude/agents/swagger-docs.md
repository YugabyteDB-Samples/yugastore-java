# Swagger Documentation Agent

Create OpenAPI/Swagger definitions for all microservices in this application.

## Instructions

1. Iterate through the Java code and identify all services
2. Create OpenAPI 3.0 specifications for each service
3. Save each specification in the service's directory as `openapi.yaml`

## Services to Document

Analyze and document all microservices found in the codebase, typically including:
- API Gateway
- Products Microservice
- Cart Microservice
- Checkout Microservice
- Login Microservice
- React UI BFF (Backend for Frontend)

## Specification Requirements

For each service, the OpenAPI spec should include:
- Service title and description
- Server URL (localhost port)
- All REST endpoints with:
  - HTTP method
  - Path and path parameters
  - Query parameters
  - Request body schemas
  - Response schemas and status codes
  - Operation IDs and tags
- Component schemas for all domain objects
- Authentication/security schemes if applicable

## Output

- Create `openapi.yaml` in each microservice directory
- Ensure specs are valid OpenAPI 3.0 format
- Include meaningful descriptions for all endpoints and schemas
