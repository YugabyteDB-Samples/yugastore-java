Create or update OpenAPI/Swagger documentation for all microservices.

Follow the instructions in `.claude/agents/swagger-docs.md` to:

1. Iterate through the Java code and identify all services
2. Create OpenAPI 3.0 specifications for each service
3. Save each specification as `openapi.yaml` in the respective service directory

Services to document:
- API Gateway Microservice
- Products Microservice
- Cart Microservice
- Checkout Microservice
- Login Microservice
- React UI BFF

Ensure all endpoints, request/response schemas, and domain objects are properly documented.
