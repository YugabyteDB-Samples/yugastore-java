FROM openjdk:8-jdk-alpine
COPY ./target/checkout-microservice-0.0.1-SNAPSHOT.jar /
EXPOSE 8086
ARG ipaddr
CMD java -jar /checkout-microservice-0.0.1-SNAPSHOT.jar --server.port=8086 --eureka.instance.preferIpAddress=true --eureka.instance.hostname=$ipaddr --cronos.yugabyte.hostname=$ipaddr
