A falsk app for show the daily pollen conditions of tree of the following three days in the USA by using Pollen API.
The variable which we called cc_url holds a JSON-formatted response to our GET request.

1.Set the region and zone for our new cluster. I chose "europe-west2-b" as it islocated in London UK, but any region should do.   
We also export the projectname as an environment variable for later ease of access:
gcloud config set compute/zone europe-west2-b
export PROJECT_ID="$(gcloud config get-value project -q)"

2.Inside of the Cassandra Terminal create a keyspace for the data to be insertedinto.
kubectl get pods -l name=cassandra
CREATE KEYSPACE air WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};

3.Following this,  create the table inside of the keyspace,  specifying all columnnames and types:
CREATE TABLE air.stats(date,value)

4.we will first need to create a Kubernetes cluster. We will be using the n1-standard-2 machines, which have two virtual CPU’s and more memory than the default. The following command creates a 3 node cluster named cassandra:
gcloud container clusters create cassandra --num-nodes=3 --machine-type "n1-standard-2"

5.Download these via the following commands:
wget -O cassandra-peer-service.yml http://tinyurl.com/yyxnephy
wget -O cassandra-service.yml http://tinyurl.com/y65czz8e
wget -O cassandra-replication-controller.yml http://tinyurl.com/y2crfsl8

6.Once these are downloaded we can now run our three components:
kubectl create -f cassandra-peer-service.yml
kubectl create -f cassandra-service.yml
kubectl create -f cassandra-replication-controller.yml

7.Check that the single container is running correctly:
kubectl get pods -l name=cassandra

and if so we can can scale up our number of nodes via our replication-controller:
kubectl scale rc cassandra --replicas=3

8.Then,we will be pulling data from our Cassandra database
into a flask web client.
1)First lets create our requirements.txt. This is the same as before, but has the
additional requirement of the python cassandra-driver.
pip
Flask
cassandra−driver
2)Next create the Dockerfile.
3)Thirdly create a new app.py

9.Now we can build our image as before:
docker build -t gcr.io/${PROJECT_ID}/y10:v1 .

Push it to the Google Repository:
docker push gcr.io/${PROJECT_ID}/y10:v1

and Run it as a service, exposing the deploment to get an external IP:
kubectl run y10 --image=gcr.io/${PROJECT_ID}/y10:v1 --port 8080
kubectl expose deployment y10 --type=LoadBalancer --port 80 --target-port 8080

10.get the external IP
kubectl get services

35.230.155.106/predict/tree/2019-03-28
