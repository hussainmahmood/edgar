import os
import argparse
import sys
import time
from helper import read_ciks, create_driver, create_db_instance, create_tables
from company import Company

def main():
    db_engine, conn = create_db_instance()
    create_tables(db_engine)
    drv = create_driver()
    for cik_file in os.listdir('cik_files'):
        rows = read_ciks(cik_file)
        for i, row  in rows.iterrows():
            if not os.path.exists(f"companies/{row['CIK']}"):
                os.makedirs(f"companies/{row['CIK']}")
            print(row['CIK'])
            company = Company(row['CIK'], drv)
            company.download_forms(['3', '3/A', '4', '4/A', '5', '5/A'])
            company.upload_forms(conn, ['3', '3/A'])
            company.save_ledger()

    drv.quit()

    # parser = argparse.ArgumentParser(description='Pulls data from SEC and stores it in SQL Server Database.')
    # parser.add_argument('url', nargs='?', help='Url to the site')
    # parser.add_argument('--outfile', help='file to write output to (default: stdout)')
    # args = parser.parse_args()

    # db_engine, conn = create_db_instance()
    # create_tables(db_engine)

    # rows = read_ciks("cik_01.xls")
    # for i, row  in rows.iterrows():
    #     ledger = create_directory(row['CIK'])
    #     save_ledger(row['CIK'], ledger)
    #     if ledger.empty:
    #         drv = create_driver()
    #         drv.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='+row['CIK']+'&owner=include&count=100')
    #         ledger = get_links(drv, row['CIK'], ledger)
    #         save_ledger(row['CIK'], ledger)
    #         drv.quit()
        
    #     ledger = download_links(row['CIK'], ledger)
    #     save_ledger(row['CIK'], ledger)
    #     # zsecform13_arr = []
    #     # zsecform13filer_arr = []
    #     for i, entry  in ledger.iterrows():
    #         if entry['DOWNLOADED'] and entry['FORM_TYPE'] == '13F-HR':
    #             ZSECFORM13_dict, ZSECFORM13_FILER_dict, ZSECFORM13_INFO_arr = parse_form13fhr(row['CIK'], entry['FILENAME'])
    #             upload_form13fhr(conn, ZSECFORM13_dict, ZSECFORM13_FILER_dict, ZSECFORM13_INFO_arr)

    # conn.close() ['3', '3/A', '4', '4/A', '5', '5/A']

    # line = "      <name>Daniel N. Mullen</name>"

    # key, match = parse_line(line)
    # print(key, match)

    # cik = "0001537621"
    # filename = "0000950123-13-005234.txt"
    # ZSECFORM13_dict, ZSECFORM13_FILER_dict, ZSECFORM13_INFO_arr = parse_form13fhr(cik, filename)
    # print(ZSECFORM13_dict)
    # print(ZSECFORM13_FILER_dict)
    # print(ZSECFORM13_INFO_arr)
    # print(files)


    # # if not args.url:
    # #     print('You must supply a url\n', file=sys.stderr)
    # #     parser.print_help()
    # #     return

    # for i in range(0, 8):
    #     if i < 7:
    #         ciks = pandas.read_excel('seccik.xlsx', nrows=100000, skiprows=(100000*i), engine='openpyxl', usecols=[2,4], names=['CIK', 'COMP_CONFRMEDNAME'])
    #         for j in range (0, 10):
    #             cik = ciks[10000*j:10000*(j+1)]
    #             cik.to_excel(f"cik_files/cik_{i}{j}.xls", index=False) 
    #     else:
    #         ciks = pandas.read_excel('seccik.xlsx', nrows=20000, skiprows=(100000*i), engine='openpyxl', usecols=[2,4], names=['CIK', 'COMP_CONFRMEDNAME'])
    #         for j in range (0, 2):
    #             cik = ciks[10000*j:10000*(j+1)]
    #             cik.to_excel(f"cik_files/cik_{i}{j}.xls", index=False) 

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")
