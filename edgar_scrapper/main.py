import os
import sys
import time
import pandas as pd
from selenium import webdriver as wd
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from helper import (TimeoutException, read_ciks, create_db_instance, create_session, create_tables, save_ledger, create_directory, 
                    get_links, download_links, parse_and_upload_form3, parse_and_upload_form4, parse_and_upload_form5)

def main():
    opt = wd.ChromeOptions()
    # opt.add_argument('--no-sandbox')
    # opt.add_argument('--headless')
    # opt.add_argument('--disable-gpu')
    # opt.add_argument('--remote-debugging-port=9222')
    opt.add_argument('--incognito')
    opt.add_argument('--ignore-certificate-errors')
    drv = wd.Chrome('../chromedriver_win32/chromedriver' , options=opt)
    error_log = pd.DataFrame(columns=['CIK', 'TIME', 'ERR_TYPE', 'ERROR'], dtype=object)
    forms_required = ['3', '3/A', '4', '4/A', '5', '5/A']
    form_3 = ['3', '3/A']
    form_4 = ['4', '4/A']
    form_5 = ['5', '5/A']
    db_engine = create_db_instance()
    create_tables(db_engine)
    session = create_session(db_engine)
    for cik_file in os.listdir('cik'):
        ciks = read_ciks(cik_file)
        for cik in ciks:
            ledger = create_directory(cik)
            print(cik)
            drv.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='+cik+'&owner=include&count=100')
            ledger, fetch_exception, fetch_error = get_links(drv, cik, ledger, datetime.fromisoformat('2021-04-02'))
            if fetch_exception:
                error_log = error_log.append(pd.DataFrame([[cik, datetime.now(), 'GetLinkException', fetch_error]], columns=['CIK', 'TIME', 'ERR_TYPE', 'ERROR'], dtype=object))
                continue

            ledger, download_exception, download_error = download_links(cik, ledger, forms_required, drv)
            if download_exception:
                error_log = error_log.append(pd.DataFrame([[cik, datetime.now(), 'DownloadException', download_error]], columns=['CIK', 'TIME', 'ERR_TYPE', 'ERROR'], dtype=object))
                continue

            for i, entry  in ledger.iterrows():
                if entry['UPLOADED'] == 'FALSE':
                    if entry['FORM_TYPE'] in form_3:
                        try:
                            parse_and_upload_form3(session, cik, entry['FILENAME'])
                            session.commit()
                            entry['UPLOADED'] = 'TRUE'
                        except TimeoutException as e:
                            error_log = error_log.append(pd.DataFrame([[cik, datetime.now(), 'Timeout', e]], columns=['CIK', 'TIME', 'ERR_TYPE', 'ERROR'], dtype=object))
                        except IntegrityError:
                            entry['UPLOADED'] = 'TRUE'
                        except Exception as e:
                            error_log = error_log.append(pd.DataFrame([[cik, datetime.now(), 'SessionException', e]], columns=['CIK', 'TIME', 'ERR_TYPE', 'ERROR'], dtype=object))
                        finally:
                            session.rollback()
                    elif entry['FORM_TYPE'] in form_4:
                        try:
                            parse_and_upload_form4(session, cik, entry['FILENAME'])
                            session.commit()
                            entry['UPLOADED'] = 'TRUE'
                        except TimeoutException as e:
                            error_log = error_log.append(pd.DataFrame([[cik, datetime.now(), 'Timeout', e]], columns=['CIK', 'TIME', 'ERR_TYPE', 'ERROR'], dtype=object))
                        except IntegrityError:
                            entry['UPLOADED'] = 'TRUE'
                        except Exception as e:
                            error_log = error_log.append(pd.DataFrame([[cik, datetime.now(), 'SessionException', e]], columns=['CIK', 'TIME', 'ERR_TYPE', 'ERROR'], dtype=object))
                        finally:
                            session.rollback()
                    elif entry['FORM_TYPE'] in form_5:
                        try:
                            parse_and_upload_form5(session, cik, entry['FILENAME'])
                            session.commit()
                            entry['UPLOADED'] = 'TRUE'
                        except TimeoutException as e:
                            error_log = error_log.append(pd.DataFrame([[cik, datetime.now(), 'Timeout', e]], columns=['CIK', 'TIME', 'ERR_TYPE', 'ERROR'], dtype=object))
                        except IntegrityError:
                            entry['UPLOADED'] = 'TRUE'
                        except Exception as e:
                            error_log = error_log.append(pd.DataFrame([[cik, datetime.now(), 'SessionException', e]], columns=['CIK', 'TIME', 'ERR_TYPE', 'ERROR'], dtype=object))
                        finally:
                            session.rollback()

            save_ledger(cik, ledger)
    
    error_log.to_csv(f"error_log.csv", index=False)
    drv.quit()
    session.close()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")
