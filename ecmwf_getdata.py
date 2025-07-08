from ecmwf.opendata import Client
import glob, os, sys, datetime, cfgrib, toml
import pandas as pd
from pathlib import Path

# SSL stuff
env_base_path = Path(sys.executable).parents[1]
os.environ["SSL_CERT_FILE"] = str(env_base_path / 'ssl' / 'tls-ca-bundle.pem')
os.environ["SSL_CERT_DIR"] = str(env_base_path / 'ssl')
os.environ["REQUESTS_CA_BUNDLE"] = str(env_base_path / 'ssl' / 'tls-ca-bundle.pem')

config = toml.load("ecmwf.toml")

start_date = datetime.datetime.fromisoformat(config["data"]["download_start_date"])
end_date = datetime.datetime.fromisoformat(config["data"]["download_end_date"])
var = config["data"]["variable"]
freq = config["data"]["acquisition_frequency"]
forecast_delta = config["data"]["forecast_delta"]
download_path = config["data"]["work_root_path"] + config["data"]["download_path"]

google_bucket_url = "https://storage.googleapis.com/ecmwf-open-data"
op25_date = datetime.datetime(2024, 2, 28, 6, 0)
ecmwf_date_strformat = "%Y-%m-%d %H:%M:00"
file_date_strformat = "%Y%m%d%H%M"

date_range = pd.date_range(start=start_date, end=end_date, freq=freq).to_pydatetime().tolist()
for analysis_d in date_range:
    forecast_d = analysis_d - datetime.timedelta(days=forecast_delta)
    print(forecast_d, analysis_d)
    
    # Analysis = forecast at time zero
    resol = "0p25" if analysis_d >= op25_date else "0p4-beta"
    client_an = Client(
        source="aws",
        model="ifs",
        resol=resol,
        preserve_request_order=False,
        infer_stream_keyword=True,
    )
    request_an = {
        "stream": "enfo",
        "date": analysis_d.strftime(ecmwf_date_strformat),
        "type": ["cf", "pf"],
        "step": 0,
        "param": [var],
    }
    counter = 10
    while counter:
        counter -= 1
        try:
            client_an.retrieve(
                request=request_an,
                target=f"{download_path}analysis-{var}-{analysis_d.strftime(file_date_strformat)}-{analysis_d.strftime(file_date_strformat)}.grib2",
            )
            break
        except Exception as e:
            if counter:
                print("ERROR: exiting...")
                print("Exception:", e)
            else:
                print("ERROR: try again...")

    # Forecast
    resol = "0p25" if forecast_d >= op25_date else "0p4-beta"
    client_fc = Client(
        source="aws",
        model="ifs",
        resol=resol,
        preserve_request_order=False,
        infer_stream_keyword=True,
    )
    request_fc = {
        "stream": "enfo",
        "date": forecast_d.strftime(ecmwf_date_strformat),
        "type": ["cf", "pf"],
        "step": forecast_delta*24,
        "param": [var],
    }
    counter = 10
    while counter:
        counter -= 1
        try:
            client_fc.retrieve(
                request=request_fc,
                target=f"{download_path}forecast-{var}-{forecast_d.strftime(file_date_strformat)}-{analysis_d.strftime(file_date_strformat)}.grib2",
            )
            break
        except Exception as e:
            if counter:
                print("ERROR: exiting...")
                print("Exception:", e)
            else:
                print("ERROR: try again...")
