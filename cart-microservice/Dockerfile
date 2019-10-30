FROM openjdk:8-jdk-alpine
COPY ./target/cart-microservice-0.0.1-SNAPSHOT.jar /
EXPOSE 8083
ARG ipaddr
CMD java -jar /cart-microservice-0.0.1-SNAPSHOT.jar --server.port=8083 --eureka.instance.preferIpAddress=true --eureka.instance.hostname=$ipaddr
