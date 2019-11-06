# Get ip address on which to run the microservices
ipaddr=$(hostname -I| cut -d ' ' -f 1)

# Run eureka microservice, assuming the latest entry is to be used
list=$(docker images | grep 'yugastore-eureka' | head -n 1 )
image=$(echo $list | cut -d ' ' -f 1)
version=$(echo $list | cut -d ' ' -f 2)

if [ -z "$image" ]
then
    echo "Eureka docker image not found"
else
    if [ -z "$version" ]
    then
        docker run -e ipaddr=$ipaddr -p 8761:8761 -d $image
    else
        docker run -e ipaddr=$ipaddr -p 8761:8761 -d $image:$version
    fi
fi

# Run api-gateway microservice, assuming latest entry is to be used
list=$(docker images | grep 'yugastore-api' | head -n 1 )
image=$(echo $list | cut -d ' ' -f 1)
version=$(echo $list | cut -d ' ' -f 2)

if [ -z "$image" ]
then
    echo "Api-gateway docker image not found"
else
    if [ -z "$version" ]
    then
        docker run -e ipaddr=$ipaddr -p 8081:8081 -d $image
    else
        docker run -e ipaddr=$ipaddr -p 8081:8081 -d $image:$version
    fi
fi

# Run products microservice, assuming latest entry is to be used
list=$(docker images | grep 'yugastore-products' | head -n 1 )
image=$(echo $list | cut -d ' ' -f 1)
version=$(echo $list | cut -d ' ' -f 2)

if [ -z "$image" ]
then
    echo "Products docker image not found"
else
    if [ -z "$version" ]
    then
        docker run -e ipaddr=$ipaddr -p 8082:8082 -d $image
    else
        docker run -e ipaddr=$ipaddr -p 8082:8082 -d $image:$version
    fi
fi

# Run checkout microservice, assuming latest entry is to be used
list=$(docker images | grep 'yugastore-checkout' | head -n 1 )
image=$(echo $list | cut -d ' ' -f 1)
version=$(echo $list | cut -d ' ' -f 2)

if [ -z "$image" ]
then
    echo "checkout docker image not found"
else
    if [ -z "$version" ]
    then
        docker run -e ipaddr=$ipaddr -p 8086:8086 -d $image
    else
        docker run -e ipaddr=$ipaddr -p 8086:8086 -d $image:$version
    fi
fi

# Run cart microservice, assuming latest entry is to be used
list=$(docker images | grep 'yugastore-cart' | head -n 1 )
image=$(echo $list | cut -d ' ' -f 1)
version=$(echo $list | cut -d ' ' -f 2)

if [ -z "$image" ]
then
    echo "cart docker image not found"
else
    if [ -z "$version" ]
    then
        docker run -e ipaddr=$ipaddr -p 8083:8083 -d $image
    else
        docker run -e ipaddr=$ipaddr -p 8083:8083 -d $image:$version
    fi
fi

# Run react-ui microservice, assuming latest entry is to be used
list=$(docker images | grep 'yugastore-react' | head -n 1 )
image=$(echo $list | cut -d ' ' -f 1)
version=$(echo $list | cut -d ' ' -f 2)

if [ -z "$image" ]
then
    echo "react-ui docker image not found"
else
    if [ -z "$version" ]
    then
        docker run -e ipaddr=$ipaddr -p 8080:8080 -d $image
    else
        docker run -e ipaddr=$ipaddr -p 8080:8080 -d $image:$version
    fi
fi

