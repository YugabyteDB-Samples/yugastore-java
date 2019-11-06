FROM openjdk:8-jdk-alpine
COPY ./target/eureka-server-local-0.0.1-SNAPSHOT.jar /
EXPOSE 8761
ARG ipaddr
CMD java -jar /eureka-server-local-0.0.1-SNAPSHOT.jar --server.port=8761 --eureka.instance.preferIpAddress=true --eureka.instance.ipAddress=$ipaddr
