from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import csv
from time import sleep
import auth
import math

cloud_config = {'secure_connect_bundle': auth.scb_path}
auth_provider = PlainTextAuthProvider(auth.auth_id, auth.auth_token)
cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
session = cluster.connect()



row = session.execute("select release_version from system.local").one()
if row:
  print(row[0])
else:
  print("An error occurred.")

keyspace = "mnist_digits"

train_insert_statement = "INSERT INTO " + keyspace + "." + "raw_train" + " JSON '"
test_insert_statement = "INSERT INTO " + keyspace + "." + "raw_test" + " JSON '"
predict_insert_statement = "INSERT INTO " + keyspace + "." + "raw_predict" + " JSON '"
end_insert_statement = "';"

total_entires = 0
with open('train.csv', newline='\n') as temp_csvfile:
  temp_reader = csv.DictReader(temp_csvfile)
  entries = sum(1 for row in temp_reader)

print("Entries: "+str(entries))
train_split = .8
inflection_point = math.floor(entries*train_split)

with open('train.csv', newline='\n') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
      label = int(row.pop("label"))
      pixel_list = [int(x) for x in list(row.values())]
      if i < inflection_point:
          cassandra_row = {"id":i, "label":label, "pixels":pixel_list}
          session.execute(train_insert_statement+str(cassandra_row).replace("'",'"')+end_insert_statement)
      else:
          cassandra_row = {"id":i-inflection_point, "label":label, "pixels":pixel_list}
          session.execute(test_insert_statement+str(cassandra_row).replace("'",'"')+end_insert_statement)
      if (i%100==0):
          print("Line "+str(i))
      i = i+1


with open('test.csv', newline='\n') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
      pixel_list = [int(x) for x in list(row.values())]
      cassandra_row = {"id":i, "pixels":pixel_list}
      session.execute(predict_insert_statement+str(cassandra_row).replace("'",'"')+end_insert_statement)
      if (i%100==0):
          print("Line "+str(i))
      i = i+1