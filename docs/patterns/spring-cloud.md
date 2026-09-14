# Spring Cloud patterns (Eureka + Feign)

## Eureka registration

Each service declares its Eureka server URL in `src/main/resources/bootstrap.yml`:

```yaml
eureka:
  client:
    serviceUrl:
      defaultZone: ${EUREKA_URI:http://localhost:8761/eureka}
```

`EUREKA_URI` is the standard override for non-local environments. The value of `spring.application.name` in `bootstrap.yml` becomes the Eureka app name (uppercased), which is what Feign clients reference.

## Feign client naming

Feign clients target services by Eureka app name:

```java
@FeignClient("products-microservice")   // matches spring.application.name in that service
public interface ProductCatalogRestClient { ... }
```

Spring Cloud handles service discovery and load balancing — no hardcoded host or port. Feign clients are injected as regular Spring beans.

## Spring Security

All services have a `SecurityConfiguration.java` that disables CSRF and HTTP Basic auth for local development:

```java
http.csrf().disable().authorizeRequests().antMatchers("/**").permitAll();
```

Do not remove this without also wiring proper auth — removing it without replacement will lock out all API calls.

## Spring Actuator

All services expose standard health/metrics endpoints at `/actuator/health`. Useful for confirming a service is up before testing an endpoint.
