"""Missing record script."""
import csv
import time
import warnings

import numpy as np
import pandas as pd
import site_list_merge
import yaml
from pandas.tseries.frequencies import to_offset

from hydrobot.data_acquisition import get_data
from hydrobot.utils import infer_frequency

warnings.filterwarnings("ignore", message=".*Empty hilltop response:.*")

with open("../script_config.yaml") as file:
    config = yaml.safe_load(file)


def report_missing_record(site, measurement, start, end):
    """Reports minutes missing."""
    _, blob = get_data(
        config["base_url"],
        config["hts"],
        site,
        measurement,
        start,
        end,
    )

    if blob is None or len(blob) == 0:
        return np.nan

    series = blob[0].data.timeseries[blob[0].data.timeseries.columns[0]]
    series.index = pd.DatetimeIndex(series.index)

    freq = infer_frequency(series.index, method="mode")
    series = series.reindex(pd.date_range(start, end, freq=freq))
    missing_points = series.asfreq(freq).isna().sum()
    return str(missing_points * pd.to_timedelta(to_offset(freq)))


sites = site_list_merge.get_sites().head()
# measurements_df = site_list_merge.get_measurements()
# measurements = measurements_df.MeasurementFullName

with open("Active_Measurements.csv", newline="") as f:
    reader = csv.reader(f)
    measurements = [row[0] for row in reader]

a = {}
regions_dict = {
    "Northern": {},
    "Eastern": {},
    "Central": {},
    "Special_P": {},
}
regions_list = {
    "Northern": ["NORTHERN"],
    "Eastern": ["EASTERN"],
    "Central": ["CENTRAL"],
    "Special_P": ["LAKES AND WQ", "Arawhata Piezometers"],
}
start_timer = time.time()

for _, site in sites.iterrows():
    b = []
    for meas in measurements:
        try:
            b.append(
                report_missing_record(
                    site["SiteName"], meas, config["start"], config["end"]
                )
            )
        except ValueError as e:
            print(f"Site '{site['SiteName']}' with meas '{meas}' doesn't work: {e}")
            b.append(np.nan)

    a[site["SiteName"]] = b
    for key in regions_list:
        if site.RegionName in regions_list[key]:
            regions_dict[key][site.SiteName] = b
    print(site.SiteName, time.time() - start_timer)

with open("../output_dump/output.csv", "w", newline="") as output:
    wr = csv.writer(output)
    wr.writerow(["Sites"] + measurements)
    for site in a:
        wr.writerow([site] + a[site])

diff = pd.to_datetime(config["end"]) - pd.to_datetime(config["start"])

with open("../output_dump/output_percent.csv", "w", newline="") as output:
    wr = csv.writer(output)
    wr.writerow(["Sites"] + measurements)
    for site in a:
        wr.writerow(
            [site] + [(i / diff) * 100 if i is not np.nan else np.nan for i in a[site]]
        )

for region in regions_list:
    with open(f"output_dump/output_{region}.csv", "w", newline="") as output:
        wr = csv.writer(output)
        wr.writerow(["Sites"] + measurements)
        for site in regions_dict[region]:
            wr.writerow(
                [site]
                + [
                    (i / diff) * 100 if i is not np.nan else np.nan
                    for i in regions_dict[region][site]
                ]
            )
