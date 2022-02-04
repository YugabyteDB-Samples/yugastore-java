FROM eclipse-temurin:17-jre
COPY ./target/api-gateway-microservice-0.0.1-SNAPSHOT.jar /
EXPOSE 8081
ARG ipaddr
CMD java -jar /api-gateway-microservice-0.0.1-SNAPSHOT.jar --server.port=8081 --eureka.instance.preferIpAddress=true --eureka.instance.hostname=$ipaddr
