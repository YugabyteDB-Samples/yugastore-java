# login-microservice

User authentication and registration. **Work in progress — optional.** The store functions without it.

@../docs/patterns/ysql.md

**Port:** 8085 | **Not Eureka-registered** | **Not started in the normal dev workflow**

## Status

No Dockerfile. Not integrated with api-gateway or any other service. Standalone Spring Boot app with JSP templates (Tomcat + Jasper + JSTL).

## Key classes

| Class | Location |
|---|---|
| `UserController` | `web/UserController.java` — login/registration web endpoints |
| `User`, `Role` | `model/` — JPA entities |
| `UserRepository`, `RoleRepository` | `repo/` |
| `UserServiceImpl` | `service/UserServiceImpl.java` |
| `WebSecurityConfig`, `SecurityConfig` | root package — Spring Security config |
