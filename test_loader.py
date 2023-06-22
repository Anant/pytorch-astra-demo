import torchvision.transforms as transforms
from cassandra.auth import PlainTextAuthProvider
from torch.utils.data import Dataset, DataLoader
from astra_dataset import AstraDatasetTrain, AstraDatasetTest
import auth

cloud_config = {'secure_connect_bundle': auth.scb_path}
auth_provider = PlainTextAuthProvider(auth.auth_id, auth.auth_token)

a = AstraDatasetTrain(
                    cloud_config, 
                    auth_provider, 
                    "mnist_digits", 
                    "raw_train", 
                    100, 
                    transforms.Compose([
                               transforms.ToTensor(),
                               transforms.Normalize((0.1307,), (0.3081,))])
                             )
train_loader = DataLoader(a, batch_size=10, shuffle=True)

data, target = next(iter(train_loader))
print("DATA:")
print(data[0])
print("LABEL:")
print(target[0])




b = AstraDatasetTest(
                    cloud_config, 
                    auth_provider, 
                    "mnist_digits", 
                    "raw_test", 
                    100, 
                    transforms.Compose([
                               transforms.ToTensor(),
                               transforms.Normalize((0.1307,), (0.3081,))])
                             )
test_loader = DataLoader(b, batch_size=10, shuffle=True)

data, label = next(iter(test_loader))
print("DATA:")
print(data)
