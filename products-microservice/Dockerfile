FROM openjdk:8-jdk-alpine
COPY ./target/products-microservice-0.0.1-SNAPSHOT.jar /
EXPOSE 8082
ARG ipaddr
CMD java -jar /products-microservice-0.0.1-SNAPSHOT.jar --server.port=8082 --eureka.instance.preferIpAddress=true --eureka.instance.hostname=$ipaddr --cronos.yugabyte.hostname=$ipaddr
