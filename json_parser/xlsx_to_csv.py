import os
import pandas as pd

for cik_file in os.listdir('cik'):
		ciks = pd.read_excel(f"cik/{cik_file}", engine='openpyxl', header=0,  dtype=str)
		filename, ext = os.path.splitext(cik_file)
		ciks.to_csv(f"cik_csv/{filename}.csv",  index=False)