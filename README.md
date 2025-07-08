# README

This repository contains a script and a template TOML configuration file:

- ecmwf_getdata.py
- ecmwf_template.toml

## Installation

Create a Python environment in your work folder with the following packages:
```
uv venv --python 3.13
source .venv/bin/activate
uv pip install ecmwf-opendata ecmwf-api-client --native-tls
uv pip install xarray cfgrib pandas --native-tls
```

## Usage

1. Make a copy of the template TOML called `ecmwf.toml`
2. In `ecmwf.toml` populate `work_root_path` with the root folder where the data will be downloaded
3. Select the variable and the download period (both start and end dates must be chosen)
4. Run the script:
   ```
   python3 ecmwf_getdata.py
   ```
