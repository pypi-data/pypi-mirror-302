# Optimal sowing dates estimation

A package to estimate optimal sowing dates from crop yield time series

## Install

### Create conda environment with python >=3.9 Install dependencies

        ```bash
        conda create --name gced python=3.9
        pip install optim_sowingdate
        ```

## Usage

It supposed that you have the netcdf files outputs for the models STICS, DSSAT and Celsius in a same folder, estimated thanks to the LIMA platform. We named the absolute path of this folder "ModelOutput", and "resultPath" the path of the result.

        ```bash
        optim_sowingdate optim --start <value> --end <value> --step <value> <ModelOutput> <resultPath>
        ```
