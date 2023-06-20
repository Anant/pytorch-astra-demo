from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import csv
from time import sleep

cloud_config = {'secure_connect_bundle': '<secure-connect_bundle>'}
auth_provider = PlainTextAuthProvider('<id>', '<token>')
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
end_insert_statement = "';"

with open('/workspace/template-python-flask/train.csv', newline='\n') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
      label = int(row.pop("label"))
      pixel_list = [int(x) for x in list(row.values())]
      cassandra_row = {"id":i, "label":label, "pixels":pixel_list}
      session.execute(train_insert_statement+str(cassandra_row).replace("'",'"')+end_insert_statement)
      print("Line "+str(i))
      i = i+1


with open('/workspace/template-python-flask/test.csv', newline='\n') as csvfile:
    reader = csv.DictReader(csvfile)
    i = 0
    for row in reader:
      pixel_list = [int(x) for x in list(row.values())]
      cassandra_row = {"id":i, "pixels":pixel_list}
      session.execute(test_insert_statement+str(cassandra_row).replace("'",'"')+end_insert_statement)
      print("Line "+str(i))
      i = i+1