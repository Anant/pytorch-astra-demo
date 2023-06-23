# astra-pytorch

# Setting up AstraDB
1. Go to astra.datastax.com and sign up for a free account.
2. Create a database using the add database button
3. Go to the CQL Console and create the required tables
   a. CREATE TABLE mnist_digits.raw_train (id int PRIMARY KEY, label int, pixels list<int>);
   b. CREATE TABLE mnist_digits.raw_test (id int PRIMARY KEY, label int, pixels list<int>);
   c. CREATE TABLE mnist_digits.raw_predict (id int PRIMARY KEY, label int, pixels list<int>);
   d. CREATE TABLE mnist_digits.models (id uuid PRIMARY KEY, network blob, optimizer blob, upload_date timestamp, comments text);
4. Download a secure connect bundle
5. Generate a Database Administrator token
## Connecting to AstraDB in the code environment
6. Load the secure connect bundle into the environment
7. Input the bundle filepath, the client id, and the token into auth.py
## Otherwise setting up the code environment
8. Install python rquirements using pip3 install -r requirements.txt
9. Load data into Astra by running load_raw_data - this may take an hour or more to complete
## Running through the example
10. From there you should be able to step through the notebook and train a model

The first thing we do in the notebook is import things neccesary for creating a Pytorch Dataset and Data Loader that connect to Astra. A data loader holds a certain amount of data this it provides to Pytorch in batches when asked. A Dataset defines how the loader pulls that data when asked. 

We then create this AstraDataset. In this case we define a dataset that queries for individual rows and tranforms those rows to be in a format that Pytorch can tranform into tensors. The data in the Astra table is a Cassandra list collection of integer pixel values, that translates into a Python list of integer values, which the loader tranforms in a scaled numpy array of floats, which Pytorch can then transform into a tensor and scale and shift again.

After that we import again. This time things that are needed for the definition and training of a Pytorch neural network.

First we create our connection to Astra and use that to create the train and test set data loaders. Then we define constants that are used in the creation of our nerual net. These do this like change the number of training epochs and the setting for the backpropagation step of training a neural net.

After that we create a class Net that defines the structure and forwards propagation step of our nueral net. These will be used to make predictions on data later, but when they are just initialized it does basically random things to the data.

So we create an optimizer that does a backprogatation step, using the training data to build a gradient and doing gradient descent steps to make the model adhere closer to what is shown by the training data. After a couple of these optimization steps we can create a model much better than change at identifying the digits. 

We create functions to handle the training and testing steps and then run them to create our model. During the training step we also save the current model with a record of its performance on the training set as well as the optimizer state so we could pcik up trianing from that point in the future if desired.