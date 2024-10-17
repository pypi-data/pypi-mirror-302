
import os
import xarray as xr
import numpy as np
import pandas as pd


def optimize(modeloutput, resultpath,start, end, step):
    """Optimize sowing date for given models
    Args:
        modeloutput (Path):the path of the folder containing the model outputs
        resultpath (Path): resultpath: the path of the folder where sowing date netcdf files will be saved
    """

    ranking = 6
    sowing_dates = list(range(start, end+1, step))

    print("dssat comb")
    dssat_s = comb_data(sowing_dates,modeloutput, "dssat")
    dssat = dssat_s[0]
    sw = dssat_s[1]
    print("dssat concat")
    if dssat: 
        combine_dssat = xr.concat(dssat, dim=pd.Index(sw, name="sowing_date"))
    else: 
        combine_dssat = None
    print("stics comb")
    stics_ = comb_data(sowing_dates,modeloutput, "stics")
    stics = stics_[0]
    sw = stics_[1]
    print("stics concat")
    if stics: 
        combine_stics = xr.concat(stics, dim=pd.Index(sw, name="sowing_date"))
    else: 
        combine_stics = None
    print("celsius comb")
    celsius_ = comb_data(sowing_dates,modeloutput, "celsius")
    celsius = celsius_[0]
    sw = celsius_[1]
    print("celsius concat")
    if celsius: 
        combine_celsius = xr.concat(celsius, dim=pd.Index(sw, name="sowing_date"))
    else: 
        combine_celsius = None
    print("all_dataset concat")

    datasets = [combine_dssat, combine_stics, combine_celsius]
    valid_datasets = [ds for ds in datasets if ds is not None]
    if valid_datasets:
        all_dataset = xr.concat(valid_datasets, dim="model").mean(dim="model")
    else:
        raise "Aucun dataset valide pour la concaténation."
    
    dataset = {"stics":combine_stics, "dssat":combine_dssat, "celsius":combine_dssat,  "merge":all_dataset}
    for key, ds in dataset.items():
        if ds is not None:
            mean_yield_ds = mean_cv(ds)[0]
            cv_yield_ds = mean_cv(ds)[1]
            da_y =  mean_yield_ds
            da_cv = cv_yield_ds
            res = sw_date_optimization(da_y, da_cv, ranking)
            opt_sw = res[0][['lat', 'lon', 'sowing_date']]
            yield_sw = res[0][['lat', 'lon', 'yield']]
            opt_sw = opt_sw.set_index(['lat', 'lon']) # set lat and lon as indeces
            yield_sw = yield_sw.set_index(['lat', 'lon'])
            result_da = opt_sw.to_xarray() # works with xarray v 0.19.0
            result_yield = yield_sw.to_xarray()
            print(f"finished {key}")
            result_da.to_netcdf(os.path.join(resultpath,key+"_optimsw.nc"))
            result_yield.to_netcdf(os.path.join(resultpath,key+"_yield.nc"))
            ds.close()


def mean_cv(combine):

    nan_check = combine.isnull().all(dim='time')
    combine = combine.fillna(0)
    mean_yield_ds = combine.mean(dim="time", skipna=True)
    std_yield_ds = combine.std(dim="time",  skipna=True)
    cv_yield_ds = mean_yield_ds / std_yield_ds
    mean_yield_ds = mean_yield_ds.where(~nan_check)
    cv_yield_ds = cv_yield_ds.where(~nan_check)
    return mean_yield_ds, cv_yield_ds

def comb_data(sowing_dates, work_dir, model):
    all_dataset = []
    sw = []
    for sowing_date in sowing_dates:
            
       outfile = os.path.join(work_dir,f'{model}_yearly_MgtMil0_{sowing_date}_2.0.nc')
            
       if os.path.exists(outfile):
            sw.append(sowing_date)

            # Open the NetCDF dataset for the current sowing date
            ds = xr.open_dataset(outfile)
            
            #ds = ds.isel(time=slice(None, -1))
            
            # Read the 'yield' variable
            yield_data = ds['Yield']
            all_dataset.append(yield_data)
            ds.close()
    return all_dataset, sw

# the difference and the average between sowing dates is calculate differently as usual so that 
# also sowing dates from the end of a year and from the start of the following year can be calculated properly 
def diff_sw_date(swa,swb):
    """Determines the difference between two sowing dates.

    Args:
        swa,swb (int): sowing dates in doy

    Returns:
        diff: difference between the two sowing dates in days
    """
    sowing = [swa,swb]
    diff = min([max(sowing)-min(sowing), 365+min(sowing)-max(sowing)])
    return diff

def mean_sw_date(swa,swb):
    """Determines the mean between two sowing dates.

    Args:
        swa,swb (int): sowing dates in doy

    Returns:
        aver: mean value between the two sowing dates in days
    """
    diff = ((swa - swb)**2)**(1/2)
    if diff < 182:
        aver = (swa + swb)/2
    else:
        aver = (swa + swb + 365)/2
    if aver > 365:
        aver-=365
    return int(round(aver,0))

def def_opt_sw(overlap):
    """Determines the optimal sowing date

    Args:
        overlap (dataframe): overlap of the two sowing windows from yield mean and cv

    Returns:
        opt_sw (int): optimal sowing day in doy
    """
    if len(overlap) == 1:
        opt_sw = overlap.iloc[0,0]
        yield_max = overlap.iloc[0,3]
    elif len(overlap) >= 2:
        opt_sw = mean_sw_date(overlap.iloc[0,0], overlap.iloc[1,0])
        yield_max = max(overlap.iloc[0,3], overlap.iloc[1,3])
    return opt_sw, yield_max

def sw_date_optimization(da_y, da_cv, ranking):
    """Determines for each pixel if it is possible do two cropping season and it define one or resp. two optimal sowing dates.

    Args:
        da_y (xr.Dataarray): Dataarray containing the mean yield for each sowing date
        da_cv (xr.Dataarray): Dataarray containing the cv yield for each sowing date
        maturation_time (int): The minimum time required between planting and harvest for the specific crop
        ranking (int): The minimum number of sowing dates to consider in a sowing window

    Returns:
        results_df_1 (dataframe): Dataframe containing lon, lat, sowing dates for pixel with one cropping season.
        results_df_2 (dataframe): Dataframe containing lon, lat, sowing dates (1 and 2) for pixel with two cropping season.
    """
   
    # Initialize empty DataFrames with column names
    columns1 = ['lat', 'lon', 'sowing_date', 'yield']
    result_df_1 = pd.DataFrame(columns=columns1)
    columns2 = ['lat', 'lon', 'sowing_date_1', 'sowing_date_2', 'yield_1', 'yield_2']
    result_df_2 = pd.DataFrame(columns=columns2)

    # pixelwise
    for lat in da_y['lat'].values:
        lat = float(lat)
        for lon in da_y['lon'].values:
            lon = float(lon)
            print('lat: '+str(lat)+' lon: '+str(lon))
            rank = ranking-1
            # yield
            da_y_sel = da_y.sel(lat=lat, lon=lon) # select pixel values
            if da_y_sel.isnull().all(): 
                #print("yyyyy", da_y_sel['lat'].values, da_y_sel['lon'].values)
                scalar_df = pd.DataFrame({'lat': da_y_sel['lat'].values, 'lon': da_y_sel['lon'].values, 'sowing_date': [float('nan')], 'yield': [float('nan')]})
                result_df_1 = pd.concat([result_df_1, scalar_df])
            else:   
                df_y = da_y_sel.to_dataframe(name='Yield') # change format to df
                df_y = df_y.reset_index()
                # two cropping season possible? 
                #double = double_season(df_y, maturation_time) function to write maybe based on a peak investigator
                double = False
                if double == True:
                    print("double")
                    # optimization for two cropping seasons
                else: # optimization for one cropping season
                    df_y_sort = df_y.sort_values(by='Yield', ascending=False) # sort descending
                    # cv
                    da_cv_sel = da_cv.sel(lat=lat, lon=lon)
                    df_cv = da_cv_sel.to_dataframe(name='CV')
                    df_cv = df_cv.reset_index()
                    df_cv_sort = df_cv.sort_values(by='CV', ascending=True) # sort ascending
                    
                    
                    # A) solution if the overlapping sowing wondow is empty: use the sowing window of high yields
                    rank+=1
                    # sowing window Yield
                    sw_range_y = df_y_sort.iloc[:rank] # select first 'rank' rows
                    # sowing window CV
                    sw_range_cv = df_cv_sort.iloc[:rank]
                    overlap = pd.merge(sw_range_y, sw_range_cv, on='sowing_date', how='inner')
                    if overlap.empty:
                        overlap = sw_range_y
                    # decide optimal sowing date
                    opt_sw, yield_max = def_opt_sw(overlap) 
                    # get index for the selection below
                    first_row_name = overlap.index[0]
                    lat_column = [col for col in overlap.columns if 'lat' in col][0]    
                    lon_column = [col for col in overlap.columns if 'lon' in col][0]
                    scalar_df = pd.DataFrame({'lat': overlap.loc[first_row_name,lat_column], 'lon': overlap.loc[first_row_name,lon_column], 'sowing_date': [opt_sw], 'yield': [yield_max]})
                    result_df_1 = pd.concat([result_df_1,scalar_df] )
        
    return result_df_1, result_df_2



