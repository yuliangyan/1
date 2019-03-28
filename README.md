A falsk app for show the daily pollen conditions of tree in the USA by using Pollen API.
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

4.




select * from air.stats



