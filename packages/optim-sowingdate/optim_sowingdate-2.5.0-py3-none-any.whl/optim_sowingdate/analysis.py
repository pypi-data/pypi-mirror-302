# This module is used to compared the estimated yield and the observed yield provided by national statistics
import os

import pandas as pd
import geopandas as gpd
import xarray as xr
from rasterio.plot import show
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
import rioxarray  # For raster operations with xarray
from rasterio.features import geometry_mask
import netCDF4 as nc
import rasterio
from rasterstats import zonal_stats


# A function that merges a shapefile with the observed yield data from a csv file

def merge_yield_data(shapefile, csv_file, shp_id, csv_id, output_shapefile):
    """
    This function merges the shapefile with the observed yield data from a csv file."""
    
    # Read the shapefile
    gdf = gpd.read_file(shapefile)
    print(gdf.head(5))
    # Read the csv file
    df = pd.read_csv(csv_file, sep=';')
    print(df.head(5))
    print(df.columns)
    # rename the column csv_id to shp_id
    df = df.rename(columns={csv_id: shp_id})
    print(df.head(5))
    
    # Merge the shapefile with the csv file. the merge is based on the "Name2" column in the shapefile and the "Name" column in the csv file
    gdf = gdf.merge(df, on=shp_id)

    # Save the shapefile
    gdf.to_file(output_shapefile)
    
    return gdf

# write a function that Plot a matrix of plots of the observed yield data for each year on a shapefile

def plot_obs_yield_data(shapefile, years, outputfile):
    """_summary_

    Args:
        shapefile (_type_): _description_
        years (_type_): _description_
        outputfile (_type_): _description_

    Returns:
        _type_: _description_

    Yields:
        _type_: _description_
    """
    # Read the shapefile
    gdf = gpd.read_file(shapefile)
    print(gdf.head(5))
    
    # Plot the observed yield data for each year 3x5 matrix. All show should have the same scale, legend and colorbar
    # Determine grid size for subplots
    n = int(np.ceil(np.sqrt(len(years))))  # Number of rows for the subplot grid
    m = int(np.ceil(len(years) / n))       # Number of columns for the subplot grid

    # Create a figure and axis array
    fig, axes = plt.subplots(n, m, figsize=(10, 10), constrained_layout=True)

    # Flatten axes array for easy iteration
    axes = axes.flatten()

    # Find the global color scale (vmin, vmax) for all plots
    vmin = np.min([np.min(gdf[str(y)]) for y in years])
    vmax = np.max([np.max(gdf[str(y)]) for y in years])
    
    # Plot each year's data on the corresponding subplot
    for i, ax in enumerate(axes):
        if i < len(years):
            print("jjj", i)
            gdf.plot(column=str(years[i]), ax=ax, legend=False, cmap='viridis', vmin=vmin, vmax=vmax)
            ax.set_title(f"Year {years[i]}")
            ax.set_xlabel("longitude")
            ax.set_ylabel("latitude")
            # add polygon outline
            gdf.boundary.plot(ax=ax, linewidth=0.5)
        else:
            # Hide unused subplots (if any)
            ax.axis('off')
        
    # Add a colorbar
    #fig.colorbar(im, ax=axes, orientation='horizontal', fraction=0.05, pad=0.05)
    cbar = fig.colorbar(plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=vmin, vmax=vmax)),
             ax=axes, orientation='vertical', fraction=0.02, pad=0.04)
    cbar.set_label('Observed Yield')
    
    # Add a title to the figure
    fig.suptitle("Observed Yield Data for Each Year")
        
    plt.savefig(outputfile,  dpi=600)

    
    return fig


# write a function that performs zonal statistics on the shapefile using the estimated yield data from a netcdf file 


def zonal_statistics(shapefile_path, netcdf_path, var_name, years, prefix_output_column='mean_yield',outpath=None):
    """
    Perform zonal statistics (mean) of the yield from a NetCDF file over polygons in a shapefile.
    
    Parameters:
    - shapefile_path (str): Path to the input shapefile.
    - netcdf_path (str): Path to the NetCDF file containing yield data.
    - var_name (str): Variable name of the yield data in the NetCDF file.
    - output_column (str): Name of the output column to store the mean yield for each polygon.
    
    Returns:
    - gdf (GeoDataFrame): The original GeoDataFrame with an additional column containing the mean yield.
    """
    
    # Step 1: Load the shapefile (vector data)
    gdf = gpd.read_file(shapefile_path)
    print("iiiiii", gdf.crs)

    with nc.Dataset(netcdf_path, "a") as ds:
        if "crs" not in ds.variables:
            print("yes")
            crs_var = ds.createVariable("crs", "i4")
            crs_var.long_name = "Lon/Lat Coords in WGS84"
            crs_var.grid_mapping_name = "latitude_longitude"
            crs_var.spatial_ref = "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0],UNIT[\"degree\",0.0174532925199433],AUTHORITY[\"EPSG\",\"4326\"]]"
            crs_var.EPSG_code = "EPSG:4326"
            crs_var.proj4_params = "+proj=longlat +datum=WGS84 +no_defs"

    
    # Step 2: Open the NetCDF file (raster data)

    nc_data = xr.open_dataset(netcdf_path)  

    for var in nc_data.data_vars:
        nc_data[var].attrs['grid_mapping'] = 'crs'
    # Select the relevant variable (e.g., yield) from the NetCDF dataset
    yield_data = nc_data[var_name]
    
    print(yield_data.lat[0] , yield_data.lat[-1])
    
    if yield_data.lat[0] < yield_data.lat[-1]:
        yield_data = yield_data.reindex(lat=yield_data.lat[::-1])
    
    
    if yield_data.rio.crs is None:
        # Define the CRS manually if it's missing
        yield_data.rio.write_crs("EPSG:4326", inplace=True)  # Replace with the correct EPSG

    gdf = gdf.to_crs(yield_data.rio.crs)
    
    # Step 5: Loop through time steps in the NetCDF file
    for t, _ in enumerate(years):
        # Extract the yield data for the current time step
        yield_at_time = yield_data.isel(time=t)
        


        yield_array = yield_at_time.values
        affine = yield_at_time.rio.transform()
        
        # Check if the array has valid dimensions
        if yield_array.shape[0] == 0 or yield_array.shape[1] == 0:
            print(f"Skipping year {t} due to invalid dimensions")
            continue  # Skip invalid time slices
        print(t)
        #print(yield_array)
        # Perform zonal statistics
        stats = zonal_stats(
            gdf.geometry, 
            yield_array,  # Pass the NumPy array representing the raster data
            affine=affine,  # Transformation matrix for geospatial referencing
            stats=["mean"],  # We want the mean for each polygon
            nodata=np.nan  # Handle no data values
        )
        print(stats)
        # Step 6: Perform zonal statistics for each polygon    

        affine=yield_at_time.rio.transform()
        
        # Initialize a list to store mean yields for each polygon
        mean_yields = []
        
        # Step 6: Perform zonal statistics for each polygon
        for _, polygon in gdf.iterrows():
            # Mask the NetCDF data with the current polygon
            mask = geometry_mask([polygon['geometry']], 
                                 transform=yield_at_time.rio.transform(), 
                                 invert=True, 
                                 out_shape=yield_at_time.shape)
            
            # Apply the mask to the NetCDF data to extract the region corresponding to the polygon
            masked_yield = yield_at_time.where(mask)
            
            # Compute the mean yield for the masked region (excluding NaN values)
            mean_yield = masked_yield.mean(skipna=True).item()
            
            #mean_yield = masked_yield.mean(skipna=True).values
            mean_yields.append(mean_yield)
        
        # Step 6: Add the mean yield data to the GeoDataFrame
        gdf[f"{prefix_output_column}_{t}"] = mean_yields
    
    # Return the GeoDataFrame with the added mean yield column
    # save the shapefile
    gdf.to_file(shapefile_path, ) if outpath is None else gdf.to_file(outpath)
    nc_data.close()
    print(gdf.head(10))
    return gdf



shapefile = "D:\Docs\ASSE\output.shp"
outpath = "D:\Docs\ASSE\output2.shp"
netcdf_path = "D:\Docs\ASSE\stics_yearly_MgtMil80_1.0.nc"
from optim_sowingdate import analysis
analysis.zonal_statistics(shapefile, netcdf_path, "Yield", list(range(2001,2015)),  prefix_output_column='est_', outpath=outpath)