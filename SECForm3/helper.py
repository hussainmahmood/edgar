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
from models import (metadata, ZSECFORM3, ZSECFORM3_ISSUER, ZSECFORM3_REPTER, ZSECFORM3_DTAB, ZSECFORM3_NDTAB, ZSECFORM3_FTNOTE,
                    ZSECFORM4, ZSECFORM4_ISSUER, ZSECFORM4_REPTER, ZSECFORM4_DTAB, ZSECFORM4_NDTAB, ZSECFORM4_FTNOTE,
                    ZSECFORM5, ZSECFORM5_ISSUER, ZSECFORM5_REPTER, ZSECFORM5_DTAB, ZSECFORM5_NDTAB, ZSECFORM5_FTNOTE)
import time

class TimeoutException(Exception):
    def __init__(self, line, message="stuck in loop."):
        self.line = line
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'Line: {self.line} -> {self.message}'


# itm_frm = pd.read_excel('item_files/demo.xlsx', usecols=[1,5], engine="openpyxl")
req = requests.session()
req.keep_alive = False
filename_regex = re.compile("-index.htm[l]{0,1}$")
# forms_required = ['SC 13G', 'DEF 14A', '13F-HR', 'PREM14A', 'DEFM14A', 
# 				  '425', 'SC TO-T', 'SC TO-I', 'SC 14D9', 'UPLOAD', 
# 				  'CORRESP', 'N-1A/485', '497K', '497', 'N-CSR/N-CSRS',
# 				  'N-PX', 'N-PORT', 'N-14']

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
	return pd.read_excel(f"cik/{cik_file}", engine='openpyxl', header=0, dtype=object, squeeze=True)

def create_directory(cik):
    if not os.path.exists(f"companies/{cik}"):
        os.makedirs(f"companies/{cik}")
        ledger = pd.DataFrame(columns=['FORM_TYPE', 'LINK', 'FILENAME', 'DOWNLOADED', 'UPLOADED', 'ERROR'])
    else:
        ledger = pd.read_excel(f'companies/{cik}/ledger.xlsx', header=0)
    
    return ledger

def create_driver():
    opt = wd.ChromeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    # opt.add_argument("--disable-features=NetworkService")
    # opt.add_argument("--window-size=1920x1080")
    # opt.add_argument("--disable-features=VizDisplayCompositor")
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

def download_links(cik, ledger, forms_required):
    for i, entry  in ledger.iterrows():
        if not entry['DOWNLOADED'] and entry['FORM_TYPE'] in forms_required:
            try:
                r = req.get(f"https://www.sec.gov{entry['LINK']}", timeout=3)
                with open(f"companies/{cik}/{entry['FILENAME']}", 'wb') as f:
                    soup = bs(r.text, "lxml")
                    f.write(soup.encode("utf-8"))
                    f.close()
                entry['DOWNLOADED'] = True
            except Exception as e:
                entry['ERROR'] = e
                print(f"Filename: {entry['FILENAME']}")
                print(f"Error: {e}")

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

    with open(f"companies/{cik}/{filename}", 'r') as f:
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
	ledger.to_excel(f"companies/{cik}/ledger.xlsx", index=False)
	return None

def create_db_instance():
	params = urllib.parse.quote_plus('Driver={ODBC Driver 17 for SQL Server};' 'Server=10.0.0.143;' 'Port=1433;'
                                     'Database=xbrl_forms;' 'UID=sa;' 'PWD=Welcome@1;')
	db_engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
	return db_engine

def create_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    return Session()

def create_tables(db_engine):
	metadata.bind = db_engine
	for table in metadata.sorted_tables:
		table.create(db_engine, checkfirst=True)
	return

def create_objects():
	pass

rx_3 = {
    'ACCESSIONNO': re.compile(r'ACCESSION NUMBER:(?P<accession_no>.*)'),
    'SEC_DOC': re.compile(r'<SEC-DOCUMENT>(?P<sec_doc>.*)'),
    'ACCEPT_TIME': re.compile(r'<ACCEPTANCE-DATETIME>(?P<accept_time>.*)'),
    'SEC_HEADER': re.compile(r'<SEC-HEADER>(?P<sec_header>.*)'),
    'DOC_FILE_COUNT': re.compile(r'PUBLIC DOCUMENT COUNT:(?P<doc_count>.*)'),
    'REPORT_PERIOD': re.compile(r'CONFORMED PERIOD OF REPORT:(?P<report_period>.*)'),
    'DATE_FILED': re.compile(r'FILED AS OF DATE:(?P<filed_date>.*)'),
    'DATE_CHANGED': re.compile(r'DATE AS OF CHANGE:(?P<change_date>.*)'),
    'REPORTER': re.compile(r'REPORTING-OWNER:'),
    'ISSUER': re.compile(r'ISSUER:'),
    'END_SEC_HEADER': re.compile(r'</SEC-HEADER>'),
    'CIK': re.compile(r'CENTRAL INDEX KEY:(?P<cik>.*)'),
    'FORM_TYPE': re.compile(r'CONFORMED SUBMISSION TYPE:(?P<form_type>.*)'),
    'ISSUER_SYMBOL': re.compile(r'<issuerTradingSymbol>(?P<issuer_symbol>.*)</issuerTradingSymbol>'),
    'SEC_FILENO': re.compile(r'SEC FILE NUMBER:(?P<file_no>.*)'),
    'FILENAME': re.compile(r'<FILENAME>(?P<filename>.*)xml'),
    'FILEDESCRIP': re.compile(r'<DESCRIPTION>(?P<filedescrip>.*)'),
    'XML_VERSION': re.compile(r'<\?xml version=\"(?P<xml_version>.*)\" '),
    'DATE_REPORT': re.compile(r'<periodOfReport>(?P<date_report>.*)</periodOfReport>'),
    'SIGN_BLOCK': re.compile(r'<ownerSignature>'),
    'SIGN_TITLE': re.compile(r'<signatureTitle>(?P<sign_title>.*)</signatureTitle>'),
    'SIGN_NAME': re.compile(r'<signatureName>(?P<sign_name>.*)</signatureName>'),
    'SIGN_DATE': re.compile(r'<signatureDate>(?P<sign_date>.*)</signatureDate>'),
    'END_SIGN_BLOCK': re.compile(r'</ownerSignature>'),
    'SCHEMA_VERSION': re.compile(r'<schemaVersion>(?P<schema>.*)</schemaVersion>'),
    'ISSUER_SYMBOL': re.compile(r'<issuerTradingSymbol>(?P<iss_symbol>.*)</issuerTradingSymbol>'),
    'CONFDNAME': re.compile(r'COMPANY CONFORMED NAME:(?P<comp_name>.*)'),
    'SIC': re.compile(r'STANDARD INDUSTRIAL CLASSIFICATION:.*\[(?P<sic>.*)\]'),
    'IRS': re.compile(r'IRS NUMBER:(?P<irs>.*)'),
    'STATE_INCORP': re.compile(r'STATE OF INCORPORATION:(?P<state_inc>.*)'),
    'FISCAL_YEAREND': re.compile(r'FISCAL YEAR END:(?P<fiscal_year>.*)'),
    'SEC_ACT': re.compile(r'SEC ACT:(?P<sec_act>.*)'),
    'FILM_NO': re.compile(r'FILM NUMBER:(?P<film_no>.*)'),
    'BUS_ADDR': re.compile(r'BUSINESS ADDRESS:.*'),
    'MAIL_ADDR': re.compile(r'MAIL ADDRESS:.*'), 
    'STREET1': re.compile(r'STREET 1:(?P<street1>.*)'),
    'STREET2': re.compile(r'STREET 2:(?P<street2>.*)'),
    'CITY': re.compile(r'CITY:(?P<city>.*)'),
    'STATE': re.compile(r'STATE:(?P<state>.*)'),
    'ZIPCODE': re.compile(r'ZIP:(?P<zip>.*)'),
    'BUS_PHONE': re.compile(r'BUSINESS PHONE:(?P<bus_phone>.*)'),
    'FORMER_COMP': re.compile(r'FORMER COMPANY:'),
    'FCOMP_CONFORMEDNAME': re.compile(r'FORMER CONFORMED NAME:(?P<fcomp_name>.*)'),
    'DATE_NAMECHANGE': re.compile(r'DATE OF NAME CHANGE:(?P<date_name_change>.*)'),
    'REPT_MAIL_ADDRESS': re.compile(r'<reportingOwnerAddress>'),
    'REPT_MAIL_STREET1': re.compile(r'<rptOwnerStreet1>(?P<street1>.*)</rptOwnerStreet1>'),
    'REPT_MAIL_STREET2': re.compile(r'<rptOwnerStreet2>(?P<street2>.*)</rptOwnerStreet2>'),
    'REPT_MAIL_CITY': re.compile(r'<rptOwnerCity>(?P<city>.*)</rptOwnerCity>'),
    'REPT_MAIL_STATE': re.compile(r'<rptOwnerState>(?P<state>.*)</rptOwnerState>'),
    'REPT_MAIL_ZIPCODE': re.compile(r'<rptOwnerZipCode>(?P<zip>.*)</rptOwnerZipCode>'),
    'REPT_MAIL_STATETXT': re.compile(r'<rptOwnerStateDescription>(?P<state_txt>.*)</rptOwnerStateDescription>'),
    'END_REPT_MAIL_ADDRESS': re.compile(r'</reportingOwnerAddress>'),
    'REPTOWN_RELATION': re.compile(r'<reportingOwnerRelationship>'),
    'DIRECTOR': re.compile(r'<isDirector>(?P<is_director>.*)</isDirector>'),
    'OFFICER': re.compile(r'<isOfficer>(?P<is_officer>.*)</isOfficer>'),
    'TENPERCENTOWNER': re.compile(r'<isTenPercentOwner>(?P<is_tenpercent>.*)</isTenPercentOwner>'),
    'OTHER': re.compile(r'<isOther>(?P<is_other>.*)</isOther>'),
    'TEXT_OTHER': re.compile(r'<otherText>(?P<otherText>.*)</otherText>'),
    'OFFICER_TITLE': re.compile(r'<officerTitle>(?P<off_title>.*)</officerTitle>'),
    'END_REPTOWN_RELATION': re.compile(r'</reportingOwnerRelationship>'),
    'NDH': re.compile(r'<nonDerivativeHolding>'),
    'SECURITY_TYPETITLE': re.compile(r'<securityTitle>'),
    'END_SECURITY_TYPETITLE': re.compile(r'</securityTitle>'),
    'SHARES': re.compile(r'<sharesOwnedFollowingTransaction>'),
    'END_SHARES': re.compile(r'</sharesOwnedFollowingTransaction>'),
    'SHARE_VALUE': re.compile(r'<valueOwnedFollowingTransaction>'),
    'END_SHARE_VALUE': re.compile(r'</valueOwnedFollowingTransaction>'),
    'OWNERSHIPTYPE': re.compile(r'<directOrIndirectOwnership>'),
    'END_OWNERSHIPTYPE': re.compile(r'</directOrIndirectOwnership>'),
    'INDBENF_OWNER': re.compile(r'<natureOfOwnership>'),
    'END_INDBENF_OWNER': re.compile(r'</natureOfOwnership>'),
    'END_NDH': re.compile(r'</nonDerivativeHolding>'),
    'VALUE': re.compile(r'<value>(?P<value>.*)</value>'),
    'FTNOTE_ID': re.compile(r'<footnoteId id="(?P<ftnote_id>.*)"/>'),
    'DH': re.compile(r'<derivativeHolding>'),
    'DERIVSECURITY_TYPETITLE': re.compile(r'<securityTitle>'),
    'END_DERIVSECURITY_TYPETITLE': re.compile(r'</securityTitle>'),
    'EXPRICE_DERVSECURTY': re.compile(r'<conversionOrExercisePrice>'),
    'END_EXPRICE_DERVSECURTY': re.compile(r'</conversionOrExercisePrice>'),
    'DATE_EXCISE': re.compile(r'<exerciseDate>'),
    'END_DATE_EXCISE': re.compile(r'</exerciseDate>'),
    'DATE_EXPIRE': re.compile(r'<expirationDate>'),
    'END_DATE_EXPIRE': re.compile(r'</expirationDate>'),
    'UNDERSECURITY_TYPETITLE': re.compile(r'<underlyingSecurityTitle>'),
    'END_UNDERSECURITY_TYPETITLE': re.compile(r'</underlyingSecurityTitle>'),
    'SHARE_AMOUNT': re.compile(r'<underlyingSecurityShares>'),
    'END_SHARE_AMOUNT': re.compile(r'</underlyingSecurityShares>'),
    'END_DH': re.compile(r'</derivativeHolding>'),
    'FOOTNOTE': re.compile(r'<footnote id=\"(?P<id>.*)\">(?P<txt>.*)</footnote>'),
}

def parse_line_form3(line, func_time):
    if time.time() - func_time > 30:
        raise TimeoutException(line)
    for key, rx in rx_3.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None

def parse_and_upload_form3(session, cik, filename):
    func_time = time.time()
    ZSECFORM3_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'ACCEPT_TIME': None, 'CIK_ISSUER': None,
        'FORM_TYPE': None, 'ISSUER_SYMBOL': None, 'SEC_HEADER': None, 'DOC_FILE_COUNT': None, 'REPORT_PERIOD': None,
        'DATE_FILED': None, 'DATE_CHANGED': None, 'VERSION': None, 'FILENAME': None, 'FILEDESCRIP': None, 'XML_VERSION': None,
        'SCHEMA_VERSION': None, 'SECTION_16': None, 'SIGN_TITLE': None, 'SIGN_NAME': None, 'SIGN_DATE': None, 'DERV_TAB': False,
        'NDERV_TAB': False, 'FTNOTE_FLG': False, 'ERDAT': None, 'ERNAME': None}
    ZSECFORM3_ISSUER_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'CIK_ISSUER': None,
        'FORM_TYPE': None, 'ISSUER_SYMBOL': None, 'ISSU_CONFDNAME': None, 'SIC': None, 'IRS': None, 'STATE_INCORP': None,
        'FISCAL_YEAREND': None, 'BUS_STREET1': None, 'BUS_STREET2': None, 'BUS_CITY': None, 'BUS_STATE': None, 'BUS_STATETXT': None, 
        'BUS_ZIPCODE': None, 'BUS_PHONE': None, 'MAIL_STREET1': None, 'MAIL_STREET2': None, 'MAIL_CITY': None, 'MAIL_STATE': None, 
        'MAIL_STATETXT': None, 'MAIL_ZIPCODE': None, 'FCOMP_CONFORMEDNAME1': None, 'DATE_NAMECHANGE1': None, 
        'FCOMP_CONFORMEDNAME2': None, 'DATE_NAMECHANGE2': None, 'FCOMP_CONFORMEDNAME3': None, 'DATE_NAMECHANGE3': None,}
    ZSECFORM3_REPTER_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'CIK_REPORTER': None, 'DATE_REPORT': None,
        'FORM_TYPE': None, 'REPT_CONFDNAME': None, 'FIRST_NAME': None, 'LAST_NAME': None, 'MIDDLE_NAME': None, 
        'OFFICER_TITLE': None, 'SEC_ACT': None, 'SEC_FILENO': None, 'FILM_NO': None, 'BUS_STREET1': None, 'BUS_STREET2': None, 
        'BUS_CITY': None, 'BUS_STATE': None, 'BUS_STATETXT': None, 'BUS_ZIPCODE': None, 'BUS_PHONE': None, 'MAIL_STREET1': None, 
        'MAIL_STREET2': None, 'MAIL_CITY': None, 'MAIL_STATE': None, 'MAIL_STATETXT': None, 'MAIL_ZIPCODE': None, 
        'FCOMP_CONFORMEDNAME': None, 'DATE_NAMECHANGE': None, 'DIRECTOR': None, 'OFFICER': None, 'TENPERCENTOWNER': None, 
        'OTHER': None, 'TEXT_OTHER': None, 'SIGN_TITLE': None, 'SIGN_NAME': None, 'SIGN_DATE': None,}
    ZSECFORM3_DTAB_arr = []
    ZSECFORM3_NDTAB_arr = []
    ZSECFORM3_FTNOTE_arr = [] 
    form_comp_count = ndh_index = dh_index = 1
    with open(f"companies/{cik}/{filename}", 'r') as file:
        line = file.readline()
        while line:
            key, match = parse_line_form3(line, func_time)
            if not key:
                line = file.readline()
                continue
            elif key == 'ACCESSIONNO':
                ZSECFORM3_dict['ACCESSIONNO'] = match.group('accession_no').strip()
                ZSECFORM3_ISSUER_dict['ACCESSIONNO'] = match.group('accession_no').strip()
                ZSECFORM3_REPTER_dict['ACCESSIONNO'] = match.group('accession_no').strip()
            elif key == 'SEC_DOC':
                ZSECFORM3_dict['SEC_DOC'] = match.group('sec_doc').strip()
                ZSECFORM3_ISSUER_dict['SEC_DOC'] = match.group('sec_doc').strip()
                ZSECFORM3_REPTER_dict['SEC_DOC'] = match.group('sec_doc').strip()
            elif key == 'ACCEPT_TIME':
                ZSECFORM3_dict['ACCEPT_TIME'] = match.group('accept_time').strip()
            elif key == 'FORM_TYPE':
                ZSECFORM3_dict['FORM_TYPE'] = match.group('form_type').strip()
                ZSECFORM3_ISSUER_dict['FORM_TYPE'] = match.group('form_type').strip()
                ZSECFORM3_REPTER_dict['FORM_TYPE'] = match.group('form_type').strip()
            elif key == 'SEC_HEADER':
                ZSECFORM3_dict['SEC_HEADER'] = match.group('sec_header').strip()
            elif key == 'DOC_FILE_COUNT':
                ZSECFORM3_dict['DOC_FILE_COUNT'] = match.group('doc_count').strip()
            elif key == 'REPORT_PERIOD':
                ZSECFORM3_dict['REPORT_PERIOD'] = match.group('report_period').strip()
            elif key == 'DATE_FILED':
                ZSECFORM3_dict['DATE_FILED'] = match.group('filed_date').strip()
                # date_report = datetime.strptime(ZSECFORM3_dict['DATE_FILED'], '%Y%m%d')
                # ZSECFORM3_REPTER_dict['DATE_REPORT'] = date_report.strftime('%Y-%m-%d')
            elif key == 'DATE_CHANGED':
                ZSECFORM3_dict['DATE_CHANGED'] = match.group('change_date').strip()
            elif key == 'ISSUER':
                while key != 'REPORTER' and key != 'END_SEC_HEADER':
                    key, match = parse_line_form3(line, func_time)
                    if key == 'CIK':
                        ZSECFORM3_dict['CIK_ISSUER'] = match.group('cik').strip()
                        ZSECFORM3_ISSUER_dict['CIK_ISSUER'] = match.group('cik').strip()
                    elif key == 'CONFDNAME':
                        ZSECFORM3_ISSUER_dict['ISSU_CONFDNAME'] = match.group('comp_name').strip()
                    elif key == 'SIC':
                        ZSECFORM3_ISSUER_dict['SIC'] = match.group('sic').strip()
                    elif key == 'IRS':
                        ZSECFORM3_ISSUER_dict['IRS'] = match.group('irs').strip()
                    elif key == 'STATE_INCORP':
                        ZSECFORM3_ISSUER_dict['STATE_INCORP'] = match.group('state_inc').strip()
                    elif key == 'FISCAL_YEAREND':
                        ZSECFORM3_ISSUER_dict['FISCAL_YEAREND'] = match.group('fiscal_year').strip()
                    elif key == 'BUS_ADDR':
                        while key != 'END_SEC_HEADER' and key != None:
                            key, match = parse_line_form3(line, func_time)
                            if key == 'STREET1':
                                ZSECFORM3_ISSUER_dict['BUS_STREET1'] = match.group('street1').strip()
                            elif key == 'STREET2':
                                ZSECFORM3_ISSUER_dict['BUS_STREET2'] = match.group('street2').strip()
                            elif key == 'CITY':
                                ZSECFORM3_ISSUER_dict['BUS_CITY'] = match.group('city').strip()
                            elif key == 'STATE':
                                ZSECFORM3_ISSUER_dict['BUS_STATE'] = match.group('state').strip()
                            elif key == 'ZIPCODE':
                                ZSECFORM3_ISSUER_dict['BUS_ZIPCODE'] = match.group('zip').strip()
                            elif key == 'BUS_PHONE':
                                ZSECFORM3_ISSUER_dict['BUS_PHONE'] = match.group('bus_phone').strip()
                            line = file.readline()
                    elif key == 'MAIL_ADDR':
                        while key != 'END_SEC_HEADER' and key != None:
                            key, match = parse_line_form3(line, func_time)
                            if key == 'STREET1':
                                ZSECFORM3_ISSUER_dict['MAIL_STREET1'] = match.group('street1').strip()
                            elif key == 'STREET2':
                                ZSECFORM3_ISSUER_dict['MAIL_STREET2'] = match.group('street2').strip()
                            elif key == 'CITY':
                                ZSECFORM3_ISSUER_dict['MAIL_CITY'] = match.group('city').strip()
                            elif key == 'STATE':
                                ZSECFORM3_ISSUER_dict['MAIL_STATE'] = match.group('state').strip()
                            elif key == 'ZIPCODE':
                                ZSECFORM3_ISSUER_dict['MAIL_ZIPCODE'] = match.group('zip').strip()
                            line = file.readline()
                    elif key == 'FORMER_COMP':
                        while key != 'END_SEC_HEADER' and key != None:
                            key, match = parse_line_form3(line, func_time)
                            if key == 'FCOMP_CONFORMEDNAME':
                                ZSECFORM3_ISSUER_dict[f'FCOMP_CONFORMEDNAME{form_comp_count}'] = match.group('fcomp_name').strip()
                            elif key == 'DATE_NAMECHANGE':
                                ZSECFORM3_ISSUER_dict[f'DATE_NAMECHANGE{form_comp_count}'] = match.group('date_name_change').strip()
                            line = file.readline()
                        form_comp_count += 1
                    line = file.readline()
            elif key == 'REPORTER':
                while key != 'ISSUER' and key != 'END_SEC_HEADER':
                    key, match = parse_line_form3(line, func_time)
                    if key == 'CIK':
                        ZSECFORM3_REPTER_dict['CIK_REPORTER'] = match.group('cik').strip()
                    elif key == 'CONFDNAME':
                        ZSECFORM3_REPTER_dict['REPT_CONFDNAME'] = match.group('comp_name').strip()
                    elif key == 'SEC_ACT':
                        ZSECFORM3_REPTER_dict['SEC_ACT'] = match.group('sec_act').strip()
                    elif key == 'SEC_FILENO':
                        ZSECFORM3_REPTER_dict['SEC_FILENO'] = match.group('file_no').strip()
                    elif key == 'FILM_NO':
                        ZSECFORM3_REPTER_dict['FILM_NO'] = match.group('film_no').strip()
                    elif key == 'BUS_ADDR':
                        while key != 'END_SEC_HEADER' and key != None:
                            key, match = parse_line_form3(line, func_time)
                            if key == 'STREET1':
                                ZSECFORM3_REPTER_dict['BUS_STREET1'] = match.group('street1').strip()
                            elif key == 'STREET2':
                                ZSECFORM3_REPTER_dict['BUS_STREET2'] = match.group('street2').strip()
                            elif key == 'CITY':
                                ZSECFORM3_REPTER_dict['BUS_CITY'] = match.group('city').strip()
                            elif key == 'STATE':
                                ZSECFORM3_REPTER_dict['BUS_STATE'] = match.group('state').strip()
                            elif key == 'ZIPCODE':
                                ZSECFORM3_REPTER_dict['BUS_ZIPCODE'] = match.group('zip').strip()
                            elif key == 'BUS_PHONE':
                                ZSECFORM3_REPTER_dict['BUS_PHONE'] = match.group('bus_phone').strip()
                            line = file.readline()
                    elif key == 'FORMER_COMP':
                        if not ZSECFORM3_REPTER_dict['FCOMP_CONFORMEDNAME']:
                            while key != 'END_SEC_HEADER' and key != None:
                                key, match = parse_line_form3(line, func_time)
                                if key == 'FCOMP_CONFORMEDNAME':
                                    ZSECFORM3_REPTER_dict['FCOMP_CONFORMEDNAME'] = match.group('fcomp_name').strip()
                                elif key == 'DATE_NAMECHANGE':
                                    ZSECFORM3_REPTER_dict['DATE_NAMECHANGE'] = match.group('date_name_change').strip()
                                line = file.readline()
                    line = file.readline()
            elif key == 'FILENAME':
                ZSECFORM3_dict['FILENAME'] = match.group('filename').strip()
                line = file.readline()
                key, match = parse_line_form3(line, func_time)
                if key == 'FILEDESCRIP':
                    ZSECFORM3_dict['FILEDESCRIP'] = match.group('filedescrip').strip()
            elif key == 'XML_VERSION':
                ZSECFORM3_dict['XML_VERSION'] = match.group('xml_version').strip()
            elif key == 'SCHEMA_VERSION':
                ZSECFORM3_dict['SCHEMA_VERSION'] = match.group('schema').strip()
            elif key == 'DATE_REPORT':
                ZSECFORM3_REPTER_dict['DATE_REPORT'] = match.group('date_report').strip()
            elif key == 'ISSUER_SYMBOL':
                ZSECFORM3_dict['ISSUER_SYMBOL'] = match.group('iss_symbol').strip()
                ZSECFORM3_ISSUER_dict['ISSUER_SYMBOL'] = match.group('iss_symbol').strip()
            elif key == 'SIGN_BLOCK':
                while key != 'END_SIGN_BLOCK':
                    key, match = parse_line_form3(line, func_time)
                    if key == 'SIGN_TITLE':
                        ZSECFORM3_dict['SIGN_TITLE'] = match.group('sign_title').strip()
                        ZSECFORM3_REPTER_dict['SIGN_TITLE'] = match.group('sign_title').strip()
                    elif key == 'SIGN_NAME':
                        ZSECFORM3_dict['SIGN_NAME'] = match.group('sign_name').strip()
                        ZSECFORM3_REPTER_dict['SIGN_NAME'] = match.group('sign_name').strip()
                    elif key == 'SIGN_DATE':
                        ZSECFORM3_dict['SIGN_DATE'] = match.group('sign_date').strip()
                        ZSECFORM3_REPTER_dict['SIGN_DATE'] = match.group('sign_date').strip()
                    line = file.readline()
            elif key == 'REPT_MAIL_ADDRESS':
                while key != 'END_REPT_MAIL_ADDRESS':
                    key, match = parse_line_form3(line, func_time)
                    if key == 'REPT_MAIL_STREET1':
                        ZSECFORM3_REPTER_dict['MAIL_STREET1'] = match.group('street1').strip()
                    elif key == 'REPT_MAIL_STREET2':
                        ZSECFORM3_REPTER_dict['MAIL_STREET2'] = match.group('street2').strip()
                    elif key == 'REPT_MAIL_CITY':
                        ZSECFORM3_REPTER_dict['MAIL_CITY'] = match.group('city').strip()
                    elif key == 'REPT_MAIL_STATE':
                        ZSECFORM3_REPTER_dict['MAIL_STATE'] = match.group('state').strip()
                    elif key == 'REPT_MAIL_ZIPCODE':
                        ZSECFORM3_REPTER_dict['MAIL_ZIPCODE'] = match.group('zip').strip()
                    elif key == 'REPT_MAIL_STATETXT':
                        ZSECFORM3_REPTER_dict['MAIL_STATETXT'] = match.group('state_txt').strip()
                    line = file.readline()
            elif key == 'REPTOWN_RELATION':
                while key != 'END_REPTOWN_RELATION':
                    key, match = parse_line_form3(line, func_time)
                    if key == 'DIRECTOR':
                        ZSECFORM3_REPTER_dict['DIRECTOR'] = match.group('is_director').strip()
                    elif key == 'OFFICER':
                        ZSECFORM3_REPTER_dict['OFFICER'] = match.group('is_officer').strip()
                    elif key == 'TENPERCENTOWNER':
                        ZSECFORM3_REPTER_dict['TENPERCENTOWNER'] = match.group('is_tenpercent').strip()
                    elif key == 'OTHER':
                        ZSECFORM3_REPTER_dict['OTHER'] = match.group('is_other').strip()
                    elif key == 'TEXT_OTHER':
                        ZSECFORM3_REPTER_dict['TEXT_OTHER'] = match.group('otherText').strip()
                    elif key == 'OFFICER_TITLE':
                        ZSECFORM3_REPTER_dict['OFFICER_TITLE'] = match.group('off_title').strip()
                    line = file.readline()
            elif key == 'NDH':
                ZSECFORM3_NDTAB_dict = {'MANDT': "100", 'ACCESSIONNO': ZSECFORM3_dict['ACCESSIONNO'], 'ACCESS_TRANXID': f"{ndh_index}", 
                                        'SECURITY_TYPETITLE': None, 'SECTITLE_FTNOTE': None, 'FORM_TYPE': ZSECFORM3_dict['FORM_TYPE'], 'SHARES': None, 
                                        'SHARE_FTNOTE': None, 'SHARE_VALUE': None, 'SHAREVALUE_FTNOTE': None, 'OWNERSHIPTYPE': None, 
                                        'OWNSHIP_FTNOTE': None, 'INDBENF_OWNER': None,'INDBENF_OWNER_FTNOTE': None}
                while key != 'END_NDH':
                    key, match = parse_line_form3(line, func_time)
                    if key == 'SECURITY_TYPETITLE':
                        while key != 'END_SECURITY_TYPETITLE':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_NDTAB_dict['SECURITY_TYPETITLE'] = match.group('value').strip()
                            elif key == 'FTNOTE_ID':
                                ZSECFORM3_NDTAB_dict['SECTITLE_FTNOTE'] = match.group('ftnote_id').strip()
                            line = file.readline()
                    elif key == 'SHARES':
                        while key != 'END_SHARES':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_NDTAB_dict['SHARES'] = match.group('value').strip()
                            elif key == 'FTNOTE_ID':
                                ZSECFORM3_NDTAB_dict['SHARE_FTNOTE'] = match.group('ftnote_id').strip()
                            line = file.readline()
                    elif key == 'SHARE_VALUE':
                        while key != 'END_SHARE_VALUE':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_NDTAB_dict['SHARE_VALUE'] = match.group('value').strip()
                            elif key == 'FTNOTE_ID':
                                ZSECFORM3_NDTAB_dict['SHAREVALUE_FTNOTE'] = match.group('ftnote_id').strip()
                            line = file.readline()
                    elif key == 'OWNERSHIPTYPE':
                        while key != 'END_OWNERSHIPTYPE':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_NDTAB_dict['OWNERSHIPTYPE'] = match.group('value').strip()
                            elif key == 'FTNOTE_ID':
                                ZSECFORM3_NDTAB_dict['OWNSHIP_FTNOTE'] = match.group('ftnote_id').strip()
                            line = file.readline()
                    elif key == 'INDBENF_OWNER':
                        while key != 'END_INDBENF_OWNER':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_NDTAB_dict['INDBENF_OWNER'] = match.group('value').strip()
                            elif key == 'FTNOTE_ID':
                                ZSECFORM3_NDTAB_dict['INDBENF_OWNER_FTNOTE'] = match.group('ftnote_id').strip()
                            line = file.readline()
                    line = file.readline()

                ZSECFORM3_NDTAB_arr.append(ZSECFORM3_NDTAB_dict)
                ZSECFORM3_dict['NDERV_TAB'] = True
                ndh_index += 1
            elif key == 'DH':
                ZSECFORM3_DTAB_dict = {'MANDT': "100", 'ACCESSIONNO': ZSECFORM3_dict['ACCESSIONNO'], 'ACCESS_TRANXID': f"{dh_index}", 
                                       'DERIVSECURITY_TYPETITLE': None, 'DATE_EXCISE': None, 'DATE_EXPIRE': None, 
                                       'SECURITY_TYPETITLE': None, 'SHARE_AMOUNT': None, 'EXPRICE_DERVSECURTY': None, 
                                       'OWNERSHIPTYPE': None, 'INDBENF_OWNER': None}
                while key != 'END_DH':
                    key, match = parse_line_form3(line, func_time)
                    if key == 'DERIVSECURITY_TYPETITLE':
                        while key != 'END_DERIVSECURITY_TYPETITLE':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_DTAB_dict['DERIVSECURITY_TYPETITLE'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'EXPRICE_DERVSECURTY':
                        while key != 'END_EXPRICE_DERVSECURTY':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_DTAB_dict['EXPRICE_DERVSECURTY'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'DATE_EXCISE':
                        while key != 'END_DATE_EXCISE':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_DTAB_dict['DATE_EXCISE'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'DATE_EXPIRE':
                        while key != 'END_DATE_EXPIRE':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_DTAB_dict['DATE_EXPIRE'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'UNDERSECURITY_TYPETITLE':
                        while key != 'END_UNDERSECURITY_TYPETITLE':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_DTAB_dict['SECURITY_TYPETITLE'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'SHARE_AMOUNT':
                        while key != 'END_SHARE_AMOUNT':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_DTAB_dict['SHARE_AMOUNT'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'OWNERSHIPTYPE':
                        while key != 'END_OWNERSHIPTYPE':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_DTAB_dict['OWNERSHIPTYPE'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'INDBENF_OWNER':
                        while key != 'END_INDBENF_OWNER':
                            key, match = parse_line_form3(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM3_DTAB_dict['INDBENF_OWNER'] = match.group('value').strip()
                            line = file.readline()
                    line = file.readline()

                ZSECFORM3_DTAB_arr.append(ZSECFORM3_DTAB_dict)
                ZSECFORM3_dict['DERV_TAB'] = True
                dh_index += 1
            elif key == 'FOOTNOTE':
                ZSECFORM3_dict['FTNOTE_FLG'] = True
                ZSECFORM3_FTNOTE_arr.append({'MANDT': "100", 'ACCESSIONNO': ZSECFORM3_dict['ACCESSIONNO'], 
                                             'SEC_DOC': ZSECFORM3_dict['SEC_DOC'], 'FOOTNOTE_ID': match.group('id').strip(), 
                                             'FOOTNOTE_TXT': match.group('txt').strip()})

            line = file.readline()

    session.add_all([ZSECFORM3(**ZSECFORM3_dict), ZSECFORM3_ISSUER(**ZSECFORM3_ISSUER_dict), ZSECFORM3_REPTER(**ZSECFORM3_REPTER_dict)])
    session.add_all([ZSECFORM3_FTNOTE(**ZSECFORM3_FTNOTE_dict) for ZSECFORM3_FTNOTE_dict in ZSECFORM3_FTNOTE_arr])
    session.add_all([ZSECFORM3_DTAB(**ZSECFORM3_DTAB_dict) for ZSECFORM3_DTAB_dict in ZSECFORM3_DTAB_arr])
    session.add_all([ZSECFORM3_NDTAB(**ZSECFORM3_NDTAB_dict) for ZSECFORM3_NDTAB_dict in ZSECFORM3_NDTAB_arr])
        


rx_4 = {
    'ACCESSIONNO': re.compile(r'ACCESSION NUMBER:(?P<accession_no>.*)'),
    'SEC_DOC': re.compile(r'<sec-document>(?P<sec_doc>.*)'),
    'ACCEPT_TIME': re.compile(r'<acceptance-datetime>(?P<accept_time>.*)'),
    'SEC_HEADER': re.compile(r'<sec-header>(?P<sec_header>.*)'),
    'DOC_FILE_COUNT': re.compile(r'PUBLIC DOCUMENT COUNT:(?P<doc_count>.*)'),
    'REPORT_PERIOD': re.compile(r'CONFORMED PERIOD OF REPORT:(?P<report_period>.*)'),
    'DATE_FILED': re.compile(r'FILED AS OF DATE:(?P<filed_date>.*)'),
    'DATE_CHANGED': re.compile(r'DATE AS OF CHANGE:(?P<change_date>.*)'),
    'REPORTER': re.compile(r'REPORTING-OWNER:'),
    'OWN_DATA': re.compile(r'OWNER DATA:'),
    'ISSUER': re.compile(r'ISSUER:'),
    'COMP_DATA': re.compile(r'COMPANY DATA:'),
    'END_SEC_HEADER': re.compile(r'</sec-header>'),
    'CIK': re.compile(r'CENTRAL INDEX KEY:(?P<cik>.*)'),
    'FORM_TYPE': re.compile(r'CONFORMED SUBMISSION TYPE:(?P<form_type>.*)'),
    'ISSUER_SYMBOL': re.compile(r'<issuertradingsymbol>(?P<issuer_symbol>.*)</issuertradingsymbol>'),
    'SEC_FILENO': re.compile(r'SEC FILE NUMBER:(?P<file_no>.*)'),
    'FILENAME': re.compile(r'<filename>(?P<filename>.*)xml'),
    'FILEDESCRIP': re.compile(r'<description>(?P<filedescrip>.*)'),
    'XML_VERSION': re.compile(r'<\?xml version=\"(?P<xml_version>.*)\"'),
    'DATE_REPORT': re.compile(r'<periodofreport>(?P<date_report>.*)</periodofreport>'),
    'SIGN_BLOCK': re.compile(r'<ownersignature>'),
    'SIGN_NAME': re.compile(r'<signaturename>(?P<sign_name>.*)</signaturename>'),
    'TITLE': re.compile(r'Title:(?P<title>.*)'),
    'NAME': re.compile(r'Name:(?P<name>.*)'),
    'SIGN_DATE': re.compile(r'<signaturedate>(?P<sign_date>.*)</signaturedate>'),
    'END_SIGN_BLOCK': re.compile(r'</ownersignature>'),
    'SCHEMA_VERSION': re.compile(r'<schemaversion>(?P<schema>.*)</schemaversion>'),
    'SECTION_16': re.compile(r'<notsubjecttosection16>(?P<section16>.*)</notsubjecttosection16>'),
    'CONFDNAME': re.compile(r'COMPANY CONFORMED NAME:(?P<comp_name>.*)'),
    'SIC': re.compile(r'STANDARD INDUSTRIAL CLASSIFICATION:.*\[(?P<sic>.*)\]'),
    'IRS': re.compile(r'IRS NUMBER:(?P<irs>.*)'),
    'STATE_INCORP': re.compile(r'STATE OF INCORPORATION:(?P<state_inc>.*)'),
    'FISCAL_YEAREND': re.compile(r'FISCAL YEAR END:(?P<fiscal_year>.*)'),
    'SEC_ACT': re.compile(r'SEC ACT:(?P<sec_act>.*)'),
    'FILM_NO': re.compile(r'FILM NUMBER:(?P<film_no>.*)'),
    'BUS_ADDR': re.compile(r'BUSINESS ADDRESS:'),
    'MAIL_ADDR': re.compile(r'MAIL ADDRESS:'), 
    'STREET1': re.compile(r'STREET 1:(?P<street1>.*)'),
    'STREET2': re.compile(r'STREET 2:(?P<street2>.*)'),
    'CITY': re.compile(r'CITY:(?P<city>.*)'),
    'STATE': re.compile(r'STATE:(?P<state>.*)'),
    'ZIPCODE': re.compile(r'ZIP:(?P<zip>.*)'),
    'BUS_PHONE': re.compile(r'BUSINESS PHONE:(?P<bus_phone>.*)'),
    'FORMER_COMP': re.compile(r'FORMER COMPANY:'),
    'FCOMP_CONFORMEDNAME': re.compile(r'FORMER CONFORMED NAME:(?P<fcomp_name>.*)'),
    'DATE_NAMECHANGE': re.compile(r'DATE OF NAME CHANGE:(?P<date_name_change>.*)'),
    'REPTOWN': re.compile(r'<reportingowner>'),
    'REPTOWN_CIK': re.compile(r'<rptownercik>(?P<cik>.*)</rptownercik>'),
    'REPTOWN_RELATION': re.compile(r'<reportingwwnerrelationship>'),
    'DIRECTOR': re.compile(r'<isdirector>(?P<is_director>.*)</isdirector>'),
    'OFFICER': re.compile(r'<isofficer>(?P<is_officer>.*)</isofficer>'),
    'TENPERCENTOWNER': re.compile(r'<istenpercentowner>(?P<is_tenpercent>.*)</istenpercentowner>'),
    'OTHER': re.compile(r'<isother>(?P<is_other>.*)</isother>'),
    'TEXT_OTHER': re.compile(r'<othertext>(?P<otherText>.*)</othertext>'),
    'OFFICER_TITLE': re.compile(r'<officertitle>(?P<off_title>.*)</officertitle>'),
    'END_REPTOWN_RELATION': re.compile(r'</reportingownerrelationship>'),
    'END_REPTOWN': re.compile(r'</reportingowner>'),
    'NDH': re.compile(r'<nonderivativetransaction>'),
    'SECURITY_TYPETITLE': re.compile(r'<securitytitle>'),
    'END_SECURITY_TYPETITLE': re.compile(r'</securitytitle>'),
    'DATE_TRANS': re.compile(r'<transactiondate>'),
    'DATE_EXECUTION': re.compile(r'<deemedexecutiondate>'),
    'TRANS_FORM_TYPE': re.compile(r'<transactionformtype>(?P<form_type>.*)</transactionformtype>'),
    'TRANS_CODE': re.compile(r'<transactioncode>(?P<trans_code>.*)</transactioncode>'),
    'SWAP': re.compile(r'<equityswapinvolved>(?P<swap>.*)</equityswapinvolved>'),
    'ACQ_DISPOSED': re.compile('<transactionacquireddisposedcode>'),
    'SHARES': re.compile(r'<transactionshares>'),
    'END_SHARES': re.compile(r'</transactionshares>'),
    'SHARE_VALUE': re.compile(r'<transactionpricepershare>'),
    'END_SHARE_VALUE': re.compile(r'</transactionpricepershare>'),
    'SHARES_AFTER': re.compile(r'<sharesownedfollowingtransaction>'),
    'END_SHARES_AFTER': re.compile(r'</sharesownedfollowingtransaction>'),
    'OWNERSHIPTYPE': re.compile(r'<directorindirectownership>'),
    'END_OWNERSHIPTYPE': re.compile(r'</directorindirectownership>'),
    'INDBENF_OWNER': re.compile(r'<natureofownership>'),
    'END_INDBENF_OWNER': re.compile(r'</natureofownership>'),
    'END_NDH': re.compile(r'</nonderivativetransaction>'),
    'VALUE': re.compile(r'<value>(?P<value>.*)</value>'),
    'FTNOTE_ID': re.compile(r'<footnoteid id="(?P<ftnote_id>.*)">'),
    'DH': re.compile(r'<derivativetransaction>'),
    'EXPRICE_DERVSECURTY': re.compile(r'<conversionorexerciseprice>'),
    'END_EXPRICE_DERVSECURTY': re.compile(r'</conversionorexerciseprice>'),
    'DATE_EXCISE': re.compile(r'<exercisedate>'),
    'END_DATE_EXCISE': re.compile(r'</exercisedate>'),
    'DATE_EXPIRE': re.compile(r'<expirationdate>'),
    'END_DATE_EXPIRE': re.compile(r'</expirationdate>'),
    'UNDERSECURITY_TYPETITLE': re.compile(r'<underlyingsecuritytitle>'),
    'END_UNDERSECURITY_TYPETITLE': re.compile(r'</underlyingsecuritytitle>'),
    'END_DH': re.compile(r'</derivativetransaction>'),
    'S_FOOTNOTE': re.compile(r'<footnote id=\"(?P<id>.*)\">(?P<txt>.*)</footnote>'),
    'M_FOOTNOTE': re.compile(r'<footnote id=\"(?P<id>.*)\">(?P<txt>.*)'),
    'END_FOOTNOTE': re.compile(r'(?P<txt>.*)</footnote>'),
}

def parse_line_form4(func_time, line=""):
    if time.time() - func_time > 30:
        raise TimeoutException(line)
    for key, rx in rx_4.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None

def parse_and_upload_form4(session, cik, filename):
    func_time = time.time()
    ZSECFORM4_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'ACCEPT_TIME': None, 'CIK_ISSUER': None,
        'FORM_TYPE': None, 'ISSUER_SYMBOL': None, 'SEC_HEADER': None, 'DOC_FILE_COUNT': None, 'REPORT_PERIOD': None,
        'DATE_FILED': None, 'DATE_CHANGED': None, 'VERSION': None, 'FILENAME': None, 'FILEDESCRIP': None, 'XML_VERSION': None,
        'SCHEMA_VERSION': None, 'SECTION_16': None, 'SIGN_TITLE': None, 'SIGN_NAME': None, 'SIGN_DATE': None, 'DERV_TAB': False,
        'NDERV_TAB': False, 'FTNOTE_FLG': False, 'ERDAT': None, 'ERNAME': None}
    ZSECFORM4_ISSUER_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'CIK_ISSUER': None,
        'FORM_TYPE': None, 'ISSUER_SYMBOL': None, 'ISSU_CONFDNAME': None, 'SIC': None, 'IRS': None, 'STATE_INCORP': None,
        'FISCAL_YEAREND': None, 'BUS_STREET1': None, 'BUS_STREET2': None, 'BUS_CITY': None, 'BUS_STATE': None, 'BUS_STATETXT': None, 
        'BUS_ZIPCODE': None, 'BUS_PHONE': None, 'MAIL_STREET1': None, 'MAIL_STREET2': None, 'MAIL_CITY': None, 'MAIL_STATE': None, 
        'MAIL_STATETXT': None, 'MAIL_ZIPCODE': None, 'FCOMP_CONFORMEDNAME1': None, 'DATE_NAMECHANGE1': None, 
        'FCOMP_CONFORMEDNAME2': None, 'DATE_NAMECHANGE2': None, 'FCOMP_CONFORMEDNAME3': None, 'DATE_NAMECHANGE3': None,}
    ZSECFORM4_REPTER_common_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'DATE_REPORT': None, 'FORM_TYPE': None}
    ZSECFORM4_REPTER_arr = []
    ZSECFORM4_DTAB_arr = []
    ZSECFORM4_NDTAB_arr = []
    ZSECFORM4_FTNOTE_arr = [] 
    form_comp_count = ndh_index = dh_index = 1
    with open(f"companies/{cik}/{filename}", 'r') as file:
        content = file.read()
        lines = content.splitlines()
        file.close()
    
    i = 0
    while i < len(lines):
        key, match = parse_line_form4(func_time, lines[i].strip())
        if not key:
            i += 1
            continue
        
        elif key == 'ACCESSIONNO':
            ZSECFORM4_dict['ACCESSIONNO'] = match.group('accession_no').strip()
            ZSECFORM4_ISSUER_dict['ACCESSIONNO'] = match.group('accession_no').strip()
            ZSECFORM4_REPTER_common_dict['ACCESSIONNO'] = match.group('accession_no').strip()
        
        elif key == 'SEC_DOC':
            ZSECFORM4_dict['SEC_DOC'] = match.group('sec_doc').strip()
            ZSECFORM4_ISSUER_dict['SEC_DOC'] = match.group('sec_doc').strip()
            ZSECFORM4_REPTER_common_dict['SEC_DOC'] = match.group('sec_doc').strip()
        
        elif key == 'ACCEPT_TIME': ZSECFORM4_dict['ACCEPT_TIME'] = match.group('accept_time').strip()
        
        elif key == 'FORM_TYPE':
            ZSECFORM4_dict['FORM_TYPE'] = match.group('form_type').strip()
            ZSECFORM4_ISSUER_dict['FORM_TYPE'] = match.group('form_type').strip()
            ZSECFORM4_REPTER_common_dict['FORM_TYPE'] = match.group('form_type').strip()
        
        elif key == 'SEC_HEADER': ZSECFORM4_dict['SEC_HEADER'] = match.group('sec_header').strip()
        
        elif key == 'DOC_FILE_COUNT': ZSECFORM4_dict['DOC_FILE_COUNT'] = match.group('doc_count').strip()
        
        elif key == 'REPORT_PERIOD': ZSECFORM4_dict['REPORT_PERIOD'] = match.group('report_period').strip()
        
        elif key == 'DATE_FILED': ZSECFORM4_dict['DATE_FILED'] = match.group('filed_date').strip()
        
        elif key == 'DATE_CHANGED': ZSECFORM4_dict['DATE_CHANGED'] = match.group('change_date').strip()
        
        elif key == 'COMP_DATA':
            while key != 'END_SEC_HEADER' and key != 'REPORTER':
                key, match = parse_line_form4(func_time, lines[i].strip())
                if key == 'BUS_ADDR':
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'STREET1': ZSECFORM4_ISSUER_dict['BUS_STREET1'] = match.group('street1').strip()
                        elif key == 'STREET2': ZSECFORM4_ISSUER_dict['BUS_STREET2'] = match.group('street2').strip()
                        elif key == 'CITY': ZSECFORM4_ISSUER_dict['BUS_CITY'] = match.group('city').strip()
                        elif key == 'STATE': ZSECFORM4_ISSUER_dict['BUS_STATE'] = match.group('state').strip()
                        elif key == 'ZIPCODE': ZSECFORM4_ISSUER_dict['BUS_ZIPCODE'] = match.group('zip').strip()
                        elif key == 'BUS_PHONE': ZSECFORM4_ISSUER_dict['BUS_PHONE'] = match.group('bus_phone').strip()
                        i += 1
                    i -= 1 
                
                elif key == 'MAIL_ADDR':
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'STREET1': ZSECFORM4_ISSUER_dict['MAIL_STREET1'] = match.group('street1').strip()
                        elif key == 'STREET2': ZSECFORM4_ISSUER_dict['MAIL_STREET2'] = match.group('street2').strip()
                        elif key == 'CITY': ZSECFORM4_ISSUER_dict['MAIL_CITY'] = match.group('city').strip()
                        elif key == 'STATE': ZSECFORM4_ISSUER_dict['MAIL_STATE'] = match.group('state').strip()
                        elif key == 'ZIPCODE': ZSECFORM4_ISSUER_dict['MAIL_ZIPCODE'] = match.group('zip').strip()
                        i += 1 
                    i -= 1
                
                elif key == 'FORMER_COMP' and form_comp_count <= 3:
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'FCOMP_CONFORMEDNAME': ZSECFORM4_ISSUER_dict[f'FCOMP_CONFORMEDNAME{form_comp_count}'] = match.group('fcomp_name').strip()
                        elif key == 'DATE_NAMECHANGE': ZSECFORM4_ISSUER_dict[f'DATE_NAMECHANGE{form_comp_count}'] = match.group('date_name_change').strip()
                        i += 1 
                    form_comp_count += 1
                    i -= 1

                elif key == 'CIK':
                    ZSECFORM4_dict['CIK_ISSUER'] = match.group('cik').strip()
                    ZSECFORM4_ISSUER_dict['CIK_ISSUER'] = match.group('cik').strip()
                
                elif key == 'CONFDNAME': ZSECFORM4_ISSUER_dict['ISSU_CONFDNAME'] = match.group('comp_name').strip()
                
                elif key == 'SIC': ZSECFORM4_ISSUER_dict['SIC'] = match.group('sic').strip()
                
                elif key == 'IRS': ZSECFORM4_ISSUER_dict['IRS'] = match.group('irs').strip()
                
                elif key == 'STATE_INCORP': ZSECFORM4_ISSUER_dict['STATE_INCORP'] = match.group('state_inc').strip()
                
                elif key == 'FISCAL_YEAREND': ZSECFORM4_ISSUER_dict['FISCAL_YEAREND'] = match.group('fiscal_year').strip()
                
                i += 1 

        elif key == 'OWN_DATA':
            ZSECFORM4_REPTER_dict = {'MANDT': "100", 'CIK_REPORTER': None, 'REPT_CONFDNAME': None, 'FIRST_NAME': None, 
                                     'LAST_NAME': None, 'MIDDLE_NAME': None, 'OFFICER_TITLE': None, 'SEC_ACT': None, 'SEC_FILENO': None, 
                                     'FILM_NO': None, 'BUS_STREET1': None, 'BUS_STREET2': None, 'BUS_CITY': None, 'BUS_STATE': None, 
                                     'BUS_STATETXT': None, 'BUS_ZIPCODE': None, 'BUS_PHONE': None, 'MAIL_STREET1': None, 'MAIL_STREET2': None, 
                                     'MAIL_CITY': None, 'MAIL_STATE': None, 'MAIL_STATETXT': None, 'MAIL_ZIPCODE': None, 
                                     'FCOMP_CONFORMEDNAME': None, 'DATE_NAMECHANGE': None, 'DIRECTOR': None, 'OFFICER': None, 
                                     'TENPERCENTOWNER': None, 'OTHER': None, 'TEXT_OTHER': None, 'SIGN_TITLE': None, 'SIGN_NAME': None, 
                                     'SIGN_DATE': None,}
            while  key != 'ISSUER' and key != 'END_SEC_HEADER' and key != 'REPORTER':
                key, match = parse_line_form4(func_time, lines[i].strip())

                if key == 'BUS_ADDR':
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'STREET1': ZSECFORM4_REPTER_dict['BUS_STREET1'] = match.group('street1').strip()
                        elif key == 'STREET2': ZSECFORM4_REPTER_dict['BUS_STREET2'] = match.group('street2').strip()
                        elif key == 'CITY': ZSECFORM4_REPTER_dict['BUS_CITY'] = match.group('city').strip()
                        elif key == 'STATE': ZSECFORM4_REPTER_dict['BUS_STATE'] = match.group('state').strip()
                        elif key == 'ZIPCODE': ZSECFORM4_REPTER_dict['BUS_ZIPCODE'] = match.group('zip').strip()
                        elif key == 'BUS_PHONE': ZSECFORM4_REPTER_dict['BUS_PHONE'] = match.group('bus_phone').strip()
                        i += 1
                    i -= 1
                
                elif key == 'MAIL_ADDR':
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'STREET1': ZSECFORM4_REPTER_dict['MAIL_STREET1'] = match.group('street1').strip()
                        elif key == 'STREET2': ZSECFORM4_REPTER_dict['MAIL_STREET2'] = match.group('street2').strip()
                        elif key == 'CITY': ZSECFORM4_REPTER_dict['MAIL_CITY'] = match.group('city').strip()
                        elif key == 'STATE': ZSECFORM4_REPTER_dict['MAIL_STATE'] = match.group('state').strip()
                        elif key == 'ZIPCODE': ZSECFORM4_REPTER_dict['MAIL_ZIPCODE'] = match.group('zip').strip()
                        i += 1
                    i -= 1
                
                elif key == 'FORMER_COMP' and not ZSECFORM4_REPTER_dict['FCOMP_CONFORMEDNAME']:
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'FCOMP_CONFORMEDNAME': ZSECFORM4_REPTER_dict['FCOMP_CONFORMEDNAME'] = match.group('fcomp_name').strip()
                        elif key == 'DATE_NAMECHANGE': ZSECFORM4_REPTER_dict['DATE_NAMECHANGE'] = match.group('date_name_change').strip()
                        i += 1
                    i -= 1

                elif key == 'CIK': ZSECFORM4_REPTER_dict['CIK_REPORTER'] = match.group('cik').strip()
                
                elif key == 'CONFDNAME': ZSECFORM4_REPTER_dict['REPT_CONFDNAME'] = match.group('comp_name').strip()
                
                elif key == 'SEC_ACT': ZSECFORM4_REPTER_dict['SEC_ACT'] = match.group('sec_act').strip()
                
                elif key == 'SEC_FILENO': ZSECFORM4_REPTER_dict['SEC_FILENO'] = match.group('file_no').strip()
                
                elif key == 'FILM_NO': ZSECFORM4_REPTER_dict['FILM_NO'] = match.group('film_no').strip()
                
                i += 1

            ZSECFORM4_REPTER_arr.append(ZSECFORM4_REPTER_dict)

        elif key == 'FILENAME':
            ZSECFORM4_dict['FILENAME'] = match.group('filename').strip()
            i += 1
            key, match = parse_line_form4(func_time, lines[i].strip())
            if key == 'FILEDESCRIP': ZSECFORM4_dict['FILEDESCRIP'] = match.group('filedescrip').strip()
            else: continue
        
        elif key == 'XML_VERSION': ZSECFORM4_dict['XML_VERSION'] = match.group('xml_version').strip()
        
        elif key == 'SCHEMA_VERSION': ZSECFORM4_dict['SCHEMA_VERSION'] = match.group('schema').strip()

        elif key == 'SECTION_16': ZSECFORM4_dict['SECTION_16'] = match.group('section16').strip()
        
        elif key == 'DATE_REPORT': ZSECFORM4_REPTER_common_dict['DATE_REPORT'] = match.group('date_report').strip()
        
        elif key == 'ISSUER_SYMBOL':
            ZSECFORM4_dict['ISSUER_SYMBOL'] = match.group('issuer_symbol').strip()
            ZSECFORM4_ISSUER_dict['ISSUER_SYMBOL'] = match.group('issuer_symbol').strip()

        elif key == 'REPTOWN':
            while key != 'END_REPTOWN':
                key, match = parse_line_form4(func_time, lines[i].strip())
                if key == 'REPTOWN_CIK':
                    reptown_cik = match.group('cik').strip()
                    if len(ZSECFORM4_REPTER_arr) > 1: index = next((ix for (ix, d) in enumerate(ZSECFORM4_REPTER_arr) if d["CIK_REPORTER"] == reptown_cik), None)
                    else: index = 0
                    if isinstance(index, int) and index >= 0:
                        while key != 'END_REPTOWN_RELATION':
                            key, match = parse_line_form4(func_time, lines[i].strip())
                            if key == 'DIRECTOR': ZSECFORM4_REPTER_arr[index]['DIRECTOR'] = match.group('is_director').strip()
                            elif key == 'OFFICER': ZSECFORM4_REPTER_arr[index]['OFFICER'] = match.group('is_officer').strip()
                            elif key == 'TENPERCENTOWNER': ZSECFORM4_REPTER_arr[index]['TENPERCENTOWNER'] = match.group('is_tenpercent').strip()
                            elif key == 'OTHER': ZSECFORM4_REPTER_arr[index]['OTHER'] = match.group('is_other').strip()
                            elif key == 'TEXT_OTHER': ZSECFORM4_REPTER_arr[index]['TEXT_OTHER'] = match.group('otherText').strip()
                            elif key == 'OFFICER_TITLE': ZSECFORM4_REPTER_arr[index]['OFFICER_TITLE'] = match.group('off_title').strip()
                            i += 1
                        i -= 1
                
                i += 1
        
        elif key == 'NDH':
            ZSECFORM4_NDTAB_dict = {'MANDT': "100", 'ACCESSIONNO': ZSECFORM4_dict['ACCESSIONNO'], 'ACCESS_TRANXID': f"{ndh_index}", 
                                    'DATE_TRANS': None, 'DATE_EXECUTION': None, 'TRANS_CODE': None, 'TRANSCODE_FTNOTE': None,
                                    'FORM_TYPE': None, 'SECURITY_TYPETITLE': None, 'SECTITLE_FTNOTE': None, 
                                    'SWAP': None, 'SHARES': None, 'SHARE_FTNOTE': None, 'ACQ_DISPOSED': None, 'SHARE_VALUE': None, 
                                    'SHAREVALUE_FTNOTE': None,  'SHARES_AFTER': None, 'SHAREAFT_FTNOTE': None,'OWNERSHIPTYPE': None, 
                                    'OWNSHIP_FTNOTE': None, 'INDBENF_OWNER': None,'INDBENF_OWNER_FTNOTE': None}
            while key != 'END_NDH':
                key, match = parse_line_form4(func_time, lines[i].strip())
                footnote_arr = []
                if key == 'SECURITY_TYPETITLE':
                    while key != 'END_SECURITY_TYPETITLE':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM4_NDTAB_dict['SECURITY_TYPETITLE'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM4_NDTAB_dict['SECTITLE_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'DATE_TRANS':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_NDTAB_dict['DATE_TRANS'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'DATE_EXECUTION':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_NDTAB_dict['DATE_EXECUTION'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'DATE_EXCISE':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_NDTAB_dict['DATE_EXCISE'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'DATE_EXPIRE':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_NDTAB_dict['DATE_EXPIRE'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'TRANS_FORM_TYPE': ZSECFORM4_NDTAB_dict['FORM_TYPE'] = match.group('form_type').strip()
                
                elif key == 'TRANS_CODE': ZSECFORM4_NDTAB_dict['TRANS_CODE'] = match.group('trans_code').strip()
                
                elif key == 'SWAP': ZSECFORM4_NDTAB_dict['SWAP'] = match.group('swap').strip()
                
                elif key == 'ACQ_DISPOSED':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_NDTAB_dict['ACQ_DISPOSED'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'SHARES':
                    while key != 'END_SHARES':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM4_NDTAB_dict['SHARES'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM4_NDTAB_dict['SHARE_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'SHARE_VALUE':
                    while key != 'END_SHARE_VALUE':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM4_NDTAB_dict['SHARE_VALUE'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM4_NDTAB_dict['SHAREVALUE_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'SHARES_AFTER':
                    while key != 'END_SHARES_AFTER':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM4_NDTAB_dict['SHARES_AFTER'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM4_NDTAB_dict['SHAREAFT_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'OWNERSHIPTYPE':
                    while key != 'END_OWNERSHIPTYPE':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM4_NDTAB_dict['OWNERSHIPTYPE'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM4_NDTAB_dict['OWNSHIP_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'INDBENF_OWNER':
                    while key != 'END_INDBENF_OWNER':
                        key, match = parse_line_form4(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM4_NDTAB_dict['INDBENF_OWNER'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM4_NDTAB_dict['INDBENF_OWNER_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1
                    
                i += 1

            ZSECFORM4_NDTAB_arr.append(ZSECFORM4_NDTAB_dict)
            ZSECFORM4_dict['NDERV_TAB'] = True
            ndh_index += 1
            i -= 1

        elif key == 'DH':
            ZSECFORM4_DTAB_dict = {'MANDT': "100", 'ACCESSIONNO': ZSECFORM4_dict['ACCESSIONNO'], 'ACCESS_TRANXID': f"{dh_index}",
                                   'DATE_TRANS': None, 'DATE_EXECUTION': None, 'TRANS_CODE': None, 
                                   'FORM_TYPE': None, 'SWAP': None, 'ACQ_DISPOSED':None, 
                                   'DERIVSECURITY_TYPETITLE': None, 'DATE_EXCISE': None, 'DATE_EXPIRE': None, 
                                   'SECURITY_TYPETITLE': None, 'SHARE_AMOUNT': None, 'EXPRICE_DERVSECURTY': None, 
                                   'PRICE_DERIV': None, 'SHARES_AFTER': None, 'OWNERSHIPTYPE': None, 'INDBENF_OWNER': None}

            while key != 'END_DH':
                key, match = parse_line_form4(func_time, lines[i].strip())
                if key == 'SECURITY_TYPETITLE':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['DERIVSECURITY_TYPETITLE'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'UNDERSECURITY_TYPETITLE':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['SECURITY_TYPETITLE'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'EXPRICE_DERVSECURTY':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['EXPRICE_DERVSECURTY'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'DATE_TRANS':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['DATE_TRANS'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'DATE_EXECUTION':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['DATE_EXECUTION'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'TRANS_FORM_TYPE': ZSECFORM4_DTAB_dict['FORM_TYPE'] = match.group('form_type').strip()
                
                elif key == 'TRANS_CODE': ZSECFORM4_DTAB_dict['TRANS_CODE'] = match.group('trans_code').strip()
                
                elif key == 'SWAP': ZSECFORM4_DTAB_dict['SWAP'] = match.group('swap').strip()
                
                elif key == 'ACQ_DISPOSED':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['ACQ_DISPOSED'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'SHARES':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['SHARE_AMOUNT'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'SHARE_VALUE':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['PRICE_DERIV'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'SHARES_AFTER':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['SHARES_AFTER'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'OWNERSHIPTYPE':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['OWNERSHIPTYPE'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'INDBENF_OWNER':
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM4_DTAB_dict['INDBENF_OWNER'] = match.group('value').strip()
                    else: i -= 1

                i += 1

            ZSECFORM4_DTAB_arr.append(ZSECFORM4_DTAB_dict)
            ZSECFORM4_dict['DERV_TAB'] = True
            dh_index += 1
            i -= 1

        elif key == 'S_FOOTNOTE':
            ZSECFORM4_dict['FTNOTE_FLG'] = True
            ZSECFORM4_FTNOTE_arr.append({'MANDT': "100", 'ACCESSIONNO': ZSECFORM4_dict['ACCESSIONNO'], 
                                         'SEC_DOC': ZSECFORM4_dict['SEC_DOC'], 'FOOTNOTE_ID': match.group('id').strip(), 
                                         'FOOTNOTE_TXT': match.group('txt').strip()})
      
        elif key == 'M_FOOTNOTE':
            ZSECFORM4_dict['FTNOTE_FLG'] = True
            footnote_id = match.group('id').strip()
            footnote_txt = match.group('txt').strip()
            while key != 'END_FOOTNOTE':
                i += 1
                key, match = parse_line_form4(func_time, lines[i].strip())
                if key != 'END_FOOTNOTE':
                    footnote_txt += f" {lines[i].strip()}"
            footnote_txt += f" {match.group('txt').strip()}"
            ZSECFORM4_FTNOTE_arr.append({'MANDT': "100", 'ACCESSIONNO': ZSECFORM4_dict['ACCESSIONNO'], 
                                         'SEC_DOC': ZSECFORM4_dict['SEC_DOC'], 'FOOTNOTE_ID': footnote_id, 
                                         'FOOTNOTE_TXT': footnote_txt})

        elif key == 'SIGN_BLOCK':
            i += 1
            key, match = parse_line_form4(func_time, lines[i].strip())
            if key == 'SIGN_NAME':
                last_sign_name = match.group('sign_name').strip()
                sign_names = match.group('sign_name').strip().split(",")
                if len(sign_names) == 1:
                    striped_name = sign_names[0].replace('.', '')
                    striped_name = striped_name.replace('/s/', '')
                    striped_name = striped_name.replace(',', '')
                    striped_name = striped_name.replace('/s/', '').strip()
                    name_parts = striped_name.split(" ")
                    if len(name_parts) > 1 and len(name_parts) <= 3:
                        comp_name = f"{name_parts[len(name_parts)-1]} {' '.join(name_parts[:len(name_parts)-1])}"
                    elif len(name_parts) > 3:
                        comp_name = f"{name_parts[2]} {' '.join(name_parts[:2])} {' '.join(name_parts[2:len(name_parts)-1])}"
                    else:
                        name_parts = []
                        comp_name = striped_name    
                else:
                    comp_name = sign_names[0]
                if len(ZSECFORM4_REPTER_arr) > 1: index = next((ix for (ix, d) in enumerate(ZSECFORM4_REPTER_arr) if d["REPT_CONFDNAME"].lower() == comp_name.lower()), None)
                else: index = 0
                if isinstance(index, int) and index >= 0:
                    if len(sign_names) == 1:
                        ZSECFORM4_dict['SIGN_NAME'] = sign_names[0].replace('/s/', '')
                        ZSECFORM4_REPTER_arr[index]['SIGN_NAME'] = sign_names[0].replace('/s/', '')
                        if len(name_parts) == 1:
                            ZSECFORM4_REPTER_arr[index]['FIRST_NAME'] = name_parts[0]
                        elif len(name_parts) == 2:
                            ZSECFORM4_REPTER_arr[index]['FIRST_NAME'] = name_parts[0]
                            ZSECFORM4_REPTER_arr[index]['LAST_NAME'] = name_parts[1]
                        else:
                            ZSECFORM4_REPTER_arr[index]['FIRST_NAME'] = name_parts[0]
                            ZSECFORM4_REPTER_arr[index]['MIDDLE_NAME'] = name_parts[1]
                            ZSECFORM4_REPTER_arr[index]['LAST_NAME'] = name_parts[2]
                    else:
                        ZSECFORM4_dict['SIGN_NAME'] = sign_names[0]
                        ZSECFORM4_REPTER_arr[index]['SIGN_NAME'] = sign_names[0]
                        for sign_name in sign_names:
                            key, match = parse_line_form4(func_time, lines[i].strip())
                            if key == 'TITLE':
                                ZSECFORM4_dict['SIGN_TITLE'] = match.group('title').strip()
                                ZSECFORM4_REPTER_arr[index]['SIGN_TITLE'] = match.group('title').strip()
                            elif key == 'NAME':
                                name = match.group('name').strip().split()
                                if len(name) == 1:
                                    ZSECFORM4_REPTER_arr[index]['FIRST_NAME'] = name[0]
                                elif len(name) == 2:
                                    ZSECFORM4_REPTER_arr[index]['FIRST_NAME'] = name[0]
                                    ZSECFORM4_REPTER_arr[index]['LAST_NAME'] = name[1]
                                else:
                                    ZSECFORM4_REPTER_arr[index]['FIRST_NAME'] = name[0]
                                    ZSECFORM4_REPTER_arr[index]['MIDDLE_NAME'] = name[1]
                                    ZSECFORM4_REPTER_arr[index]['LAST_NAME'] = name[2]
                    i += 1
                    key, match = parse_line_form4(func_time, lines[i].strip())
                    if key == 'SIGN_DATE':
                        ZSECFORM4_dict['SIGN_DATE'] = match.group('sign_date').strip()
                        ZSECFORM4_REPTER_arr[index]['SIGN_DATE'] = match.group('sign_date').strip()
                    else: i -= 1
            
            i -= 1

        i += 1

    for ZSECFORM4_REPTER_dict in ZSECFORM4_REPTER_arr:
        ZSECFORM4_REPTER_dict['ACCESSIONNO'] = ZSECFORM4_REPTER_common_dict['ACCESSIONNO']
        ZSECFORM4_REPTER_dict['SEC_DOC'] = ZSECFORM4_REPTER_common_dict['SEC_DOC']
        ZSECFORM4_REPTER_dict['DATE_REPORT'] = ZSECFORM4_REPTER_common_dict['DATE_REPORT']
        ZSECFORM4_REPTER_dict['FORM_TYPE'] = ZSECFORM4_REPTER_common_dict['FORM_TYPE']

    session.add_all([ZSECFORM4(**ZSECFORM4_dict), ZSECFORM4_ISSUER(**ZSECFORM4_ISSUER_dict)])
    session.add_all([ZSECFORM4_REPTER(**ZSECFORM4_REPTER_dict) for ZSECFORM4_REPTER_dict in ZSECFORM4_REPTER_arr])
    session.add_all([ZSECFORM4_FTNOTE(**ZSECFORM4_FTNOTE_dict) for ZSECFORM4_FTNOTE_dict in ZSECFORM4_FTNOTE_arr])
    session.add_all([ZSECFORM4_DTAB(**ZSECFORM4_DTAB_dict) for ZSECFORM4_DTAB_dict in ZSECFORM4_DTAB_arr])
    session.add_all([ZSECFORM4_NDTAB(**ZSECFORM4_NDTAB_dict) for ZSECFORM4_NDTAB_dict in ZSECFORM4_NDTAB_arr])

rx_5 = {
    'ACCESSIONNO': re.compile(r'ACCESSION NUMBER:(?P<accession_no>.*)'),
    'SEC_DOC': re.compile(r'<sec-document>(?P<sec_doc>.*)'),
    'ACCEPT_TIME': re.compile(r'<acceptance-datetime>(?P<accept_time>.*)'),
    'SEC_HEADER': re.compile(r'<sec-header>(?P<sec_header>.*)'),
    'DOC_FILE_COUNT': re.compile(r'PUBLIC DOCUMENT COUNT:(?P<doc_count>.*)'),
    'REPORT_PERIOD': re.compile(r'CONFORMED PERIOD OF REPORT:(?P<report_period>.*)'),
    'DATE_FILED': re.compile(r'FILED AS OF DATE:(?P<filed_date>.*)'),
    'DATE_CHANGED': re.compile(r'DATE AS OF CHANGE:(?P<change_date>.*)'),
    'REPORTER': re.compile(r'REPORTING-OWNER:'),
    'OWN_DATA': re.compile(r'OWNER DATA:'),
    'ISSUER': re.compile(r'ISSUER:'),
    'COMP_DATA': re.compile(r'COMPANY DATA:'),
    'END_SEC_HEADER': re.compile(r'</sec-header>'),
    'CIK': re.compile(r'CENTRAL INDEX KEY:(?P<cik>.*)'),
    'FORM_TYPE': re.compile(r'CONFORMED SUBMISSION TYPE:(?P<form_type>.*)'),
    'ISSUER_SYMBOL': re.compile(r'<issuertradingsymbol>(?P<issuer_symbol>.*)</issuertradingsymbol>'),
    'SEC_FILENO': re.compile(r'SEC FILE NUMBER:(?P<file_no>.*)'),
    'FILENAME': re.compile(r'<filename>(?P<filename>.*)xml'),
    'FILEDESCRIP': re.compile(r'<description>(?P<filedescrip>.*)'),
    'XML_VERSION': re.compile(r'<\?xml version=\"(?P<xml_version>.*)\"'),
    'DATE_REPORT': re.compile(r'<periodofreport>(?P<date_report>.*)</periodofreport>'),
    'SIGN_BLOCK': re.compile(r'<ownersignature>'),
    'SIGN_NAME': re.compile(r'<signaturename>(?P<sign_name>.*)</signaturename>'),
    'TITLE': re.compile(r'Title:(?P<title>.*)'),
    'NAME': re.compile(r'Name:(?P<name>.*)'),
    'SIGN_DATE': re.compile(r'<signaturedate>(?P<sign_date>.*)</signaturedate>'),
    'END_SIGN_BLOCK': re.compile(r'</ownersignature>'),
    'SCHEMA_VERSION': re.compile(r'<schemaversion>(?P<schema>.*)</schemaversion>'),
    'SECTION_16': re.compile(r'<notsubjecttosection16>(?P<section16>.*)</notsubjecttosection16>'),
    'FORM3': re.compile(r'<form3holdingsreported>(?P<form3>.*)</form3holdingsreported>'),
    'FORM4': re.compile(r'<form4transactionsreported>(?P<form4>.*)</form4transactionsreported>'),
    'CONFDNAME': re.compile(r'COMPANY CONFORMED NAME:(?P<comp_name>.*)'),
    'SIC': re.compile(r'STANDARD INDUSTRIAL CLASSIFICATION:.*\[(?P<sic>.*)\]'),
    'IRS': re.compile(r'IRS NUMBER:(?P<irs>.*)'),
    'STATE_INCORP': re.compile(r'STATE OF INCORPORATION:(?P<state_inc>.*)'),
    'FISCAL_YEAREND': re.compile(r'FISCAL YEAR END:(?P<fiscal_year>.*)'),
    'SEC_ACT': re.compile(r'SEC ACT:(?P<sec_act>.*)'),
    'FILM_NO': re.compile(r'FILM NUMBER:(?P<film_no>.*)'),
    'BUS_ADDR': re.compile(r'BUSINESS ADDRESS:'),
    'MAIL_ADDR': re.compile(r'MAIL ADDRESS:'), 
    'STREET1': re.compile(r'STREET 1:(?P<street1>.*)'),
    'STREET2': re.compile(r'STREET 2:(?P<street2>.*)'),
    'CITY': re.compile(r'CITY:(?P<city>.*)'),
    'STATE': re.compile(r'STATE:(?P<state>.*)'),
    'ZIPCODE': re.compile(r'ZIP:(?P<zip>.*)'),
    'BUS_PHONE': re.compile(r'BUSINESS PHONE:(?P<bus_phone>.*)'),
    'FORMER_COMP': re.compile(r'FORMER COMPANY:'),
    'FCOMP_CONFORMEDNAME': re.compile(r'FORMER CONFORMED NAME:(?P<fcomp_name>.*)'),
    'DATE_NAMECHANGE': re.compile(r'DATE OF NAME CHANGE:(?P<date_name_change>.*)'),
    'REPTOWN': re.compile(r'<reportingowner>'),
    'REPTOWN_CIK': re.compile(r'<rptownercik>(?P<cik>.*)</rptownercik>'),
    'REPTOWN_RELATION': re.compile(r'<reportingwwnerrelationship>'),
    'DIRECTOR': re.compile(r'<isdirector>(?P<is_director>.*)</isdirector>'),
    'OFFICER': re.compile(r'<isofficer>(?P<is_officer>.*)</isofficer>'),
    'TENPERCENTOWNER': re.compile(r'<istenpercentowner>(?P<is_tenpercent>.*)</istenpercentowner>'),
    'OTHER': re.compile(r'<isother>(?P<is_other>.*)</isother>'),
    'TEXT_OTHER': re.compile(r'<othertext>(?P<otherText>.*)</othertext>'),
    'OFFICER_TITLE': re.compile(r'<officertitle>(?P<off_title>.*)</officertitle>'),
    'END_REPTOWN_RELATION': re.compile(r'</reportingownerrelationship>'),
    'END_REPTOWN': re.compile(r'</reportingowner>'),
    'NDH': re.compile(r'<nonderivativetransaction>'),
    'SECURITY_TYPETITLE': re.compile(r'<securitytitle>'),
    'END_SECURITY_TYPETITLE': re.compile(r'</securitytitle>'),
    'DATE_TRANS': re.compile(r'<transactiondate>'),
    'END_DATE_TRANS': re.compile(r'</transactiondate>'),
    'DATE_EXECUTION': re.compile(r'<deemedexecutiondate>'),
    'TRANS_FORM_TYPE': re.compile(r'<transactionformtype>(?P<form_type>.*)</transactionformtype>'),
    'TRANS_CODE': re.compile(r'<transactioncode>(?P<trans_code>.*)</transactioncode>'),
    'SWAP': re.compile(r'<equityswapinvolved>(?P<swap>.*)</equityswapinvolved>'),
    'END_TRANSCODING': re.compile(r'</transactioncoding>'),
    'ACQ_DISPOSED': re.compile('<transactionacquireddisposedcode>'),
    'SHARES': re.compile(r'<transactionshares>'),
    'END_SHARES': re.compile(r'</transactionshares>'),
    'SHARE_VALUE': re.compile(r'<transactionpricepershare>'),
    'END_SHARE_VALUE': re.compile(r'</transactionpricepershare>'),
    'SHARES_AFTER': re.compile(r'<sharesownedfollowingtransaction>'),
    'END_SHARES_AFTER': re.compile(r'</sharesownedfollowingtransaction>'),
    'OWNERSHIPTYPE': re.compile(r'<directorindirectownership>'),
    'END_OWNERSHIPTYPE': re.compile(r'</directorindirectownership>'),
    'INDBENF_OWNER': re.compile(r'<natureofownership>'),
    'END_INDBENF_OWNER': re.compile(r'</natureofownership>'),
    'END_NDH': re.compile(r'</nonderivativetransaction>'),
    'VALUE': re.compile(r'<value>(?P<value>.*)</value>'),
    'FTNOTE_ID': re.compile(r'<footnoteid id="(?P<ftnote_id>.*)">'),
    'DH': re.compile(r'<derivativetransaction>'),
    'EXPRICE_DERVSECURTY': re.compile(r'<conversionorexerciseprice>'),
    'END_EXPRICE_DERVSECURTY': re.compile(r'</conversionorexerciseprice>'),
    'DATE_EXCISE': re.compile(r'<exercisedate>'),
    'END_DATE_EXCISE': re.compile(r'</exercisedate>'),
    'DATE_EXPIRE': re.compile(r'<expirationdate>'),
    'END_DATE_EXPIRE': re.compile(r'</expirationdate>'),
    'UNDERSECURITY_TYPETITLE': re.compile(r'<underlyingsecuritytitle>'),
    'END_UNDERSECURITY_TYPETITLE': re.compile(r'</underlyingsecuritytitle>'),
    'END_DH': re.compile(r'</derivativetransaction>'),
    'S_FOOTNOTE': re.compile(r'<footnote id=\"(?P<id>.*)\">(?P<txt>.*)</footnote>'),
    'M_FOOTNOTE': re.compile(r'<footnote id=\"(?P<id>.*)\">(?P<txt>.*)'),
    'END_FOOTNOTE': re.compile(r'(?P<txt>.*)</footnote>'),
}

def parse_line_form5(func_time, line=""):
    if time.time() - func_time > 30:
        raise TimeoutException(line)
    for key, rx in rx_5.items():
        match = rx.search(line)
        if match:
            return key, match
    return None, None

def parse_and_upload_form5(session, cik, filename):
    func_time = time.time()
    ZSECFORM5_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'ACCEPT_TIME': None, 'CIK_ISSUER': None,
        'FORM_TYPE': None, 'ISSUER_SYMBOL': None, 'SEC_HEADER': None, 'DOC_FILE_COUNT': None, 'REPORT_PERIOD': None,
        'DATE_FILED': None, 'DATE_CHANGED': None, 'VERSION': None, 'FILENAME': None, 'FILEDESCRIP': None, 'XML_VERSION': None,
        'SCHEMA_VERSION': None, 'SECTION_16': None, 'FORM3HOLDRPTD': None, 'FORM4TRANXRPTD': None, 'SIGN_TITLE': None, 
        'SIGN_NAME': None, 'SIGN_DATE': None, 'DERV_TAB': False,'NDERV_TAB': False, 'FTNOTE_FLG': False, 'ERDAT': None}
    ZSECFORM5_ISSUER_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'CIK_ISSUER': None,
        'FORM_TYPE': None, 'ISSUER_SYMBOL': None, 'ISSU_CONFDNAME': None, 'SIC': None, 'IRS': None, 'STATE_INCORP': None,
        'FISCAL_YEAREND': None, 'BUS_STREET1': None, 'BUS_STREET2': None, 'BUS_CITY': None, 'BUS_STATE': None, 'BUS_STATETXT': None, 
        'BUS_ZIPCODE': None, 'BUS_PHONE': None, 'MAIL_STREET1': None, 'MAIL_STREET2': None, 'MAIL_CITY': None, 'MAIL_STATE': None, 
        'MAIL_STATETXT': None, 'MAIL_ZIPCODE': None, 'FCOMP_CONFORMEDNAME1': None, 'DATE_NAMECHANGE1': None, 
        'FCOMP_CONFORMEDNAME2': None, 'DATE_NAMECHANGE2': None, 'FCOMP_CONFORMEDNAME3': None, 'DATE_NAMECHANGE3': None,}
    ZSECFORM5_REPTER_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'DATE_REPORT': None, 'FORM_TYPE': None, 'CIK_REPORTER': None, 
         'REPT_CONFDNAME': None, 'FIRST_NAME': None, 'LAST_NAME': None, 'MIDDLE_NAME': None, 'OFFICER_TITLE': None, 'SEC_ACT': None, 
         'SEC_FILENO': None, 'FILM_NO': None, 'BUS_STREET1': None, 'BUS_STREET2': None, 'BUS_CITY': None, 'BUS_STATE': None, 
         'BUS_STATETXT': None, 'BUS_ZIPCODE': None, 'BUS_PHONE': None, 'MAIL_STREET1': None, 'MAIL_STREET2': None, 'MAIL_CITY': None, 
         'MAIL_STATE': None, 'MAIL_STATETXT': None, 'MAIL_ZIPCODE': None, 'FCOMP_CONFORMEDNAME': None, 'DATE_NAMECHANGE': None, 
         'DIRECTOR': None, 'OFFICER': None, 'TENPERCENTOWNER': None, 'OTHER': None, 'TEXT_OTHER': None, 'SIGN_TITLE': None, 'SIGN_NAME': None, 
         'SIGN_DATE': None,}
    ZSECFORM5_DTAB_arr = []
    ZSECFORM5_NDTAB_arr = []
    ZSECFORM5_FTNOTE_arr = [] 
    form_comp_count = ndh_index = dh_index = 1
    with open(f"companies/{cik}/{filename}", 'r') as file:
        content = file.read()
        lines = content.splitlines()
        file.close()
    
    i = 0
    while i < len(lines):
        key, match = parse_line_form5(func_time, lines[i].strip())
        if not key:
            i += 1
            continue
        
        elif key == 'ACCESSIONNO':
            ZSECFORM5_dict['ACCESSIONNO'] = match.group('accession_no').strip()
            ZSECFORM5_ISSUER_dict['ACCESSIONNO'] = match.group('accession_no').strip()
            ZSECFORM5_REPTER_dict['ACCESSIONNO'] = match.group('accession_no').strip()
        
        elif key == 'SEC_DOC':
            ZSECFORM5_dict['SEC_DOC'] = match.group('sec_doc').strip()
            ZSECFORM5_ISSUER_dict['SEC_DOC'] = match.group('sec_doc').strip()
            ZSECFORM5_REPTER_dict['SEC_DOC'] = match.group('sec_doc').strip()
        
        elif key == 'ACCEPT_TIME': ZSECFORM5_dict['ACCEPT_TIME'] = match.group('accept_time').strip()
        
        elif key == 'FORM_TYPE':
            ZSECFORM5_dict['FORM_TYPE'] = match.group('form_type').strip()
            ZSECFORM5_ISSUER_dict['FORM_TYPE'] = match.group('form_type').strip()
            ZSECFORM5_REPTER_dict['FORM_TYPE'] = match.group('form_type').strip()
        
        elif key == 'SEC_HEADER': ZSECFORM5_dict['SEC_HEADER'] = match.group('sec_header').strip()
        
        elif key == 'DOC_FILE_COUNT': ZSECFORM5_dict['DOC_FILE_COUNT'] = match.group('doc_count').strip()
        
        elif key == 'REPORT_PERIOD': ZSECFORM5_dict['REPORT_PERIOD'] = match.group('report_period').strip()
        
        elif key == 'DATE_FILED': ZSECFORM5_dict['DATE_FILED'] = match.group('filed_date').strip()
        
        elif key == 'DATE_CHANGED': ZSECFORM5_dict['DATE_CHANGED'] = match.group('change_date').strip()
        
        elif key == 'COMP_DATA':
            while key != 'END_SEC_HEADER' and key != 'REPORTER':
                key, match = parse_line_form5(func_time, lines[i].strip())
                if key == 'BUS_ADDR':
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'STREET1': ZSECFORM5_ISSUER_dict['BUS_STREET1'] = match.group('street1').strip()
                        elif key == 'STREET2': ZSECFORM5_ISSUER_dict['BUS_STREET2'] = match.group('street2').strip()
                        elif key == 'CITY': ZSECFORM5_ISSUER_dict['BUS_CITY'] = match.group('city').strip()
                        elif key == 'STATE': ZSECFORM5_ISSUER_dict['BUS_STATE'] = match.group('state').strip()
                        elif key == 'ZIPCODE': ZSECFORM5_ISSUER_dict['BUS_ZIPCODE'] = match.group('zip').strip()
                        elif key == 'BUS_PHONE': ZSECFORM5_ISSUER_dict['BUS_PHONE'] = match.group('bus_phone').strip()
                        i += 1
                    i -= 1 
                
                elif key == 'MAIL_ADDR':
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'STREET1': ZSECFORM5_ISSUER_dict['MAIL_STREET1'] = match.group('street1').strip()
                        elif key == 'STREET2': ZSECFORM5_ISSUER_dict['MAIL_STREET2'] = match.group('street2').strip()
                        elif key == 'CITY': ZSECFORM5_ISSUER_dict['MAIL_CITY'] = match.group('city').strip()
                        elif key == 'STATE': ZSECFORM5_ISSUER_dict['MAIL_STATE'] = match.group('state').strip()
                        elif key == 'ZIPCODE': ZSECFORM5_ISSUER_dict['MAIL_ZIPCODE'] = match.group('zip').strip()
                        i += 1 
                    i -= 1
                
                elif key == 'FORMER_COMP' and form_comp_count <= 3:
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'FCOMP_CONFORMEDNAME': ZSECFORM5_ISSUER_dict[f'FCOMP_CONFORMEDNAME{form_comp_count}'] = match.group('fcomp_name').strip()
                        elif key == 'DATE_NAMECHANGE': ZSECFORM5_ISSUER_dict[f'DATE_NAMECHANGE{form_comp_count}'] = match.group('date_name_change').strip()
                        i += 1 
                    form_comp_count += 1
                    i -= 1

                elif key == 'CIK':
                    ZSECFORM5_dict['CIK_ISSUER'] = match.group('cik').strip()
                    ZSECFORM5_ISSUER_dict['CIK_ISSUER'] = match.group('cik').strip()
                
                elif key == 'CONFDNAME': ZSECFORM5_ISSUER_dict['ISSU_CONFDNAME'] = match.group('comp_name').strip()
                
                elif key == 'SIC': ZSECFORM5_ISSUER_dict['SIC'] = match.group('sic').strip()
                
                elif key == 'IRS': ZSECFORM5_ISSUER_dict['IRS'] = match.group('irs').strip()
                
                elif key == 'STATE_INCORP': ZSECFORM5_ISSUER_dict['STATE_INCORP'] = match.group('state_inc').strip()
                
                elif key == 'FISCAL_YEAREND': ZSECFORM5_ISSUER_dict['FISCAL_YEAREND'] = match.group('fiscal_year').strip()
                
                i += 1 

        elif key == 'OWN_DATA':
            while  key != 'ISSUER' and key != 'END_SEC_HEADER':
                key, match = parse_line_form5(func_time, lines[i].strip())

                if key == 'BUS_ADDR':
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'STREET1': ZSECFORM5_REPTER_dict['BUS_STREET1'] = match.group('street1').strip()
                        elif key == 'STREET2': ZSECFORM5_REPTER_dict['BUS_STREET2'] = match.group('street2').strip()
                        elif key == 'CITY': ZSECFORM5_REPTER_dict['BUS_CITY'] = match.group('city').strip()
                        elif key == 'STATE': ZSECFORM5_REPTER_dict['BUS_STATE'] = match.group('state').strip()
                        elif key == 'ZIPCODE': ZSECFORM5_REPTER_dict['BUS_ZIPCODE'] = match.group('zip').strip()
                        elif key == 'BUS_PHONE': ZSECFORM5_REPTER_dict['BUS_PHONE'] = match.group('bus_phone').strip()
                        i += 1
                    i -= 1
                
                elif key == 'MAIL_ADDR':
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'STREET1': ZSECFORM5_REPTER_dict['MAIL_STREET1'] = match.group('street1').strip()
                        elif key == 'STREET2': ZSECFORM5_REPTER_dict['MAIL_STREET2'] = match.group('street2').strip()
                        elif key == 'CITY': ZSECFORM5_REPTER_dict['MAIL_CITY'] = match.group('city').strip()
                        elif key == 'STATE': ZSECFORM5_REPTER_dict['MAIL_STATE'] = match.group('state').strip()
                        elif key == 'ZIPCODE': ZSECFORM5_REPTER_dict['MAIL_ZIPCODE'] = match.group('zip').strip()
                        i += 1
                    i -= 1
                
                elif key == 'FORMER_COMP' and not ZSECFORM5_REPTER_dict['FCOMP_CONFORMEDNAME']:
                    while key and key != 'END_SEC_HEADER':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'FCOMP_CONFORMEDNAME': ZSECFORM5_REPTER_dict['FCOMP_CONFORMEDNAME'] = match.group('fcomp_name').strip()
                        elif key == 'DATE_NAMECHANGE': ZSECFORM5_REPTER_dict['DATE_NAMECHANGE'] = match.group('date_name_change').strip()
                        i += 1
                    i -= 1

                elif key == 'CIK': ZSECFORM5_REPTER_dict['CIK_REPORTER'] = match.group('cik').strip()
                
                elif key == 'CONFDNAME': ZSECFORM5_REPTER_dict['REPT_CONFDNAME'] = match.group('comp_name').strip()
                
                elif key == 'SEC_ACT': ZSECFORM5_REPTER_dict['SEC_ACT'] = match.group('sec_act').strip()
                
                elif key == 'SEC_FILENO': ZSECFORM5_REPTER_dict['SEC_FILENO'] = match.group('file_no').strip()
                
                elif key == 'FILM_NO': ZSECFORM5_REPTER_dict['FILM_NO'] = match.group('film_no').strip()
                
                i += 1

        elif key == 'FILENAME':
            ZSECFORM5_dict['FILENAME'] = match.group('filename').strip()
            i += 1
            key, match = parse_line_form5(func_time, lines[i].strip())
            if key == 'FILEDESCRIP': ZSECFORM5_dict['FILEDESCRIP'] = match.group('filedescrip').strip()
            else: i -= 1
        
        elif key == 'XML_VERSION': ZSECFORM5_dict['XML_VERSION'] = match.group('xml_version').strip()
        
        elif key == 'SCHEMA_VERSION': ZSECFORM5_dict['SCHEMA_VERSION'] = match.group('schema').strip()

        elif key == 'SECTION_16': ZSECFORM5_dict['SECTION_16'] = match.group('section16').strip()

        elif key == 'FORM3': ZSECFORM5_dict['FORM3HOLDRPTD'] = match.group('form3').strip()

        elif key == 'FORM4': ZSECFORM5_dict['FORM4TRANXRPTD'] = match.group('form4').strip()

        elif key == 'DATE_REPORT': ZSECFORM5_REPTER_dict['DATE_REPORT'] = match.group('date_report').strip()
        
        elif key == 'ISSUER_SYMBOL':
            ZSECFORM5_dict['ISSUER_SYMBOL'] = match.group('issuer_symbol').strip()
            ZSECFORM5_ISSUER_dict['ISSUER_SYMBOL'] = match.group('issuer_symbol').strip()

        elif key == 'REPTOWN_RELATION':
             while key != 'END_REPTOWN_RELATION':
                key, match = parse_line_form5(func_time, lines[i].strip())
                if key == 'DIRECTOR': ZSECFORM5_REPTER_dict['DIRECTOR'] = match.group('is_director').strip()
                elif key == 'OFFICER': ZSECFORM5_REPTER_dict['OFFICER'] = match.group('is_officer').strip()
                elif key == 'TENPERCENTOWNER': ZSECFORM5_REPTER_dict['TENPERCENTOWNER'] = match.group('is_tenpercent').strip()
                elif key == 'OTHER': ZSECFORM5_REPTER_dict['OTHER'] = match.group('is_other').strip()
                elif key == 'TEXT_OTHER': ZSECFORM5_REPTER_dict['TEXT_OTHER'] = match.group('otherText').strip()
                elif key == 'OFFICER_TITLE': ZSECFORM5_REPTER_dict['OFFICER_TITLE'] = match.group('off_title').strip()
                i += 1
        
        elif key == 'NDH':
            ZSECFORM5_NDTAB_dict = {'MANDT': "100", 'ACCESSIONNO': ZSECFORM5_dict['ACCESSIONNO'], 'ACCESS_TRANXID': f"{ndh_index}", 
                                    'DATE_TRANS': None, 'TRANSDATE_FTNOTE': None, 'DATE_EXECUTION': None, 'TRANS_CODE': None, 'TRANSCODE_FTNOTE': None,
                                    'FORM_TYPE': None, 'SECURITY_TYPETITLE': None, 'SECTITLE_FTNOTE': None, 
                                    'SWAP': None, 'SWAP_FTNOTE': None, 'SHARES': None, 'SHARE_FTNOTE': None, 'ACQ_DISPOSED': None, 'SHARE_VALUE': None, 
                                    'SHAREVALUE_FTNOTE': None,  'SHARES_AFTER': None, 'SHAREAFT_FTNOTE': None,'OWNERSHIPTYPE': None, 
                                    'OWNSHIP_FTNOTE': None, 'INDBENF_OWNER': None,'INDBENF_OWNER_FTNOTE': None}
            while key != 'END_NDH':
                key, match = parse_line_form5(func_time, lines[i].strip())
                footnote_arr = []
                if key == 'SECURITY_TYPETITLE':
                    while key != 'END_SECURITY_TYPETITLE':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM5_NDTAB_dict['SECURITY_TYPETITLE'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM5_NDTAB_dict['SECTITLE_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'DATE_TRANS':
                    while key != 'END_DATE_TRANS':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM5_NDTAB_dict['DATE_TRANS'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM5_NDTAB_dict['TRANSDATE_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'DATE_EXECUTION':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_NDTAB_dict['DATE_EXECUTION'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'DATE_EXCISE':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_NDTAB_dict['DATE_EXCISE'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'DATE_EXPIRE':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_NDTAB_dict['DATE_EXPIRE'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'TRANS_FORM_TYPE': ZSECFORM5_NDTAB_dict['FORM_TYPE'] = match.group('form_type').strip()
                
                elif key == 'TRANS_CODE': ZSECFORM5_NDTAB_dict['TRANS_CODE'] = match.group('trans_code').strip()
                
                elif key == 'SWAP': 
                    ZSECFORM5_NDTAB_dict['SWAP'] = match.group('swap').strip()
                    while key != 'END_TRANSCODING':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM5_NDTAB_dict['SWAP_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1
                
                elif key == 'ACQ_DISPOSED':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_NDTAB_dict['ACQ_DISPOSED'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'SHARES':
                    while key != 'END_SHARES':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM5_NDTAB_dict['SHARES'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM5_NDTAB_dict['SHARE_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'SHARE_VALUE':
                    while key != 'END_SHARE_VALUE':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM5_NDTAB_dict['SHARE_VALUE'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM5_NDTAB_dict['SHAREVALUE_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'SHARES_AFTER':
                    while key != 'END_SHARES_AFTER':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM5_NDTAB_dict['SHARES_AFTER'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM5_NDTAB_dict['SHAREAFT_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'OWNERSHIPTYPE':
                    while key != 'END_OWNERSHIPTYPE':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM5_NDTAB_dict['OWNERSHIPTYPE'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM5_NDTAB_dict['OWNSHIP_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1

                elif key == 'INDBENF_OWNER':
                    while key != 'END_INDBENF_OWNER':
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'VALUE': ZSECFORM5_NDTAB_dict['INDBENF_OWNER'] = match.group('value').strip()
                        elif key == 'FTNOTE_ID': footnote_arr.append(match.group('ftnote_id').strip())
                        i += 1
                    ZSECFORM5_NDTAB_dict['INDBENF_OWNER_FTNOTE'] = ", ".join(footnote_arr)
                    i -= 1
                    
                i += 1

            ZSECFORM5_NDTAB_arr.append(ZSECFORM5_NDTAB_dict)
            ZSECFORM5_dict['NDERV_TAB'] = True
            ndh_index += 1
            i -= 1

        elif key == 'DH':
            ZSECFORM5_DTAB_dict = {'MANDT': "100", 'ACCESSIONNO': ZSECFORM5_dict['ACCESSIONNO'], 'ACCESS_TRANXID': f"{dh_index}",
                                   'DATE_TRANS': None, 'DATE_EXECUTION': None, 'TRANS_CODE': None, 
                                   'FORM_TYPE': None, 'SWAP': None, 'ACQ_DISPOSED':None, 
                                   'DERIVSECURITY_TYPETITLE': None, 'DATE_EXCISE': None, 'DATE_EXPIRE': None, 
                                   'SECURITY_TYPETITLE': None, 'SHARE_AMOUNT': None, 'EXPRICE_DERVSECURTY': None, 
                                   'PRICE_DERIV': None, 'SHARES_AFTER': None, 'OWNERSHIPTYPE': None, 'INDBENF_OWNER': None}

            while key != 'END_DH':
                key, match = parse_line_form5(func_time, lines[i].strip())
                if key == 'SECURITY_TYPETITLE':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['DERIVSECURITY_TYPETITLE'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'UNDERSECURITY_TYPETITLE':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['SECURITY_TYPETITLE'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'EXPRICE_DERVSECURTY':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['EXPRICE_DERVSECURTY'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'DATE_TRANS':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['DATE_TRANS'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'DATE_EXECUTION':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['DATE_EXECUTION'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'TRANS_FORM_TYPE': ZSECFORM5_DTAB_dict['FORM_TYPE'] = match.group('form_type').strip()
                
                elif key == 'TRANS_CODE': ZSECFORM5_DTAB_dict['TRANS_CODE'] = match.group('trans_code').strip()
                
                elif key == 'SWAP': ZSECFORM5_DTAB_dict['SWAP'] = match.group('swap').strip()
                
                elif key == 'ACQ_DISPOSED':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['ACQ_DISPOSED'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'SHARES':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['SHARE_AMOUNT'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'SHARE_VALUE':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['PRICE_DERIV'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'SHARES_AFTER':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['SHARES_AFTER'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'OWNERSHIPTYPE':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['OWNERSHIPTYPE'] = match.group('value').strip()
                    else: i -= 1

                elif key == 'INDBENF_OWNER':
                    i += 1
                    key, match = parse_line_form5(func_time, lines[i].strip())
                    if key == 'VALUE': ZSECFORM5_DTAB_dict['INDBENF_OWNER'] = match.group('value').strip()
                    else: i -= 1

                i += 1

            ZSECFORM5_DTAB_arr.append(ZSECFORM5_DTAB_dict)
            ZSECFORM5_dict['DERV_TAB'] = True
            dh_index += 1
            i -= 1

        elif key == 'S_FOOTNOTE':
            ZSECFORM5_dict['FTNOTE_FLG'] = True
            ZSECFORM5_FTNOTE_arr.append({'MANDT': "100", 'ACCESSIONNO': ZSECFORM5_dict['ACCESSIONNO'], 
                                         'SEC_DOC': ZSECFORM5_dict['SEC_DOC'], 'FOOTNOTE_ID': match.group('id').strip(), 
                                         'FOOTNOTE_TXT': match.group('txt').strip()})
      
        elif key == 'M_FOOTNOTE':
            ZSECFORM5_dict['FTNOTE_FLG'] = True
            footnote_id = match.group('id').strip()
            footnote_txt = match.group('txt').strip()
            while key != 'END_FOOTNOTE':
                i += 1
                key, match = parse_line_form5(func_time, lines[i].strip())
                if key != 'END_FOOTNOTE':
                    footnote_txt += f" {lines[i].strip()}"
            footnote_txt += f" {match.group('txt').strip()}"
            ZSECFORM5_FTNOTE_arr.append({'MANDT': "100", 'ACCESSIONNO': ZSECFORM5_dict['ACCESSIONNO'], 
                                         'SEC_DOC': ZSECFORM5_dict['SEC_DOC'], 'FOOTNOTE_ID': footnote_id, 
                                         'FOOTNOTE_TXT': footnote_txt})

        elif key == 'SIGN_BLOCK':
            i += 1
            key, match = parse_line_form5(func_time, lines[i].strip())
            if key == 'SIGN_NAME':
                last_sign_name = match.group('sign_name').strip()
                sign_names = match.group('sign_name').strip().split(",")
                if len(sign_names) == 1:
                    striped_name = sign_names[0].replace('.', '')
                    striped_name = striped_name.replace('/s/', '')
                    striped_name = striped_name.replace(',', '')
                    striped_name = striped_name.replace('By:', '').strip()
                    name_parts = striped_name.split(" ")
                    if len(name_parts) > 1 and len(name_parts) <= 3:
                        comp_name = f"{name_parts[len(name_parts)-1]} {' '.join(name_parts[:len(name_parts)-1])}"
                    elif len(name_parts) > 3:
                        comp_name = f"{name_parts[2]} {' '.join(name_parts[:2])} {' '.join(name_parts[2:len(name_parts)-1])}"
                    else:
                        name_parts = []
                        comp_name = striped_name

                    ZSECFORM5_dict['SIGN_NAME'] = sign_names[0].replace('/s/', '')
                    ZSECFORM5_REPTER_dict['SIGN_NAME'] = sign_names[0].replace('/s/', '')
                    if len(name_parts) == 1:
                        ZSECFORM5_REPTER_dict['FIRST_NAME'] = name_parts[0]
                    elif len(name_parts) == 2:
                        ZSECFORM5_REPTER_dict['FIRST_NAME'] = name_parts[0]
                        ZSECFORM5_REPTER_dict['LAST_NAME'] = name_parts[1]
                    else:
                        ZSECFORM5_REPTER_dict['FIRST_NAME'] = name_parts[0]
                        ZSECFORM5_REPTER_dict['MIDDLE_NAME'] = name_parts[1]
                        ZSECFORM5_REPTER_dict['LAST_NAME'] = name_parts[2]  
                else:
                    comp_name = sign_names[0]

                    ZSECFORM5_dict['SIGN_NAME'] = sign_names[0]
                    ZSECFORM5_REPTER_dict['SIGN_NAME'] = sign_names[0]
                    for sign_name in sign_names:
                        key, match = parse_line_form5(func_time, lines[i].strip())
                        if key == 'TITLE':
                            ZSECFORM5_dict['SIGN_TITLE'] = match.group('title').strip()
                            ZSECFORM5_REPTER_dict['SIGN_TITLE'] = match.group('title').strip()
                        elif key == 'NAME':
                            name = match.group('name').strip().split()
                            if len(name) == 1:
                                ZSECFORM5_REPTER_dict['FIRST_NAME'] = name[0]
                            elif len(name) == 2:
                                ZSECFORM5_REPTER_dict['FIRST_NAME'] = name[0]
                                ZSECFORM5_REPTER_dict['LAST_NAME'] = name[1]
                            else:
                                ZSECFORM5_REPTER_dict['FIRST_NAME'] = name[0]
                                ZSECFORM5_REPTER_dict['MIDDLE_NAME'] = name[1]
                                ZSECFORM5_REPTER_dict['LAST_NAME'] = name[2]

                i += 1
                key, match = parse_line_form5(func_time, lines[i].strip())
                if key == 'SIGN_DATE':
                    ZSECFORM5_dict['SIGN_DATE'] = match.group('sign_date').strip()
                    ZSECFORM5_REPTER_dict['SIGN_DATE'] = match.group('sign_date').strip()
                else: i -= 1
            
            i -= 1

        i += 1

    session.add_all([ZSECFORM5(**ZSECFORM5_dict), ZSECFORM5_ISSUER(**ZSECFORM5_ISSUER_dict), ZSECFORM5_REPTER(**ZSECFORM5_REPTER_dict)])
    session.add_all([ZSECFORM5_FTNOTE(**ZSECFORM5_FTNOTE_dict) for ZSECFORM5_FTNOTE_dict in ZSECFORM5_FTNOTE_arr])
    session.add_all([ZSECFORM5_DTAB(**ZSECFORM5_DTAB_dict) for ZSECFORM5_DTAB_dict in ZSECFORM5_DTAB_arr])
    session.add_all([ZSECFORM5_NDTAB(**ZSECFORM5_NDTAB_dict) for ZSECFORM5_NDTAB_dict in ZSECFORM5_NDTAB_arr])