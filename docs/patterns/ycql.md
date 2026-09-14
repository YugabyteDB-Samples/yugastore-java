# YCQL connectivity pattern

Used by: `products-microservice`, `checkout-microservice`

YugabyteDB's Cassandra-compatible API. Port `9042`, keyspace `cronos`.

## Driver

The Yugabyte Java Driver (`com.yugabyte:java-driver-core:4.6.0-yb-10`) replaces the OSS DataStax driver. In `pom.xml`:

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-cassandra</artifactId>
  <exclusions>
    <exclusion>
      <groupId>com.datastax.oss</groupId>
      <artifactId>java-driver-core</artifactId>
    </exclusion>
  </exclusions>
</dependency>
<dependency>
  <groupId>com.yugabyte</groupId>
  <artifactId>java-driver-core</artifactId>
  <version>4.6.0-yb-10</version>
</dependency>
```

## Schema (keyspace: cronos)

| Table | Key columns | Purpose |
|---|---|---|
| `products` | `asin` (PK) | Full product metadata |
| `product_rankings` | `category` (PK), `sales_rank` (clustering) | Products by category, sorted by rank |
| `product_inventory` | `asin` (PK) | Stock quantity per product |
| `orders` | `asin`, `user_id`, `order_id` | Order records created at checkout |

DDL: [resources/schema.cql](../../resources/schema.cql)

## Config class pattern

The YCQL session is configured in a `@Configuration` class gated by Spring profile:

```java
@Configuration
@Profile("local")
public class YugabyteYCQLConfig extends AbstractCassandraConfiguration {
    @Override protected String getContactPoints() { return "127.0.0.1"; }
    @Override protected int getPort() { return 9042; }
    @Override protected String getKeyspaceName() { return "cronos"; }
}
```

A parallel `@Profile("cloud")` config class exists for deployed environments.

## Repositories

Use Spring Data Cassandra repositories (`CassandraRepository<T, ID>`). Entity classes are annotated with `@Table`; primary keys with `@PrimaryKey` (simple) or `@PrimaryKeyColumn` (composite, using a separate `@PrimaryKeyClass`).
