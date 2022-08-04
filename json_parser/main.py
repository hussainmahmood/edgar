import urllib
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import pandas as pd
from models import metadata, BasicInformation, MailingAddress, BusinessAddress, FormerName, File, Filing

def create_db_instance():
    params = urllib.parse.quote_plus('Driver={ODBC Driver 17 for SQL Server};' 'Server=.;' 'Port=1433;'
                                     'Database=edgar_json;' 'UID=sa;' 'PWD=tag$tag12;')
    db_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    return db_engine

def create_tables(db_engine):
    metadata.bind = db_engine
    for table in metadata.sorted_tables:
        table.create(db_engine, checkfirst=True)
    return

def main():
	db_engine = create_db_instance()
	create_tables(db_engine)
	Session = sessionmaker(bind=db_engine)
	session = Session()
	opt = wd.ChromeOptions()
	opt.add_argument('--incognito')
	opt.add_argument('--ignore-certificate-errors')
	drv = wd.Chrome('../chromedriver_win32/chromedriver' , options=opt)

	for cik_file in os.listdir('cik'):
		ciks = pd.read_excel(f"cik/{cik_file}", engine='openpyxl', header=0, dtype=object, squeeze=True)
		for cik in ciks:
			drv.get(f"https://data.sec.gov/submissions/CIK{cik}.json")  
			body = drv.find_element_by_tag_name('body')
			pret = bs(body.get_attribute('innerHTML'), features='lxml')
			json_text = pret.find('pre')
			try:
				data = json.loads(json_text.get_text())
			except Exception as e: 
				print(e)
			else:
				if isinstance(data, dict):
					tickers = None
					exchanges = None
					if data["tickers"]:
						tickers = ", ".join(data["tickers"])
					if data["exchanges"]:
						exchanges = ", ".join(data["exchanges"])
					basic_info 	= 	{"cik": data["cik"], 
									"entityType": data["entityType"],
									"sic": data["sic"],
									"sicDescription": data["sicDescription"],
									"insiderTransactionForOwnerExists": data["insiderTransactionForOwnerExists"],
									"insiderTransactionForIssuerExists": data["insiderTransactionForIssuerExists"],
									"name": data["name"],
									"tickers": tickers,
									"exchanges": exchanges,
									"ein": data["ein"],
									"description": data["description"],
									"website": data["website"],
									"investorWebsite": data["investorWebsite"],
									"category": data["category"],
									"fiscalYearEnd": data["fiscalYearEnd"],
									"stateOfIncorporation": data["stateOfIncorporation"],
									"stateOfIncorporationDescription": data["stateOfIncorporationDescription"],
									"phone": data["phone"],
									"flags": data["flags"]}
					mailing_address = data["addresses"]["mailing"]
					mailing_address["cik"] = basic_info["cik"]
					business_address = data["addresses"]["business"]
					business_address["cik"] = basic_info["cik"]
					former_name_arr = []
					for former in data["formerNames"]:
						former_name = {"cik": basic_info["cik"], "name": former["name"],"from_date": former["from"][:10], "to_date": former["to"][:10]}
						former_name_arr.append(former_name)
					file_arr = []
					for file in data["filings"]["files"]:
						file["cik"] = basic_info["cik"]
						file_arr.append(file)
					filing_arr = []
					recent = data["filings"]["recent"]
					for i in range(len(recent["accessionNumber"])):
						filing = {"cik": basic_info["cik"], 
								  "accessionNumber": recent["accessionNumber"][i],
								  "filingDate": recent["filingDate"][i],
								  "reportDate": recent["reportDate"][i], 
								  "acceptanceDateTime": recent["acceptanceDateTime"][i], 
								  "act": recent["act"][i],
								  "form": recent["form"][i], 
								  "fileNumber": recent["fileNumber"][i], 
								  "filmNumber": recent["filmNumber"][i],
								  "items": recent["items"][i], 
								  "size": recent["size"][i], 
								  "isXBRL": recent["isXBRL"][i],
								  "isInlineXBRL": recent["isInlineXBRL"][i], 
								  "primaryDocument": recent["primaryDocument"][i], 
								  "primaryDocDescription": recent["primaryDocDescription"][i]}
						filing_arr.append(filing)


					session.add_all([BasicInformation(**basic_info), MailingAddress(**mailing_address), BusinessAddress(**business_address)])
					session.add_all([FormerName(**former_name) for former_name in former_name_arr])
					session.add_all([File(**file) for file in file_arr])
					session.add_all([Filing(**filing) for filing in filing_arr])
					try:
						session.commit()
					except Exception as e:
						session.rollback()
				else:
					print(type(data))

	drv.quit()
	session.close()

if __name__ == "__main__":
    main()