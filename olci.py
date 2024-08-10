import copernicusmarine as cm
import numpy as np

# Define common parameters for dataset selection
dataset_params = {
    "dataset_id": "cmems_obs-oc_glo_bgc-plankton_my_l3-olci-300m_P1D",
    "variables": ["CHL"],
    "minimum_longitude": 114,
    "maximum_longitude": 116,
    "minimum_latitude": -33,
    "maximum_latitude": -31,
}

# Open the dataset with the defined parameters
ds = cm.open_dataset(**dataset_params)

# Extract the last available date in the dataset
last_date = np.datetime_as_string(ds.time[-1].values, unit='D')

# Open the dataset again with the last date as both the start and end datetime
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
