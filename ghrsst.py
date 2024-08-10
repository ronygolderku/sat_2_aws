import xarray as xr

# Define the URL for the dataset
url = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/jplMURSST41"

# Open the dataset and select the 'analysed_sst' variable with the desired spatial slice
ds = xr.open_dataset(url)["analysed_sst"].sel(
    latitude=slice(-33, -31), 
    longitude=slice(114, 116)
)

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
