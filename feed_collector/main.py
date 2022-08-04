import re
import urllib
import time
import pytz
from datetime import datetime
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
from sqlalchemy import Column, DateTime, Date, String, Integer, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
metadata = Base.metadata


class Feed(Base):
    __tablename__ = 'feed'
    __table_args__ = (UniqueConstraint('cik', 'report_type', 'accession_number', 'file', 'date_accepted', name='ux_cik_report_accession_file_date'),
                     )

    feed_id = Column(Integer, primary_key=True)
    cik = Column(String(15))
    name = Column(String)
    report_type = Column(String(15))
    accession_number = Column(String(30))
    form_type = Column(String)
    description = Column(String)
    text_url = Column(String)
    html_url = Column(String)
    date_accepted = Column(DateTime)
    date_filed = Column(Date)  
    file = Column(String(15))
    film_number = Column(String)

def create_db_instance():
    params = urllib.parse.quote_plus('Driver={ODBC Driver 17 for SQL Server};' 'Server=.;' 'Port=1433;'
                                     'Database=edgar_db;' 'UID=sa;' 'PWD=tag$tag12;')
    db_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    conn = db_engine.connect()
    return db_engine, conn

def create_tables(db_engine):
    metadata.bind = db_engine
    for table in metadata.sorted_tables:
        table.create(db_engine, checkfirst=True)
    return

def main():
    db_engine, conn = create_db_instance()
    create_tables(db_engine)
    opt = wd.ChromeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--remote-debugging-port=9222')
    opt.add_argument('--incognito')
    opt.add_argument('--ignore-certificate-errors')
    drv = wd.Chrome('chromedriver_win32/chromedriver' , options=opt)

    drv.get('https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent')
    last = datetime(1970, 1, 1, tzinfo=pytz.timezone('US/Eastern'))
    timezone = pytz.timezone('US/Eastern')
    last_cik = ""
    last_report = "" 
    last_accession = ""
    while True:
        drv.refresh()
        i = 0
        body = drv.find_element_by_tag_name('body')
        pret = bs(body.get_attribute('innerHTML'), features='lxml')
        if not pret:
            continue
        tr = pret.find('th', text='Form').parent
        table = tr.parent
        trs = table.find_all('tr')
        trs.pop(0)
        continued = False
        for tr in reversed(trs):
            i += 1
            if continued:
                continued = False
                continue
            tds = tr.find_all('td')
            if i % 2 == 0:
                temp = tds[-1].get_text().split('(')
                feed_dict['cik'] = temp[-2].replace(')', '').strip()
                feed_dict['name'] = temp[0].strip()
                for part in temp[1:-2]:
                    feed_dict['name'] += f" ({part.strip()}"
                feed_dict['report_type'] = temp[-1].replace(')', '').strip()
                if not (last_cik == feed_dict['cik'] and last_report == feed_dict['report_type'] and last_accession == feed_dict['accession_number']):
                    last_cik = feed_dict['cik']
                    last_report = feed_dict['report_type'] 
                    last_accession = feed_dict['accession_number'] 
                    try:
                        conn.execute(Feed.__table__.insert(), feed_dict)
                    except Exception as e:
                        pass
            else:
                accept_time = tds[3].get_text().strip()
                accept_pend = datetime.strptime(accept_time, '%Y-%m-%d%H:%M:%S')
                accept_pend = timezone.localize(accept_pend)
                if accept_pend >= last:
                    last = accept_pend                     
                    desc = tds[2].get_text().split('Accession Number:')
                    accession = desc[1].split()
                    text_link = tds[1].find('a', text='[text]')
                    html_link = tds[1].find('a', text='[html]')
                    filed_date = tds[4].get_text().strip()
                    filed_pend = datetime.strptime(filed_date[:10], '%Y-%m-%d')
                    feed_dict = {}
                    feed_dict['accession_number'] = accession[0]
                    feed_dict['form_type'] = tds[0].get_text().strip()
                    feed_dict['description'] = desc[0].strip()
                    feed_dict['text_url'] = text_link['href']
                    feed_dict['html_url'] = html_link['href']
                    feed_dict['date_accepted'] = accept_pend
                    feed_dict['date_filed'] = filed_pend
                    if len(tds) == 6:
                        file = tds[5].find('a')
                        file = file.get_text().strip()
                        film_number = tds[5].get_text().replace(file, '').strip()
                        feed_dict['file'] = file
                        feed_dict['film_number'] = film_number
                else:
                    continued = True
                    continue

        time.sleep(60)

if __name__ == "__main__":
    main()