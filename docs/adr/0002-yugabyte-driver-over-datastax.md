# ADR-0002: Use the Yugabyte Java Driver, not the DataStax OSS driver, for YCQL modules

**Status:** Accepted
**Date:** 2026-09-14 (retroactively documented — the decision predates this ADR process)

## Context

`products-microservice` and `checkout-microservice` talk to YugabyteDB over YCQL (Cassandra-compatible). Spring Boot's `spring-boot-starter-data-cassandra` pulls in the OSS DataStax driver by default, which is not YugabyteDB-aware (partition/topology handling, driver-level compatibility).

## Decision

Both modules explicitly depend on `com.yugabyte:java-driver-core:4.6.0-yb-10` and explicitly exclude the DataStax OSS driver from `spring-boot-starter-data-cassandra`.

## Consequences

Do not add a DataStax driver dependency to a YCQL-backed module, even transitively — it will conflict with or silently shadow the Yugabyte-aware driver. See `docs/gotchas.md` for the specific dependency exclusion.
