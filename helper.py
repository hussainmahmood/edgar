import os
import re
import pandas as pd
import requests
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import urllib
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import metadata

# itm_frm = pd.read_excel('item_files/demo.xlsx', usecols=[1,5], engine="openpyxl")
req = requests.session()
req.keep_alive = False
filename_regex = re.compile("-index.htm[l]{0,1}$")
# forms_required = ['SC 13G', 'DEF 14A', '13F-HR', 'PREM14A', 'DEFM14A', 
# 				  '425', 'SC TO-T', 'SC TO-I', 'SC 14D9', 'UPLOAD', 
# 				  'CORRESP', 'N-1A/485', '497K', '497', 'N-CSR/N-CSRS',
# 				  'N-PX', 'N-PORT', 'N-14']
forms_required = ['13F-HR']

# strDefinitions = ["<SEC-DOCUMENT>", "<SEC-HEADER>", "<ACCEPTANCE-DATETIME>", "ACCESSION NUMBER:", "PUBLIC DOCUMENT COUNT:", 
# 				  "CONFORMED PERIOD OF REPORT:", "FILED AS OF DATE:", "DATE AS OF CHANGE:", "EFFECTIVENESS DATE:", 
# 				  "COMPANY CONFORMED NAME:", "CENTRAL INDEX KEY:", "IRS NUMBER:", "STATE OF INCORPORATION:", 
# 				  "FISCAL YEAR END:", "FORM TYPE:", "SEC ACT:", "SEC FILE NUMBER:", "FILM NUMBER:", "BUSINESS ADDRESS:", 
# 				  "MAIL ADDRESS:", "STREET 1:", "STREET 2:", "CITY:", "STATE:", "ZIP:", "BUSINESS PHONE:", "<SEQUENCE>"]

rx_13fhr = {
	'ZACCESSIONNO': re.compile(r'ACCESSION NUMBER:(?P<accession_no>.*)'),
    'ZSECDOC': re.compile(r'<SEC-DOCUMENT>(?P<sec_doc>.*)'),
    'ZSEC_ACCEPTTIME': re.compile(r'<ACCEPTANCE-DATETIME>(?P<sec_acceptime>.*)'),
    'ZCIK_ISSUER': re.compile(r'CENTRAL INDEX KEY:(?P<cik>.*)'),
    'ZFORM_TYPE': re.compile(r'CONFORMED SUBMISSION TYPE:(?P<form_type>.*)'),
    'ZSECHEADER': re.compile(r'<SEC-HEADER>(?P<sec_header>.*)'),
    'ZDOC_COUNT': re.compile(r'PUBLIC DOCUMENT COUNT:(?P<doc_count>.*)'),
    'ZREPORT_PERIOD': re.compile(r'CONFORMED PERIOD OF REPORT:(?P<report_period>.*)'),
    'ZDATE_FILED': re.compile(r'FILED AS OF DATE:(?P<filed_date>.*)'),
    'ZDATE_CHANGED': re.compile(r'DATE AS OF CHANGE:(?P<change_date>.*)'),
    'ZSEC_FILENO': re.compile(r'SEC FILE NUMBER:(?P<file_no>.*)'),
    'ZXML_VERSION': re.compile(r'<\?xml version=(?P<xml_version>.*) encoding="UTF-8"\?>'),
    'SIGN_BLOCK': re.compile(r'<signatureBlock>'),
    'ZSIGN_TITLE': re.compile(r'<title>(?P<sign_title>.*)</title>'),
    'ZSIGN_NAME': re.compile(r'<name>(?P<sign_name>.*)</name>'),
    'ZSIGN_DATE': re.compile(r'<signatureDate>(?P<sign_date>.*)</signatureDate>'),
    'END_SIGN_BLOCK': re.compile(r'</signatureBlock>'),
    'ZTOTAL_TABENTRY': re.compile(r'<tableEntryTotal>(?P<total_tab_entry>.*)</tableEntryTotal>'),
    'ZTOTAL_TABVALUE': re.compile(r'<tableValueTotal>(?P<total_tab_value>.*)</tableValueTotal>'),
    'ZCOMPCONFDNAME': re.compile(r'COMPANY CONFORMED NAME:(?P<comp_name>.*)'),
    'ZSEC_IRSNO': re.compile(r'IRS NUMBER:(?P<irs_no>.*)'),
    'ZINCORP_STATE': re.compile(r'STATE OF INCORPORATION:(?P<inc_state>.*)'),
    'ZFISCAL_YREND': re.compile(r'FISCAL YEAR END:(?P<fiscal_year>.*)'),
    'BUS_ADDR': re.compile(r'BUSINESS ADDRESS:.*'),
    'MAIL_ADDR': re.compile(r'MAIL ADDRESS:.*'), 
    'STREET1': re.compile(r'STREET 1:(?P<street>.*)'),
    'STREET2': re.compile(r'STREET 2:(?P<street>.*)'),
    'CITY': re.compile(r'CITY:(?P<city>.*)'),
    'REGION': re.compile(r'STATE:(?P<region>.*)'),
    'POST_CODE': re.compile(r'ZIP:(?P<post_code>.*)'),
    'BUS_TELF': re.compile(r'BUSINESS PHONE:(?P<bus_telf>.*)'),
    'INFO_TABLE': re.compile(r'<infoTable>'),
    'ZCUSIP': re.compile(r'<cusip>(?P<cusip>.*)</cusip>'),
    'ZSHAREPRINCIPAL': re.compile(r'<nameOfIssuer>(?P<share_principal>.*)</nameOfIssuer>'), 
	'ZCLASS_TITLE': re.compile(r'<titleOfClass>(?P<class_title>.*)</titleOfClass>'),  
	'ZVALUE': re.compile(r'<value>(?P<value>.*)</value>'),  
	'ZSHARES': re.compile(r'<sshPrnamt>(?P<shares>.*)</sshPrnamt>'),  
	'ZSSHPRNAMTYPE': re.compile(r'<sshPrnamtType>(?P<share_type>.*)</sshPrnamtType>'),  
	'ZPUT_CALL': re.compile(r'<putCall>(?P<class_title>.*)</putCall>'), 
	'ZINVST_DISCRET': re.compile(r'<investmentDiscretion>(?P<inv_discret>.*)</investmentDiscretion>'),
	'ZOTHERMANAGERS': re.compile(r'<otherManager>(?P<other_manager>.*)</otherManager>'),
	'ZVOTEAUTHSOLE': re.compile(r'<Sole>(?P<vote_sole>.*)</Sole>'),  
	'ZVOTEAUTHSHARED': re.compile(r'<Shared>(?P<vote_shared>.*)</Shared>'), 
	'ZVOTEAUTHNONE': re.compile(r'<None>(?P<vote_none>.*)</None>'), 
	'END_INFO_TABLE': re.compile(r'</infoTable>'),
}


def read_ciks(cik_file):
	return pd.read_excel(f"cik_files/{cik_file}", engine='xlrd', header=0, dtype=object)

def create_directory(cik):
	if not os.path.exists(f"txt_files/{cik}"):
		os.makedirs(f"txt_files/{cik}")
		ledger = pd.DataFrame(columns=['FORM_TYPE', 'LINK', 'FILENAME', 'DOWNLOADED', 'UPLOADED', 'ERROR'])
		# ledger.to_excel(f'txt_files/{cik}/ledger.xls', index=False)
	else:
		ledger = pd.read_excel(f'txt_files/{cik}/ledger.xls', header=0)

	return ledger

def create_driver():
	opt = wd.ChromeOptions()
	opt.add_argument('--no-sandbox')
	opt.add_argument('--headless')
	opt.add_argument("--disable-dev-shm-usage")
	opt.add_argument("--disable-gpu")
	opt.add_argument("--disable-features=NetworkService")
	opt.add_argument("--window-size=1920x1080")
	opt.add_argument("--disable-features=VizDisplayCompositor")
	opt.add_argument('--incognito')
	opt.add_argument('--ignore-certificate-errors')
	return wd.Chrome('chromedriver_win32/chromedriver' , options=opt)

def get_links(drv, cik, ledger):
	next_button = True
	while next_button:
		try:
			table_div = drv.find_element_by_id('seriesDiv')
			pret = bs(table_div.get_attribute('innerHTML'), features='lxml')
			for tr in pret.find_all("tr"):
				tds = tr.find_all("td")
				if tds:
					form_type = tds[0].get_text().strip()
					link = tds[1].find('a', id='documentsbutton').get('href').strip()
					link = re.sub(filename_regex, '.txt', link)
					if link not in ledger.values:
						filename = link.split('/')[-1]
						ledger = ledger.append(pd.DataFrame([[form_type, link, filename, False, False, ""]], columns=['FORM_TYPE', 'LINK', 'FILENAME', 'DOWNLOADED', 'UPLOADED', 'ERROR']))
			try:
				drv.find_element_by_css_selector("input[value='Next 100']").click()
			except Exception as e:
				next_button = False 
		except Exception as e:
			next_button = False 
			print(f"CIK: {cik}")
			print(f"Error: {e}")
			pass

	return ledger

def download_links(cik, ledger):
    for i, entry  in ledger.iterrows():
    	if not entry['DOWNLOADED'] and entry['FORM_TYPE'] in forms_required:
    		try:
	    		r = req.get(f"https://www.sec.gov{entry['LINK']}", timeout=3)
	    		with open(f"txt_files/{cik}/{entry['FILENAME']}", 'wb') as f:  
	    			# for line in res.splitlines():
	    			# 	if line.__contains__(docCountStr):
	    			# 		docCount = int(line.replace(docCountStr, '').strip())
	    			# 		break
	    			f.write(r.content) 
	    			f.close()
	    		entry['DOWNLOADED'] = True
	    	except Exception as e:
	    		entry['ERROR'] = e
	    		print(f"Filename: {entry['FILENAME']}")
	    		print(f"Error: {e}")
	    		pass

    return ledger


def parse_form13fhr_line(line):
    for key, rx in rx_13fhr.items():
        match = rx.search(line)
        if match:
        	return key, match
    
    return None, None

def parse_form13fhr(cik, filename):
    ZSECFORM13_dict = {
    'MANDT': "100", 'ZACCESSIONNO': None, 'ZSECDOC': None, 'ZSEC_ACCEPTTIME': None, 'ZCIK_ISSUER': None, 'ZFORM_TYPE': None, 
    'ZISSUER_SYMBOL': None, 'ZSECHEADER': None, 'ZDOC_COUNT': None, 'ZREPORT_PERIOD': None, 'ZDATE_FILED': None, 
    'ZDATE_CHANGED': None, 'ZAMEND': None, 'ZAMEND_NUMBER': None, 'ZAMEND_RESTATE': None, 'ZAMEND_NEWHOLDING': None, 
    'VERSION': None, 'ZSEC_FILENO': None, 'ZSEC_FILENAME': None, 'ZFILE_DESCRIP': None, 'ZXML_VERSION': None, 
    'ZSCHEMA_VERSION': None, 'ZSECTION16': None, 'ZSIGN_TITLE': None, 'ZSIGN_NAME': None, 'ZSIGN_DATE': None, 
    'ERDAT': None, 'ERNAME': None, 'ZTOTAL_TABENTRY': None, 'ZTOTAL_TABVALUE': None,
    }

    ZSECFORM13_FILER_dict = {
    'MANDT': "100", 'ZACCESSIONNO': None, 'ZCIK_ISSUER': None, 'ZCOMPCONFDNAME': None, 'ZSEC_IRSNO': None, 
    'ZINCORP_STATE': None, 'ZFISCAL_YREND': None, 'BUS_STRAS': None, 'BUS_CITY': None, 'BUS_REGION': None, 
    'BUS_BEZEI20': None, 'BUS_POST_CODE': None, 'BUS_TELF': None, 'MAIL_STRAS': None, 'MAIL_CITY': None, 
    'MAIL_REGION': None, 'MAIL_POST_CODE': None, 'ZFCOMPCONFDNAME1': None, 'ZDATE_NAMECHANGE1': None, 
    'ZFCOMPCONFDNAME2': None, 'ZDATE_NAMECHANGE2': None, 'ZFCOMPCONFDNAME3': None, 'ZDATE_NAMECHANGE3': None,
    }

    ZSECFORM13F_INFO_arr = []

    with open(f"txt_files/{cik}/{filename}", 'r') as f:
        line = f.readline()
        while line:
            key, match = parse_form13fhr_line(line)
            if key == 'ZACCESSIONNO':
                ZSECFORM13_dict['ZACCESSIONNO'] = match.group('accession_no').strip()
                ZSECFORM13_FILER_dict['ZACCESSIONNO'] = match.group('accession_no').strip()
            elif key == 'ZSECDOC':
                ZSECFORM13_dict['ZSECDOC'] = match.group('sec_doc').strip()
                ZSECFORM13_dict['ZSECDOC'] = match.group('sec_doc').strip()
            elif key == 'ZSEC_ACCEPTTIME':
                ZSECFORM13_dict['ZSEC_ACCEPTTIME'] = match.group('sec_acceptime').strip()
            elif key == 'ZCIK_ISSUER':
                ZSECFORM13_dict['ZCIK_ISSUER'] = match.group('cik').strip()
                ZSECFORM13_FILER_dict['ZCIK_ISSUER'] = match.group('cik').strip()
            elif key == 'ZFORM_TYPE':
                ZSECFORM13_dict['ZFORM_TYPE'] = match.group('form_type').strip()
            elif key == 'ZSECHEADER':
                ZSECFORM13_dict['ZSECHEADER'] = match.group('sec_header').strip()
            elif key == 'ZDOC_COUNT':
                ZSECFORM13_dict['ZDOC_COUNT'] = match.group('doc_count').strip()
            elif key == 'ZREPORT_PERIOD':
                ZSECFORM13_dict['ZREPORT_PERIOD'] = match.group('report_period').strip()
            elif key == 'ZDATE_FILED':
                ZSECFORM13_dict['ZDATE_FILED'] = match.group('filed_date').strip()
            elif key == 'ZDATE_CHANGED':
                ZSECFORM13_dict['ZDATE_CHANGED'] = match.group('change_date').strip()
            elif key == 'ZSEC_FILENO':
                ZSECFORM13_dict['ZSEC_FILENO'] = match.group('file_no').strip()
            elif key == 'ZXML_VERSION':
                ZSECFORM13_dict['ZXML_VERSION'] = match.group('xml_version').strip()
            elif key == 'SIGN_BLOCK':
            	while key != 'END_SIGN_BLOCK':
            		key, match = parse_form13fhr_line(line)
            		if key == 'ZSIGN_TITLE':
            			ZSECFORM13_dict['ZSIGN_TITLE'] = match.group('sign_title').strip()
            		elif key == 'ZSIGN_NAME':
            			ZSECFORM13_dict['ZSIGN_NAME'] = match.group('sign_name').strip()
            		elif key == 'ZSIGN_DATE':
            			ZSECFORM13_dict['ZSIGN_DATE'] = match.group('sign_date').strip()
            		line = f.readline()
            elif key == 'ZTOTAL_TABENTRY':
                ZSECFORM13_dict[key] = match.group('total_tab_entry').strip()
            elif key == 'ZTOTAL_TABVALUE':
                ZSECFORM13_dict[key] = match.group('total_tab_value').strip()
            elif key == 'ZCOMPCONFDNAME':
                ZSECFORM13_FILER_dict[key] = match.group('comp_name').strip()
            elif key == 'ZSEC_IRSNO':
                ZSECFORM13_FILER_dict[key] = match.group('irs_no').strip()
            elif key == 'ZINCORP_STATE':
                ZSECFORM13_FILER_dict[key] = match.group('inc_state').strip()
            elif key == 'ZFISCAL_YREND':
                ZSECFORM13_FILER_dict[key] = match.group('fiscal_year').strip()
            elif key == 'BUS_ADDR':
                while key != 'BUS_TELF':
                    key, match = parse_form13fhr_line(line)
                    if key == 'STREET1':
                        ZSECFORM13_FILER_dict['BUS_STRAS'] = match.group('street').strip()
                    elif key == 'STREET2':
                        ZSECFORM13_FILER_dict['BUS_STRAS'] += f", {match.group('street').strip()}"
                    elif key == 'CITY':
                        ZSECFORM13_FILER_dict['BUS_CITY'] = match.group('city').strip()
                    elif key == 'REGION':
                        ZSECFORM13_FILER_dict['BUS_REGION'] = match.group('region').strip()
                    elif key == 'POST_CODE':
                        ZSECFORM13_FILER_dict['BUS_POST_CODE'] = match.group('post_code').strip()
                    elif key == 'BUS_TELF':
                        ZSECFORM13_FILER_dict[key] = match.group('bus_telf').strip()

                    line = f.readline()
            
            elif key == 'MAIL_ADDR':
                while key != 'POST_CODE':
                    key, match = parse_form13fhr_line(line)
                    if key == 'STREET1':
                        ZSECFORM13_FILER_dict['MAIL_STRAS'] = match.group('street').strip()
                    elif key == 'STREET2':
                        ZSECFORM13_FILER_dict['MAIL_STRAS'] += f", {match.group('street').strip()}"
                    elif key == 'CITY':
                        ZSECFORM13_FILER_dict['MAIL_CITY'] = match.group('city').strip()
                    elif key == 'REGION':
                        ZSECFORM13_FILER_dict['MAIL_REGION'] = match.group('region').strip()
                    elif key == 'POST_CODE':
                        ZSECFORM13_FILER_dict['MAIL_POST_CODE'] = match.group('post_code').strip()

                    line = f.readline()

            elif key == 'INFO_TABLE':
            	ZSECFORM13F_INFO_dict = {'MANDT': "100", 'ZACCESSIONNO': ZSECFORM13_dict['ZACCESSIONNO'], 
            	'ZCIK_ISSUER': ZSECFORM13_dict['ZCIK_ISSUER'], 'ZCUSIP': None, 'ZSHAREPRINCIPAL': None, 
            	'ZCOMPCONFDNAME': ZSECFORM13_FILER_dict['ZCOMPCONFDNAME'], 'ZCLASS_TITLE': None, 'ZVALUE': None, 
            	'ZSHARES': None, 'ZSSHPRNAMTYPE': None, 'ZPUT_CALL': None, 'ZINVST_DISCRET': None, 
            	'ZOTHERMANAGERS': None, 'ZVOTEAUTHSOLE': None, 'ZVOTEAUTHSHARED': None, 'ZVOTEAUTHNONE': None }
            	while key != 'END_INFO_TABLE':
            		key, match = parse_form13fhr_line(line)
            		if key == 'ZCUSIP':
            			ZSECFORM13F_INFO_dict[key] = match.group('cusip').strip()
            		elif key == 'ZSHAREPRINCIPAL':
            			ZSECFORM13F_INFO_dict[key] = match.group('share_principal').strip()
            		elif key == 'ZCLASS_TITLE':
            			ZSECFORM13F_INFO_dict[key] = match.group('class_title').strip()
            		elif key == 'ZVALUE':
            			ZSECFORM13F_INFO_dict[key] = match.group('value').strip()
            		elif key == 'ZSHARES':
            			ZSECFORM13F_INFO_dict[key] = match.group('shares').strip()
            		elif key == 'ZSSHPRNAMTYPE':
            			ZSECFORM13F_INFO_dict[key] = match.group('share_type').strip()
            		elif key == 'ZINVST_DISCRET':
            			ZSECFORM13F_INFO_dict[key] = match.group('inv_discret').strip()
            		elif key == 'ZOTHERMANAGERS':
            			ZSECFORM13F_INFO_dict[key] = match.group('other_manager').strip()
            		elif key == 'ZVOTEAUTHSOLE':
            			ZSECFORM13F_INFO_dict[key] = match.group('vote_sole').strip()
            		elif key == 'ZVOTEAUTHSHARED':
            			ZSECFORM13F_INFO_dict[key] = match.group('vote_shared').strip()
            		elif key == 'ZVOTEAUTHNONE':
            			ZSECFORM13F_INFO_dict[key] = match.group('vote_none').strip()

            		line = f.readline()
            	ZSECFORM13F_INFO_arr.append(ZSECFORM13F_INFO_dict)

            line = f.readline()

    return ZSECFORM13_dict, ZSECFORM13_FILER_dict, ZSECFORM13F_INFO_arr

def upload_form13fhr(conn, ZSECFORM13_dict, ZSECFORM13_FILER_dict, ZSECFORM13F_INFO_arr):
	if ZSECFORM13_dict and ZSECFORM13_dict and ZSECFORM13F_INFO_arr:
		conn.execute(ZSECFORM13.__table__.insert(), ZSECFORM13_dict)
		conn.execute(ZSECFORM13_FILER.__table__.insert(), ZSECFORM13_FILER_dict)
		for ZSECFORM13F_INFO_dict in ZSECFORM13F_INFO_arr:
			conn.execute(ZSECFORM13F_INFO.__table__.insert(), ZSECFORM13F_INFO_dict)
		# conn.execute(ZSECFORM13.__table__.insert(), [ZSECFORM13_dict])
		return
        # zsecform13_arr.append(ZSECFORM13_dict)
        # zsecform13filer_arr.append(ZSECFORM13_FILER_dict)




def save_ledger(cik, ledger):
	ledger.to_excel(f"txt_files/{cik}/ledger.xls", index=False)
	return None

# def create_form_entries(cik, form_arr, formfiler_arr, form_type):
# 	if form_type == '13F-HR': 
# 		zsecform13_df = pd.DataFrame(form_arr)
# 		zsecform13filer_df = pd.DataFrame(formfiler_arr)
# 		zsecform13_df.to_excel(f"zsecform13.xls", index=False)
# 		return None

def create_db_instance():
	params = urllib.parse.quote_plus('Driver={ODBC Driver 17 for SQL Server};' 'Server=10.0.0.143;' 'Port=1433;' 
                                         'Database=xbrl_forms;' 'UID=sa;' 'PWD=Welcome@1;')
	db_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
	conn = db_engine.connect()
	return db_engine, conn

def create_tables(db_engine):
	metadata.bind = db_engine
	for table in metadata.sorted_tables:
		table.create(db_engine, checkfirst=True)
	return

def create_objects():
	pass
