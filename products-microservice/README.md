# Kronos-cassandra-rest-api

App provides rest endpoints for searching the product catalog and provides results for displaying the analystics on the frontend. It uses Spring Data Cassandra and Spring Data Rest for exposing the data stored in YugabyteDB to downstream application. 

### Prerequisites

1. Access to PCF environment
2. Cassandra statefull set running in PKS
3. IP address of LoadBalencer/Nodeport exposing the YugaByteDB service

### Deploying the app to PCF

Step 1: Build the Spring Boot application 

```
mvn clean package -DSkipTests
```

Step 2: Deploy the app onto PCF

```
cf push
```

