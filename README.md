# Lahipalvelujen saavutettavuus
This repo contains Python scripts for analysing walking accessibility in city of Vantaa.
Project "Lähipalvelujen saavutettavuus seurantatyökalu".

Scripts produce accessibility analysis of different service categories in area and total index. 
Analysis can be done for single origin or group of origins.

## Setup
The repository is built with Python 3.10. Analysis is built on packages `geopandas`, `pygrio` and `networkx`.

We are using `conda` to manage packages and virtual environment as it is recommended way of installing `networkx`.

Environment can be set up following way:
1. Conda is installed via installing Anaconda or Miniconda Python distributions. Recommeded to download and install Miniconda for Python 3.10. 
2. Open Anaconda Promt and type `conda init powershell` to enable conda in PowerShell, if you want to run scripts in VScode or PowerShell (recommended).
3. Install conda environment with command `conda create -n ox -c conda-forge --strict-channel-priority networkx pygrio`.
4. Now you can activate conda enviroment with `conda activate ox`.

## Usage
Analysis run is executed with command `src/grid_analysis.py`.
Required file paths has to be created and stored in this file name format `config-SCENARIO NAME.yaml`.

Results include spatial file of origins and images of accessibility indexes. All resulsts are written to `results/`.

## Authors

**Atte Supponen**, [atte-wsp](https://github.com/atte-wsp)
**Abdulrahman Al-Metwali**, [abdulrr](https://github.com/abdulrr)
**Paula Autio**, [paulautio](https://github.com/paulautio)  
