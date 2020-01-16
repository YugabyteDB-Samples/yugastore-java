# Yugastore on Managed Kubernetes

This is an implementation of a sample ecommerce app. This microservices-based retail marketplace or eCommerce app is composed of **microservices written in Spring (Java)**, a **UI based on React**, **YugaByte DB as the distributed SQL database** and **Istio for microservices traffic management**.


# Features

* Written fully in Spring
* Desgined for multi-region and Kubernetes-native deployments
* Istio for microservices traffic management and Service Discovery
* Features 6 microservices
* Sample data has over 6K products in the store


# Build and run

## Build Jars with Maven 
To build, simply run the following from the base directory:

```
$ mvn -DskipTests package
```


## Build a Docker Image with Maven

To get started quickly, you can run Jib without even changing your pom.xml:

```
$ ./mvnw com.google.cloud.tools:jib-maven-plugin:dockerBuild -Dimage=nchandrappa/cart-microservice
```

To push to a Docker registry you use the build goal, instead of dockerBuild, i.e.

```
$ ./mvnw com.google.cloud.tools:jib-maven-plugin:build -Dimage=nchandrappa/cart-microservice
```

Note: Update docker image id to reflect the docker repository of your choice.


## Deploy Istio on kubernetes

Install Istio on your kubernetes cluster using `demo` profile so that monitoring and tracing are enabled by default for microservices. [Istio installation docs] (https://istio.io/docs/setup/install/helm/) 


## Deploy YugabyteDB cluster on Kubernetes

You can [install YugaByte DB by following these instructions](https://docs.yugabyte.com/latest/quick-start/).

a. Install YugabyteDB in minikube

```
$ kubectl create -f k8s-deployments/util/default-rbac.yml
$ kubectl create namespace yb-demo
$ kubectl create -f k8s-deployments/Yugabyte/yugabyte-statefulset-rf-1.yaml -n yb-demo

```

## Load Sample Data into cluster created in previous step

a. Verify YugabyteDB installation by connecting to postgres terminal using the following command

```
$ kubectl -n yb-demo exec -it yb-tserver-0 /home/yugabyte/bin/ysqlsh -- -h yb-tserver-0  --echo-queries
```

b. find the external-ip for YugabyteDB cluster by running the below command 

```
$ kubectl get service yb-db-service -n yb-demo
```

set the following environment variables from above data.  example: 

```
$ export CQLSH_HOST=192.168.64.3
$ export CQLSH_PORT=9042
$ export YSQLSH_HOST=192.168.64.3
$ export YSQLSH_PORT=5433
```

d. Now create the necessary tables as shown below. Load sample dataset by following the steps here: (resources/README.md)

```
$ cqlsh -f resources/schema.cql
```

Next, load some sample data. Follow the data load steps in 

```
$ ./resources/dataload.sh
```

Create the postgres tables in `resources/schema.sql` for the YSQL tables

```
$ ysqlsh -h $YSQLSH_HOST -p $YSQLSH_PORT -d postgres -f schema.sql
```

## Deploy Istio Destination Rules and Virtual Servers


```
kubectl label namespace default istio-injection=enabled
kubectl apply -f  k8s-deployments/istio/destination-rule-all.yaml
kubectl apply -f  k8s-deployments/istio/virtual-service-all.yaml
```


## Deploy Yugastore Microservices on Kubernetes

Make sure you have built the docker images as described above and you're in the `yugastore-java` base directory. Now do the following steps.

```
$ kubectl apply -f k8s-deployments/microservices/yugastore-deployment.yaml
```

## Deploy istio ingress gateway for Yugastore-UI microservice

```
$ kubectl apply -f k8s-deployments 
```

## Find the Istio gateway external-ip address and navigate to Yugastore-UI

```
$ kubectl get service istio-ingressgateway -n istio-system
```

# Traffic Management with Istio - Day 2 operations

We have two versions of cart-microservice, one which uses standard postgres jdbc driver and v2 of the same microservice that uses YugabyteDB cluster aware JDBC driver. We are going to use these two microservices to demonstrate set of day 2 tasks that are commonly used in in microservices deployments like, canary testing, A/B testing, chaos testing.. to name a few.


## Canary testing of cart microservice

Canary releases are used to reduce the risk of deploying a new version of microservice into production. You start by routing only a few selected users or small percentage of traffic on to newer version of the microservice. In this task, you'll configure a virtualservice to route 95% of traffic to cart-microservice:v1 and 5% of traffic to cart-microservice:v2.

```
$ kubectl apply -f k8s-deployments/istio/cart-microservice-canary-testing.yaml
```

## A/B Testing of cart microservice

A/B testing is used to for testing the new features that are going to prod, like its usability, popularity, noticeability etc. In this task, you will configure a virtualservice to route 50% of traffic onto cart-microservice:v1 and other 50% of traffic to cart-microservice:v1

```
$ kubectl apply -f cart-microservice-ab-testing.yaml
```
