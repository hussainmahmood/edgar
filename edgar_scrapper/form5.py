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
    'FORM3': re.compile(r'<form3HoldingsReported>(?P<form3>.*)</form3HoldingsReported>'),
    'FORM4': re.compile(r'<form4TransactionsReported>(?P<form4>.*)</form4TransactionsReported>'),
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
    'SWAP': re.compile(r'<equitySwapInvolved>(?P<swap>.*)</equitySwapInvolved>'),
    'END_TRANSCODING': re.compile(r'</transactionCoding>'),
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
        'SIGN_NAME': None, 'SIGN_DATE': None, 'DERV_TAB': False,'NDERV_TAB': False, 'FTNOTE_FLG': False, 'ERDAT': None, 'ERNAME': None}
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