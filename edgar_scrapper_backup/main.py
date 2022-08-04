import os
import argparse
import sys
import time
from datetime import datetime
from helper import TimeoutException, read_ciks, create_driver, create_db_instance, create_session, create_tables, save_ledger, create_directory, get_links, download_links, parse_and_upload_form4
from company import Company

def main():
    # db_engine, conn = create_db_instance()
    # create_tables(db_engine)
    # drv = create_driver()
    # for cik_file in os.listdir('cik_files'):
    #     rows = read_ciks(cik_file)
    #     for i, row  in rows.iterrows():
    #         if not os.path.exists(f"companies/{row['CIK']}"):
    #             os.makedirs(f"companies/{row['CIK']}")
    #         company = Company(row['CIK'], drv)
    #         company.download_forms(['3', '3/A', '4', '4/A', '5', '5/A'])
    #         company.save_ledger()
    #         company.upload_forms(conn, ['3', '3/A'])
    #         company.save_ledger()

    # drv.quit()

    # parser = argparse.ArgumentParser(description='Pulls data from SEC and stores it in SQL Server Database.')
    # parser.add_argument('url', nargs='?', help='Url to the site')
    # parser.add_argument('--outfile', help='file to write output to (default: stdout)')
    # args = parser.parse_args()

    forms_required = ['4', '4/A']
    form_4 = ['4', '4/A']
    db_engine = create_db_instance()
    create_tables(db_engine)
    error_log = open(f"error_log.txt", "a")  
    for cik_file in os.listdir('cik'):
        ciks = read_ciks(cik_file)
        for cik in ciks:
            ledger = create_directory(cik)
            print(cik)
            save_ledger(cik, ledger)
            if ledger.empty:
                drv = create_driver()
                drv.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='+cik+'&owner=include&count=100')
                ledger = get_links(drv, cik, ledger)
                save_ledger(cik, ledger)
                drv.quit()
            
            ledger = download_links(cik, ledger, forms_required)
            for i, entry  in ledger.iterrows():
                if entry['DOWNLOADED'] and entry['FORM_TYPE'] in form_4 and not entry['UPLOADED']:
                    session = create_session(db_engine)
                    try:
                        parse_and_upload_form4(session, cik, entry['FILENAME'])
                        session.commit()
                        entry['UPLOADED'] = True
                    except TimeoutException as e:
                        entry['ERROR'] = e
                        error_log.write(f"CIK: {cik} ({datetime.now()})\n")
                        error_log.write(f"Error: {e}\n")
                        pass
                    except Exception as e:
                        entry['ERROR'] = e
                        error_log.write(f"CIK: {cik} ({datetime.now()})\n")
                        error_log.write(f"Error: {e}\n")
                        session.rollback()
                        pass
                    finally:
                        session.close()
            save_ledger(cik, ledger)

    error_log.close()

    parse_and_upload_form4("0000824104", "0001144204-04-008193.txt")

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
