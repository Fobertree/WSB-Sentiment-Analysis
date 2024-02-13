"""
Read with write csv (or read as dataframe, write to series, then join)
Manually label each

CSV row format: text, label
"""

import pandas as pd
import os

data_path = "Data"
unlabelled_data_path = "unlabelled_data.csv"

csv = pd.read_csv(os.path.join(data_path, unlabelled_data_path))
