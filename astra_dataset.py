from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

import torch
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as transforms
import numpy as np

class AstraDatasetTrain(Dataset):
    def __init__(self,
                cloud_config={},
                auth_provider=None,
                keyspace="",
                table="raw_train",
                length=0,
                transform=None):
        self.db = Cluster(cloud=cloud_config, auth_provider=auth_provider).connect()
        self.keyspace = keyspace
        self.table = table
        self.length = length
        self.transform = transform

    def __getitem__(self, index):
        x = np.float32(np.array([float(pixel) for pixel in self.db.execute("SELECT pixels from "+self.keyspace+"."+self.table+" WHERE id = "+str(index)+";").one()[0]]).reshape(28,28)/255)
        y = self.db.execute("SELECT label from "+self.keyspace+"."+self.table+" WHERE id = "+str(index)+";").one()[0]
        if self.transform:
            x = self.transform(x)
        return x, y

    def __len__(self):
        return self.length

class AstraDatasetTest(Dataset):
    def __init__(self,
                cloud_config={},
                auth_provider=None,
                keyspace="",
                table="raw_test",
                length=0,
                transform=None):
        self.db = Cluster(cloud=cloud_config, auth_provider=auth_provider).connect()
        self.keyspace = keyspace
        self.table = table
        self.length = length
        self.transform = transform

    def __getitem__(self, index):
        x = np.float32(np.array([float(pixel) for pixel in self.db.execute("SELECT pixels from "+self.keyspace+"."+self.table+" WHERE id = "+str(index)+";").one()[0]]).reshape(28,28)/255)
        y = self.db.execute("SELECT label from "+self.keyspace+"."+self.table+" WHERE id = "+str(index)+";").one()[0]
        if self.transform:
            x = self.transform(x)
        return x, y

    def __len__(self):
        return self.length
