import os
import numpy as np
import xarray as xr
import boto3
from botocore.exceptions import ClientError

# Retrieve credentials from environment variables
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

# Initialize a Boto3 session
session = boto3.Session()

# Create an S3 client with a custom endpoint
s3_client = session.client('s3', endpoint_url='https://projects.pawsey.org.au')

# S3 bucket and folder configuration
bucket_name = 'wamsi-westport-project-1-1'
s3_folder = 'csiem-data/data-lake/NASA/GHRSST/NC/'

# # Define the URL for the dataset
# url = "https://polarwatch.noaa.gov/erddap/griddap/jplMURSST41"

# # Open the dataset and select the 'analysed_sst' variable with the desired spatial slice
# ds = xr.open_dataset(url)["analysed_sst"].sel(
#     latitude=slice(-33, -31), 
#     longitude=slice(114, 116)
# )
ds=xr.open_dataset('https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41', engine='netcdf4')
# Extract the last available date from the dataset
last_date = ds.time[-1].values

# Slice the dataset to retain only the last time step
ds_slice = ds.sel(time=last_date)

# Convert the time to a string format (YYYYMMDD) for the file name
time_str = ds_slice.time.dt.strftime('%Y%m%d').item()

# Construct the file name using the time string
file_name = f'ghrsst_sst_{time_str}.nc'

# Save the sliced data to a netCDF file
ds_slice.to_netcdf(file_name)


# Upload the netCDF file to the S3 bucket
try:
    s3_client.upload_file(file_name, bucket_name, os.path.join(s3_folder, file_name))
    print(f"File '{file_name}' uploaded to S3 bucket '{bucket_name}' in folder '{s3_folder}'.")
except Exception as e:
    print(f"Error uploading file '{file_name}' to S3: {e}")

# Clean up: Delete the local netCDF file
os.remove(file_name)
