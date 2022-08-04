import re
from datetime import datetime
from models import (metadata, ZSECFORM3, 
	ZSECFORM3_ISSUER, ZSECFORM3_REPTER, ZSECFORM3_DTAB, ZSECFORM3_NDTAB, ZSECFORM3_FTNOTE)

class form_13():

	def __init__(self, file, conn):
		self.patterns = {
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
		self.ZSECFORM13_dict = {
		'MANDT': "100", 'ZACCESSIONNO': None, 'ZSECDOC': None, 'ZSEC_ACCEPTTIME': None, 'ZCIK_ISSUER': None, 
		'ZFORM_TYPE': None, 'ZISSUER_SYMBOL': None, 'ZSECHEADER': None, 'ZDOC_COUNT': None, 'ZREPORT_PERIOD': None, 'ZDATE_FILED': None, 
		'ZDATE_CHANGED': None, 'ZAMEND': None, 'ZAMEND_NUMBER': None, 'ZAMEND_RESTATE': None, 'ZAMEND_NEWHOLDING': None, 
		'VERSION': None, 'ZSEC_FILENO': None, 'ZSEC_FILENAME': None, 'ZFILE_DESCRIP': None, 'ZXML_VERSION': None, 
		'ZSCHEMA_VERSION': None, 'ZSECTION16': None, 'ZSIGN_TITLE': None, 'ZSIGN_NAME': None, 'ZSIGN_DATE': None, 
		'ERDAT': None, 'ERNAME': None, 'ZTOTAL_TABENTRY': None, 'ZTOTAL_TABVALUE': None
		}

		self.ZSECFORM13_FILER_dict = {
			'MANDT': "100", 'ZACCESSIONNO': None, 'ZCIK_ISSUER': None, 'ZCOMPCONFDNAME': None, 'ZSEC_IRSNO': None, 
			'ZINCORP_STATE': None, 'ZFISCAL_YREND': None, 'BUS_STRAS': None, 'BUS_CITY': None, 'BUS_REGION': None, 
			'BUS_BEZEI20': None, 'BUS_POST_CODE': None, 'BUS_TELF': None, 'MAIL_STRAS': None, 'MAIL_CITY': None, 
			'MAIL_REGION': None, 'MAIL_POST_CODE': None, 'ZFCOMPCONFDNAME1': None, 'ZDATE_NAMECHANGE1': None, 
			'ZFCOMPCONFDNAME2': None, 'ZDATE_NAMECHANGE2': None, 'ZFCOMPCONFDNAME3': None, 'ZDATE_NAMECHANGE3': None
			}

		self.ZSECFORM13F_INFO_arr = []
		self.file = file
		self.line = self.file.readline()
		self.parse_form()
		self.upload_form(conn)


	def parse_line(self):
	    for key, rx in self.patterns.items():
	        match = rx.search(self.line)
	        if match:
	        	return key, match
	    return None, None
	
	def parse_form(self):
		while self.line:
			key, match = self.parse_line()
			if key == 'ZACCESSIONNO':
				self.ZSECFORM13_dict['ZACCESSIONNO'] = match.group('accession_no').strip()
				self.ZSECFORM13_FILER_dict['ZACCESSIONNO'] = match.group('accession_no').strip()
			elif key == 'ZSECDOC':
				self.ZSECFORM13_dict['ZSECDOC'] = match.group('sec_doc').strip()
				self.ZSECFORM13_dict['ZSECDOC'] = match.group('sec_doc').strip()
			elif key == 'ZSEC_ACCEPTTIME':
				self.ZSECFORM13_dict['ZSEC_ACCEPTTIME'] = match.group('sec_acceptime').strip()
			elif key == 'ZCIK_ISSUER':
				self.ZSECFORM13_dict['ZCIK_ISSUER'] = match.group('cik').strip()
				self.ZSECFORM13_FILER_dict['ZCIK_ISSUER'] = match.group('cik').strip()
			elif key == 'ZFORM_TYPE':
				self.ZSECFORM13_dict['ZFORM_TYPE'] = match.group('form_type').strip()
			elif key == 'ZSECHEADER':
				self.ZSECFORM13_dict['ZSECHEADER'] = match.group('sec_header').strip()
			elif key == 'ZDOC_COUNT':
				self.ZSECFORM13_dict['ZDOC_COUNT'] = match.group('doc_count').strip()
			elif key == 'ZREPORT_PERIOD':
				self.ZSECFORM13_dict['ZREPORT_PERIOD'] = match.group('report_period').strip()
			elif key == 'ZDATE_FILED':
				self.ZSECFORM13_dict['ZDATE_FILED'] = match.group('filed_date').strip()
			elif key == 'ZDATE_CHANGED':
				self.ZSECFORM13_dict['ZDATE_CHANGED'] = match.group('change_date').strip()
			elif key == 'ZSEC_FILENO':
				self.ZSECFORM13_dict['ZSEC_FILENO'] = match.group('file_no').strip()
			elif key == 'ZXML_VERSION':
				self.ZSECFORM13_dict['ZXML_VERSION'] = match.group('xml_version').strip()
			elif key == 'SIGN_BLOCK':
				while key != 'END_SIGN_BLOCK':
					key, match = self.parse_line()
					if key == 'ZSIGN_TITLE':
						self.ZSECFORM13_dict['ZSIGN_TITLE'] = match.group('sign_title').strip()
					elif key == 'ZSIGN_NAME':
						self.ZSECFORM13_dict['ZSIGN_NAME'] = match.group('sign_name').strip()
					elif key == 'ZSIGN_DATE':
						self.ZSECFORM13_dict['ZSIGN_DATE'] = match.group('sign_date').strip()
					self.line = self.file.readline()
			elif key == 'ZTOTAL_TABENTRY':
				self.ZSECFORM13_dict[key] = match.group('total_tab_entry').strip()
			elif key == 'ZTOTAL_TABVALUE':
				self.ZSECFORM13_dict[key] = match.group('total_tab_value').strip()
			elif key == 'ZCOMPCONFDNAME':
				self.ZSECFORM13_FILER_dict[key] = match.group('comp_name').strip()
			elif key == 'ZSEC_IRSNO':
				self.ZSECFORM13_FILER_dict[key] = match.group('irs_no').strip()
			elif key == 'ZINCORP_STATE':
				self.ZSECFORM13_FILER_dict[key] = match.group('inc_state').strip()
			elif key == 'ZFISCAL_YREND':
				self.ZSECFORM13_FILER_dict[key] = match.group('fiscal_year').strip()
			elif key == 'BUS_ADDR':
				while key:
					key, match = self.parse_line()
					if key == 'STREET1':
						self.ZSECFORM13_FILER_dict['BUS_STRAS'] = match.group('street').strip()
					elif key == 'STREET2':
						self.ZSECFORM13_FILER_dict['BUS_STRAS'] += f", {match.group('street').strip()}"
					elif key == 'CITY':
						self.ZSECFORM13_FILER_dict['BUS_CITY'] = match.group('city').strip()
					elif key == 'REGION':
						self.ZSECFORM13_FILER_dict['BUS_REGION'] = match.group('region').strip()
					elif key == 'POST_CODE':
						self.ZSECFORM13_FILER_dict['BUS_POST_CODE'] = match.group('post_code').strip()
					elif key == 'BUS_TELF':
						self.ZSECFORM13_FILER_dict[key] = match.group('bus_telf').strip()
					self.line = self.file.readline()
			elif key == 'MAIL_ADDR':
				while key:
					key, match = self.parse_line()
					if key == 'STREET1':
						self.ZSECFORM13_FILER_dict['MAIL_STRAS'] = match.group('street').strip()
					elif key == 'STREET2':
						self.ZSECFORM13_FILER_dict['MAIL_STRAS'] += f", {match.group('street').strip()}"
					elif key == 'CITY':
						self.ZSECFORM13_FILER_dict['MAIL_CITY'] = match.group('city').strip()
					elif key == 'REGION':
						self.ZSECFORM13_FILER_dict['MAIL_REGION'] = match.group('region').strip()
					elif key == 'POST_CODE':
						self.ZSECFORM13_FILER_dict['MAIL_POST_CODE'] = match.group('post_code').strip()
					self.line = self.file.readline()
			elif key == 'INFO_TABLE':
				ZSECFORM13F_INFO_dict = {'MANDT': "100", 'ZACCESSIONNO': self.ZSECFORM13_dict['ZACCESSIONNO'], 
							        	'ZCIK_ISSUER': self.ZSECFORM13_dict['ZCIK_ISSUER'], 'ZCUSIP': None, 'ZSHAREPRINCIPAL': None, 
							        	'ZCOMPCONFDNAME': self.ZSECFORM13_FILER_dict['ZCOMPCONFDNAME'], 'ZCLASS_TITLE': None, 
							        	'ZVALUE': None, 'ZSHARES': None, 'ZSSHPRNAMTYPE': None, 'ZPUT_CALL': None, 'ZINVST_DISCRET': None, 
							        	'ZOTHERMANAGERS': None, 'ZVOTEAUTHSOLE': None, 'ZVOTEAUTHSHARED': None, 'ZVOTEAUTHNONE': None
							        	}
				while key != 'END_INFO_TABLE':
					key, match = self.parse_line()
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
					self.line = self.file.readline()

				self.ZSECFORM13F_INFO_arr.append(ZSECFORM13F_INFO_dict)

			self.line = self.file.readline()

	def upload_form(self, conn):
		conn.execute(ZSECFORM13.__table__.insert(), self.ZSECFORM13_dict)
		conn.execute(ZSECFORM13_FILER.__table__.insert(), self.ZSECFORM13_FILER_dict)
		for ZSECFORM13F_INFO_dict in self.ZSECFORM13F_INFO_arr:
			conn.execute(ZSECFORM13F_INFO.__table__.insert(), ZSECFORM13F_INFO_dict)

class form_3():

	def __init__(self, file, conn):
		self.patterns = {
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
			'FCOMP_CONFORMEDDNAME': re.compile(r'FORMER CONFORMED NAME:(?P<fcomp_name>.*)'),
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
		self.ZSECFORM3_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'ACCEPT_TIME': None, 'CIK_ISSUER': None,
		    'FORM_TYPE': None, 'ISSUER_SYMBOL': None, 'SEC_HEADER': None, 'DOC_FILE_COUNT': None, 'REPORT_PERIOD': None,
		    'DATE_FILED': None, 'DATE_CHANGED': None, 'VERSION': None, 'FILENAME': None, 'FILEDESCRIP': None, 'XML_VERSION': None,
		    'SCHEMA_VERSION': None, 'SECTION_16': None, 'SIGN_TITLE': None, 'SIGN_NAME': None, 'SIGN_DATE': None, 'DERV_TAB': False,
		    'NDERV_TAB': False, 'FTNOTE_FLG': False, 'ERDAT': None, 'ERNAME': None}
		self.ZSECFORM3_ISSUER_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'CIK_ISSUER': None,
		    'FORM_TYPE': None, 'ISSUER_SYMBOL': None, 'ISSU_CONFDNAME': None, 'SIC': None, 'IRS': None, 'STATE_INCORP': None,
		    'FISCAL_YEAREND': None, 'BUS_STREET1': None, 'BUS_STREET2': None, 'BUS_CITY': None, 'BUS_STATE': None, 'BUS_STATETXT': None, 
		    'BUS_ZIPCODE': None, 'BUS_PHONE': None, 'MAIL_STREET1': None, 'MAIL_STREET2': None, 'MAIL_CITY': None, 'MAIL_STATE': None, 
		    'MAIL_STATETXT': None, 'MAIL_ZIPCODE': None, 'FCOMP_CONFORMEDDNAME1': None, 'DATE_NAMECHANGE1': None, 
		    'FCOMP_CONFORMEDDNAME2': None, 'DATE_NAMECHANGE2': None, 'FCOMP_CONFORMEDDNAME3': None, 'DATE_NAMECHANGE3': None,}
		self.ZSECFORM3_REPTER_dict = {'MANDT': "100", 'ACCESSIONNO': None, 'SEC_DOC': None, 'CIK_REPORTER': None, 'DATE_REPORT': None,
		    'FORM_TYPE': None, 'REPT_CONFDNAME': None, 'FIRST_NAME': None, 'LAST_NAME': None, 'MIDDLE_NAME': None, 
		    'OFFICER_TITLE': None, 'SEC_ACT': None, 'SEC_FILENO': None, 'FILM_NO': None, 'BUS_STREET1': None, 'BUS_STREET2': None, 
		    'BUS_CITY': None, 'BUS_STATE': None, 'BUS_STATETXT': None, 'BUS_ZIPCODE': None, 'BUS_PHONE': None, 'MAIL_STREET1': None, 
		    'MAIL_STREET2': None, 'MAIL_CITY': None, 'MAIL_STATE': None, 'MAIL_STATETXT': None, 'MAIL_ZIPCODE': None, 
		    'FCOMP_CONFORMEDDNAME': None, 'DATE_NAMECHANGE': None, 'DIRECTOR': None, 'OFFICER': None, 'TENPERCENTOWNER': None, 
		    'OTHER': None, 'TEXT_OTHER': None, 'SIGN_TITLE': None, 'SIGN_NAME': None, 'SIGN_DATE': None,}
		    # datetimeobject = datetime.strptime(oldformat,'%Y%m%d')
			# newformat = datetimeobject.strftime('%Y-%m-%d')
		self.ZSECFORM3_DTAB_arr = []
		self.ZSECFORM3_NDTAB_arr = []
		self.ZSECFORM3_FTNOTE_arr = [] 
		self.file = file
		self.line = self.file.readline()
		self.parse_form()
		self.upload_form(conn)


	def parse_line(self):
	    for key, rx in self.patterns.items():
	        match = rx.search(self.line)
	        if match:
	        	return key, match
	    return None, None
	
	def parse_form(self):
		form_comp_count = ndh_index = dh_index = 1
		while self.line:
			key, match = self.parse_line()
			if not key:
				self.line = self.file.readline()
				continue
			elif key == 'ACCESSIONNO':
				self.ZSECFORM3_dict['ACCESSIONNO'] = match.group('accession_no').strip()
				self.ZSECFORM3_ISSUER_dict['ACCESSIONNO'] = match.group('accession_no').strip()
				self.ZSECFORM3_REPTER_dict['ACCESSIONNO'] = match.group('accession_no').strip()
			elif key == 'SEC_DOC':
				self.ZSECFORM3_dict['SEC_DOC'] = match.group('sec_doc').strip()
				self.ZSECFORM3_ISSUER_dict['SEC_DOC'] = match.group('sec_doc').strip()
				self.ZSECFORM3_REPTER_dict['SEC_DOC'] = match.group('sec_doc').strip()
			elif key == 'ACCEPT_TIME':
				self.ZSECFORM3_dict['ACCEPT_TIME'] = match.group('accept_time').strip()
			elif key == 'FORM_TYPE':
				self.ZSECFORM3_dict['FORM_TYPE'] = match.group('form_type').strip()
				self.ZSECFORM3_ISSUER_dict['FORM_TYPE'] = match.group('form_type').strip()
				self.ZSECFORM3_REPTER_dict['FORM_TYPE'] = match.group('form_type').strip()
			elif key == 'SEC_HEADER':
				self.ZSECFORM3_dict['SEC_HEADER'] = match.group('sec_header').strip()
			elif key == 'DOC_FILE_COUNT':
				self.ZSECFORM3_dict['DOC_FILE_COUNT'] = match.group('doc_count').strip()
			elif key == 'REPORT_PERIOD':
				self.ZSECFORM3_dict['REPORT_PERIOD'] = match.group('report_period').strip()
			elif key == 'DATE_FILED':
				self.ZSECFORM3_dict['DATE_FILED'] = match.group('filed_date').strip()
				# date_report = datetime.strptime(self.ZSECFORM3_dict['DATE_FILED'], '%Y%m%d')
				# self.ZSECFORM3_REPTER_dict['DATE_REPORT'] = date_report.strftime('%Y-%m-%d')
			elif key == 'DATE_CHANGED':
				self.ZSECFORM3_dict['DATE_CHANGED'] = match.group('change_date').strip()
			elif key == 'ISSUER':
				while key != 'REPORTER' and key != 'END_SEC_HEADER':
					key, match = self.parse_line()
					if key == 'CIK':
						self.ZSECFORM3_dict['CIK_ISSUER'] = match.group('cik').strip()
						self.ZSECFORM3_ISSUER_dict['CIK_ISSUER'] = match.group('cik').strip()
					elif key == 'CONFDNAME':
						self.ZSECFORM3_ISSUER_dict['ISSU_CONFDNAME'] = match.group('comp_name').strip()
					elif key == 'SIC':
						self.ZSECFORM3_ISSUER_dict['SIC'] = match.group('sic').strip()
					elif key == 'IRS':
						self.ZSECFORM3_ISSUER_dict['IRS'] = match.group('irs').strip()
					elif key == 'STATE_INCORP':
						self.ZSECFORM3_ISSUER_dict['STATE_INCORP'] = match.group('state_inc').strip()
					elif key == 'FISCAL_YEAREND':
						self.ZSECFORM3_ISSUER_dict['FISCAL_YEAREND'] = match.group('fiscal_year').strip()
					elif key == 'BUS_ADDR':
						while key != 'END_SEC_HEADER' and key != None:
							key, match = self.parse_line()
							if key == 'STREET1':
								self.ZSECFORM3_ISSUER_dict['BUS_STREET1'] = match.group('street1').strip()
							elif key == 'STREET2':
								self.ZSECFORM3_ISSUER_dict['BUS_STREET2'] = match.group('street2').strip()
							elif key == 'CITY':
								self.ZSECFORM3_ISSUER_dict['BUS_CITY'] = match.group('city').strip()
							elif key == 'STATE':
								self.ZSECFORM3_ISSUER_dict['BUS_STATE'] = match.group('state').strip()
							elif key == 'ZIPCODE':
								self.ZSECFORM3_ISSUER_dict['BUS_ZIPCODE'] = match.group('zip').strip()
							elif key == 'BUS_PHONE':
								self.ZSECFORM3_ISSUER_dict['BUS_PHONE'] = match.group('bus_phone').strip()
							self.line = self.file.readline()
					elif key == 'MAIL_ADDR':
						while key != 'END_SEC_HEADER' and key != None:
							key, match = self.parse_line()
							if key == 'STREET1':
								self.ZSECFORM3_ISSUER_dict['MAIL_STREET1'] = match.group('street1').strip()
							elif key == 'STREET2':
								self.ZSECFORM3_ISSUER_dict['MAIL_STREET2'] = match.group('street2').strip()
							elif key == 'CITY':
								self.ZSECFORM3_ISSUER_dict['MAIL_CITY'] = match.group('city').strip()
							elif key == 'STATE':
								self.ZSECFORM3_ISSUER_dict['MAIL_STATE'] = match.group('state').strip()
							elif key == 'ZIPCODE':
								self.ZSECFORM3_ISSUER_dict['MAIL_ZIPCODE'] = match.group('zip').strip()
							self.line = self.file.readline()
					elif key == 'FORMER_COMP':
						while key != 'END_SEC_HEADER' and key != None:
							key, match = self.parse_line()
							if key == 'FCOMP_CONFORMEDDNAME':
								self.ZSECFORM3_ISSUER_dict[f'FCOMP_CONFORMEDDNAME{form_comp_count}'] = match.group('fcomp_name').strip()
							elif key == 'DATE_NAMECHANGE':
								self.ZSECFORM3_ISSUER_dict[f'DATE_NAMECHANGE{form_comp_count}'] = match.group('date_name_change').strip()
							self.line = self.file.readline()
						form_comp_count += 1
					self.line = self.file.readline()
			elif key == 'REPORTER':
				while key != 'ISSUER' and key != 'END_SEC_HEADER':
					key, match = self.parse_line()
					if key == 'CIK':
						self.ZSECFORM3_REPTER_dict['CIK_REPORTER'] = match.group('cik').strip()
					elif key == 'CONFDNAME':
						self.ZSECFORM3_REPTER_dict['REPT_CONFDNAME'] = match.group('comp_name').strip()
					elif key == 'SEC_ACT':
						self.ZSECFORM3_REPTER_dict['SEC_ACT'] = match.group('sec_act').strip()
					elif key == 'SEC_FILENO':
						self.ZSECFORM3_REPTER_dict['SEC_FILENO'] = match.group('file_no').strip()
					elif key == 'FILM_NO':
						self.ZSECFORM3_REPTER_dict['FILM_NO'] = match.group('film_no').strip()
					elif key == 'BUS_ADDR':
						while key != 'END_SEC_HEADER' and key != None:
							key, match = self.parse_line()
							if key == 'STREET1':
								self.ZSECFORM3_REPTER_dict['BUS_STREET1'] = match.group('street1').strip()
							elif key == 'STREET2':
								self.ZSECFORM3_REPTER_dict['BUS_STREET2'] = match.group('street2').strip()
							elif key == 'CITY':
								self.ZSECFORM3_REPTER_dict['BUS_CITY'] = match.group('city').strip()
							elif key == 'STATE':
								self.ZSECFORM3_REPTER_dict['BUS_STATE'] = match.group('state').strip()
							elif key == 'ZIPCODE':
								self.ZSECFORM3_REPTER_dict['BUS_ZIPCODE'] = match.group('zip').strip()
							elif key == 'BUS_PHONE':
								self.ZSECFORM3_REPTER_dict['BUS_PHONE'] = match.group('bus_phone').strip()
							self.line = self.file.readline()
					elif key == 'FORMER_COMP':
						if not self.ZSECFORM3_REPTER_dict['FCOMP_CONFORMEDDNAME']:
							while key != 'END_SEC_HEADER' and key != None:
								key, match = self.parse_line()
								if key == 'FCOMP_CONFORMEDDNAME':
									self.ZSECFORM3_REPTER_dict['FCOMP_CONFORMEDDNAME'] = match.group('fcomp_name').strip()
								elif key == 'DATE_NAMECHANGE':
									self.ZSECFORM3_REPTER_dict['DATE_NAMECHANGE'] = match.group('date_name_change').strip()
								self.line = self.file.readline()
					self.line = self.file.readline()
			elif key == 'FILENAME':
				self.ZSECFORM3_dict['FILENAME'] = match.group('filename').strip()
				self.line = self.file.readline()
				key, match = self.parse_line()
				if key == 'FILEDESCRIP':
					self.ZSECFORM3_dict['FILEDESCRIP'] = match.group('filedescrip').strip()
			elif key == 'XML_VERSION':
				self.ZSECFORM3_dict['XML_VERSION'] = match.group('xml_version').strip()
			elif key == 'SCHEMA_VERSION':
				self.ZSECFORM3_dict['SCHEMA_VERSION'] = match.group('schema').strip()
			elif key == 'DATE_REPORT':
				self.ZSECFORM3_REPTER_dict['DATE_REPORT'] = match.group('date_report').strip()
			elif key == 'ISSUER_SYMBOL':
				self.ZSECFORM3_dict['ISSUER_SYMBOL'] = match.group('iss_symbol').strip()
				self.ZSECFORM3_ISSUER_dict['ISSUER_SYMBOL'] = match.group('iss_symbol').strip()
			elif key == 'SIGN_BLOCK':
				while key != 'END_SIGN_BLOCK':
					key, match = self.parse_line()
					if key == 'SIGN_TITLE':
						self.ZSECFORM3_dict['SIGN_TITLE'] = match.group('sign_title').strip()
						self.ZSECFORM3_REPTER_dict['SIGN_TITLE'] = match.group('sign_title').strip()
					elif key == 'SIGN_NAME':
						self.ZSECFORM3_dict['SIGN_NAME'] = match.group('sign_name').strip()
						self.ZSECFORM3_REPTER_dict['SIGN_NAME'] = match.group('sign_name').strip()
					elif key == 'SIGN_DATE':
						self.ZSECFORM3_dict['SIGN_DATE'] = match.group('sign_date').strip()
						self.ZSECFORM3_REPTER_dict['SIGN_DATE'] = match.group('sign_date').strip()
					self.line = self.file.readline()
			elif key == 'REPT_MAIL_ADDRESS':
				while key != 'END_REPT_MAIL_ADDRESS':
					key, match = self.parse_line()
					if key == 'REPT_MAIL_STREET1':
						self.ZSECFORM3_REPTER_dict['MAIL_STREET1'] = match.group('street1').strip()
					elif key == 'REPT_MAIL_STREET2':
						self.ZSECFORM3_REPTER_dict['MAIL_STREET2'] = match.group('street2').strip()
					elif key == 'REPT_MAIL_CITY':
						self.ZSECFORM3_REPTER_dict['MAIL_CITY'] = match.group('city').strip()
					elif key == 'REPT_MAIL_STATE':
						self.ZSECFORM3_REPTER_dict['MAIL_STATE'] = match.group('state').strip()
					elif key == 'REPT_MAIL_ZIPCODE':
						self.ZSECFORM3_REPTER_dict['MAIL_ZIPCODE'] = match.group('zip').strip()
					elif key == 'REPT_MAIL_STATETXT':
						self.ZSECFORM3_REPTER_dict['MAIL_STATETXT'] = match.group('state_txt').strip()
					self.line = self.file.readline()
			elif key == 'REPTOWN_RELATION':
				while key != 'END_REPTOWN_RELATION':
					key, match = self.parse_line()
					if key == 'DIRECTOR':
						self.ZSECFORM3_REPTER_dict['DIRECTOR'] = match.group('is_director').strip()
					elif key == 'OFFICER':
						self.ZSECFORM3_REPTER_dict['OFFICER'] = match.group('is_officer').strip()
					elif key == 'TENPERCENTOWNER':
						self.ZSECFORM3_REPTER_dict['TENPERCENTOWNER'] = match.group('is_tenpercent').strip()
					elif key == 'OTHER':
						self.ZSECFORM3_REPTER_dict['OTHER'] = match.group('is_other').strip()
					elif key == 'TEXT_OTHER':
						self.ZSECFORM3_REPTER_dict['OFFICER'] = match.group('otherText').strip()
					elif key == 'OFFICER_TITLE':
						self.ZSECFORM3_REPTER_dict['OFFICER_TITLE'] = match.group('off_title').strip()
					self.line = self.file.readline()
			elif key == 'NDH':
				ZSECFORM3_NDTAB_dict = {'MANDT': "100", 'ACCESSIONNO': self.ZSECFORM3_dict['ACCESSIONNO'], 'ACCESS_TRANXID': ndh_index, 
										'SECURITY_TYPETITLE': None, 'SECTITLE_FTNOTE': None, 'FORM_TYPE': self.ZSECFORM3_dict['FORM_TYPE'], 'SHARES': None, 
										'SHARE_FTNOTE': None, 'SHARE_VALUE': None, 'SHAREVALUE_FTNOTE': None, 'OWNERSHIPTYPE': None, 
										'OWNSHIP_FTNOTE': None, 'INDBENF_OWNER': None,'INDBENF_OWNER_FTNOTE': None}
				while key != 'END_NDH':
					key, match = self.parse_line()
					if key == 'SECURITY_TYPETITLE':
						while key != 'END_SECURITY_TYPETITLE':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_NDTAB_dict['SECURITY_TYPETITLE'] = match.group('value').strip()
							elif key == 'FTNOTE_ID':
								ZSECFORM3_NDTAB_dict['SECTITLE_FTNOTE'] = match.group('ftnote_id').strip()
							self.line = self.file.readline()
					elif key == 'SHARES':
						while key != 'END_SHARES':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_NDTAB_dict['SHARES'] = match.group('value').strip()
							elif key == 'FTNOTE_ID':
								ZSECFORM3_NDTAB_dict['SHARE_FTNOTE'] = match.group('ftnote_id').strip()
							self.line = self.file.readline()
					elif key == 'SHARE_VALUE':
						while key != 'END_SHARE_VALUE':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_NDTAB_dict['SHARE_VALUE'] = match.group('value').strip()
							elif key == 'FTNOTE_ID':
								ZSECFORM3_NDTAB_dict['SHAREVALUE_FTNOTE'] = match.group('ftnote_id').strip()
							self.line = self.file.readline()
					elif key == 'OWNERSHIPTYPE':
						while key != 'END_OWNERSHIPTYPE':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_NDTAB_dict['OWNERSHIPTYPE'] = match.group('value').strip()
							elif key == 'FTNOTE_ID':
								ZSECFORM3_NDTAB_dict['OWNSHIP_FTNOTE'] = match.group('ftnote_id').strip()
							self.line = self.file.readline()
					elif key == 'INDBENF_OWNER':
						while key != 'END_INDBENF_OWNER':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_NDTAB_dict['INDBENF_OWNER'] = match.group('value').strip()
							elif key == 'FTNOTE_ID':
								ZSECFORM3_NDTAB_dict['INDBENF_OWNER_FTNOTE'] = match.group('ftnote_id').strip()
							self.line = self.file.readline()
					self.line = self.file.readline()

				self.ZSECFORM3_NDTAB_arr.append(ZSECFORM3_NDTAB_dict)
				self.ZSECFORM3_dict['NDERV_TAB'] = True
				ndh_index += 1
			elif key == 'DH':
				ZSECFORM3_DTAB_dict = {'MANDT': "100", 'ACCESSIONNO': self.ZSECFORM3_dict['ACCESSIONNO'], 'ACCESS_TRANXID': dh_index, 
									   'DERIVSECURITY_TYPETITLE': None, 'DATE_EXCISE': None, 'DATE_EXPIRE': None, 
									   'SECURITY_TYPETITLE': None, 'SHARE_AMOUNT': None, 'EXPRICE_DERVSECURTY': None, 
									   'OWNERSHIPTYPE': None, 'INDBENF_OWNER': None}
				while key != 'END_DH':
					key, match = self.parse_line()
					if key == 'DERIVSECURITY_TYPETITLE':
						while key != 'END_DERIVSECURITY_TYPETITLE':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_DTAB_dict['DERIVSECURITY_TYPETITLE'] = match.group('value').strip()
							self.line = self.file.readline()
					elif key == 'EXPRICE_DERVSECURTY':
						while key != 'END_EXPRICE_DERVSECURTY':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_DTAB_dict['EXPRICE_DERVSECURTY'] = match.group('value').strip()
							self.line = self.file.readline()
					elif key == 'DATE_EXCISE':
						while key != 'END_DATE_EXCISE':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_DTAB_dict['DATE_EXCISE'] = match.group('value').strip()
							self.line = self.file.readline()
					elif key == 'DATE_EXPIRE':
						while key != 'END_DATE_EXPIRE':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_DTAB_dict['DATE_EXPIRE'] = match.group('value').strip()
							self.line = self.file.readline()
					elif key == 'UNDERSECURITY_TYPETITLE':
						while key != 'END_UNDERSECURITY_TYPETITLE':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_DTAB_dict['SECURITY_TYPETITLE'] = match.group('value').strip()
							self.line = self.file.readline()
					elif key == 'SHARE_AMOUNT':
						while key != 'END_SHARE_AMOUNT':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_DTAB_dict['SHARE_AMOUNT'] = match.group('value').strip()
							self.line = self.file.readline()
					elif key == 'OWNERSHIPTYPE':
						while key != 'END_OWNERSHIPTYPE':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_DTAB_dict['OWNERSHIPTYPE'] = match.group('value').strip()
							self.line = self.file.readline()
					elif key == 'INDBENF_OWNER':
						while key != 'END_INDBENF_OWNER':
							key, match = self.parse_line()
							if key == 'VALUE':
								ZSECFORM3_DTAB_dict['INDBENF_OWNER'] = match.group('value').strip()
							self.line = self.file.readline()
					self.line = self.file.readline()

				self.ZSECFORM3_DTAB_arr.append(ZSECFORM3_DTAB_dict)
				self.ZSECFORM3_dict['DERV_TAB'] = True
				dh_index += 1
			elif key == 'FOOTNOTE':
				self.ZSECFORM3_dict['FTNOTE_FLG'] = True
				self.ZSECFORM3_FTNOTE_arr.append({'MANDT': "100", 'ACCESSIONNO': self.ZSECFORM3_dict['ACCESSIONNO'], 
											 'SEC_DOC': self.ZSECFORM3_dict['SEC_DOC'], 'FOOTNOTE_ID': match.group('id').strip(), 
											 'FOOTNOTE_TXT': match.group('txt').strip()})

			self.line = self.file.readline()

	def upload_form(self, conn):
		conn.execute(ZSECFORM3.__table__.insert(), self.ZSECFORM3_dict)
		conn.execute(ZSECFORM3_ISSUER.__table__.insert(), self.ZSECFORM3_ISSUER_dict)
		conn.execute(ZSECFORM3_REPTER.__table__.insert(), self.ZSECFORM3_REPTER_dict)
		for ZSECFORM3_FTNOTE_dict in self.ZSECFORM3_FTNOTE_arr:
			conn.execute(ZSECFORM3_FTNOTE.__table__.insert(), ZSECFORM3_FTNOTE_dict)
		for ZSECFORM3_DTAB_dict in self.ZSECFORM3_DTAB_arr:
			conn.execute(ZSECFORM3_DTAB.__table__.insert(), ZSECFORM3_DTAB_dict)
		for ZSECFORM3_NDTAB_dict in self.ZSECFORM3_NDTAB_arr:
			conn.execute(ZSECFORM3_NDTAB.__table__.insert(), ZSECFORM3_NDTAB_dict)