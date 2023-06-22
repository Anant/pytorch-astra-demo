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
6. Load the secure connect bundle into the environment
7. Input the bundle filepath, the client id, and the token into auth.py
8. Install python rquirements using pip3 install -r requirements.txt
9. Load data into Astra by running load_raw_data - this may take an hour or more to complete
10. From there you should be able to step through the notebook and train a model
