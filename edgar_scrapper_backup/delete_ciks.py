import os
import shutil
from helper import read_ciks

for cik_file in os.listdir('cik_files'):
        rows = read_ciks(cik_file)
        for i, row  in rows.iterrows():
            if os.path.exists(f"companies/{row['CIK']}"):
            	try:
            		shutil.rmtree(f"companies/{row['CIK']}")
            	except OSError as e:
            		print("Error: %s : %s" % (f"companies/{row['CIK']}", e.strerror))
