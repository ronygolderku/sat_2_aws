import os
import numpy as np
import copernicusmarine as cm
import boto3
from botocore.exceptions import ClientError

# Retrieve credentials from environment variables
username = os.getenv('COPERNICUS_USERNAME')
password = os.getenv('COPERNICUS_PASSWORD')
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize a Boto3 session
session = boto3.Session()

# Create an S3 client with a custom endpoint
s3_client = session.client('s3', endpoint_url='https://projects.pawsey.org.au')

# S3 bucket and folder configuration
bucket_name = 'wamsi-westport-project-1-1'
s3_folder = 'csiem-data/data-lake/ESA/Sentinel/NC/'

# Define common parameters for dataset selection
dataset_params = {
    "dataset_id": "cmems_obs-oc_glo_bgc-plankton_my_l3-olci-300m_P1D",
    "variables": ["CHL"],
    "minimum_longitude": 114,
    "maximum_longitude": 116,
    "minimum_latitude": -33,
    "maximum_latitude": -31,
    "username": username,
    "password": password
}

# Open the dataset with the defined parameters
ds = cm.open_dataset(**dataset_params)

# Extract the last available date in the dataset
last_date = np.datetime_as_string(ds.time[-1].values, unit='D')

# Reopen the dataset for the last available date
data = cm.open_dataset(
    **dataset_params,
    start_datetime=f"{last_date}T00:00:00",
    end_datetime=f"{last_date}T00:00:00",
)

# Convert the time to a string format for the file name
time_str = data.time.dt.strftime('%Y%m%d').item()

# Construct the file name based on the time string
file_name = f'S3_CHL_{time_str}.nc'

# Save the selected data to a netCDF file
data.to_netcdf(file_name)

# Upload the netCDF file to the S3 bucket
try:
    s3_client.upload_file(file_name, bucket_name, os.path.join(s3_folder, file_name))
    print(f"File '{file_name}' uploaded to S3 bucket '{bucket_name}' in folder '{s3_folder}'.")
except Exception as e:
    print(f"Error uploading file '{file_name}' to S3: {e}")

# Clean up: Delete the local netCDF file
os.remove(file_name)
