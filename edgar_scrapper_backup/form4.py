rx_4 = {
    'ACCESSIONNO': re.compile(r'ACCESSION NUMBER:(?P<accession_no>.*)'),
    'SEC_DOC': re.compile(r'<SEC-DOCUMENT>(?P<sec_doc>.*)'),
    'ACCEPT_TIME': re.compile(r'<ACCEPTANCE-DATETIME>(?P<accept_time>.*)'),
    'SEC_HEADER': re.compile(r'<SEC-HEADER>(?P<sec_header>.*)'),
    'DOC_FILE_COUNT': re.compile(r'PUBLIC DOCUMENT COUNT:(?P<doc_count>.*)'),
    'REPORT_PERIOD': re.compile(r'CONFORMED PERIOD OF REPORT:(?P<report_period>.*)'),
    'DATE_FILED': re.compile(r'FILED AS OF DATE:(?P<filed_date>.*)'),
    'DATE_CHANGED': re.compile(r'DATE AS OF CHANGE:(?P<change_date>.*)'),
    'REPORTER': re.compile(r'REPORTING-OWNER:'),
    'OWN_DATA': re.compile(r'OWNER DATA:'),
    'ISSUER': re.compile(r'ISSUER:'),
    'COMP_DATA': re.compile(r'COMPANY DATA:'),
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
    'SIGN_NAME': re.compile(r'<signatureName>(?P<sign_name>.*)</signatureName>'),
    'TITLE': re.compile(r'Title:(?P<title>.*)'),
    'NAME': re.compile(r'Name:(?P<name>.*)'),
    'SIGN_DATE': re.compile(r'<signatureDate>(?P<sign_date>.*)</signatureDate>'),
    'END_SIGN_BLOCK': re.compile(r'</ownerSignature>'),
    'SCHEMA_VERSION': re.compile(r'<schemaVersion>(?P<schema>.*)</schemaVersion>'),
    'SECTION_16': re.compile(r'<notSubjectToSection16>(?P<section16>.*)</notSubjectToSection16>'),
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
    'REPTOWN': re.compile(r'<reportingOwner>'),
    'REPTOWN_CIK': re.compile(r'<rptOwnerCik>(?P<cik>.*)</rptOwnerCik>'),
    'REPTOWN_RELATION': re.compile(r'<reportingOwnerRelationship>'),
    'DIRECTOR': re.compile(r'<isDirector>(?P<is_director>.*)</isDirector>'),
    'OFFICER': re.compile(r'<isOfficer>(?P<is_officer>.*)</isOfficer>'),
    'TENPERCENTOWNER': re.compile(r'<isTenPercentOwner>(?P<is_tenpercent>.*)</isTenPercentOwner>'),
    'OTHER': re.compile(r'<isOther>(?P<is_other>.*)</isOther>'),
    'TEXT_OTHER': re.compile(r'<otherText>(?P<otherText>.*)</otherText>'),
    'OFFICER_TITLE': re.compile(r'<officerTitle>(?P<off_title>.*)</officerTitle>'),
    'END_REPTOWN_RELATION': re.compile(r'</reportingOwnerRelationship>'),
    'END_REPTOWN': re.compile(r'</reportingOwner>'),
    'NDH': re.compile(r'<nonDerivativeTransaction>'),
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
    'END_NDH': re.compile(r'</nonDerivativeTransaction>'),
    'VALUE': re.compile(r'<value>(?P<value>.*)</value>'),
    'FTNOTE_ID': re.compile(r'<footnoteId id="(?P<ftnote_id>.*)"/>'),
    'DH': re.compile(r'<derivativeTransaction>'),
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
    'END_DH': re.compile(r'</derivativeTransaction>'),
    'FOOTNOTE': re.compile(r'<footnote id=\"(?P<id>.*)\">(?P<txt>.*)</footnote>'),
}

def parse_line_form4(line, func_time):
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
        lines = file.split('\n')
        print(lines)
        line = file.readline()
        while line:
            key, match = parse_line_form4(line, func_time)
            if not key:
                line = file.readline()
                continue
            elif key == 'ACCESSIONNO':
                ZSECFORM4_dict['ACCESSIONNO'] = match.group('accession_no').strip()
                ZSECFORM4_ISSUER_dict['ACCESSIONNO'] = match.group('accession_no').strip()
                ZSECFORM4_REPTER_common_dict['ACCESSIONNO'] = match.group('accession_no').strip()
            elif key == 'SEC_DOC':
                ZSECFORM4_dict['SEC_DOC'] = match.group('sec_doc').strip()
                ZSECFORM4_ISSUER_dict['SEC_DOC'] = match.group('sec_doc').strip()
                ZSECFORM4_REPTER_common_dict['SEC_DOC'] = match.group('sec_doc').strip()
            elif key == 'ACCEPT_TIME':
                ZSECFORM4_dict['ACCEPT_TIME'] = match.group('accept_time').strip()
            elif key == 'FORM_TYPE':
                ZSECFORM4_dict['FORM_TYPE'] = match.group('form_type').strip()
                ZSECFORM4_ISSUER_dict['FORM_TYPE'] = match.group('form_type').strip()
                ZSECFORM4_REPTER_common_dict['FORM_TYPE'] = match.group('form_type').strip()
            elif key == 'SEC_HEADER':
                ZSECFORM4_dict['SEC_HEADER'] = match.group('sec_header').strip()
            elif key == 'DOC_FILE_COUNT':
                ZSECFORM4_dict['DOC_FILE_COUNT'] = match.group('doc_count').strip()
            elif key == 'REPORT_PERIOD':
                ZSECFORM4_dict['REPORT_PERIOD'] = match.group('report_period').strip()
            elif key == 'DATE_FILED':
                ZSECFORM4_dict['DATE_FILED'] = match.group('filed_date').strip()
            elif key == 'DATE_CHANGED':
                ZSECFORM4_dict['DATE_CHANGED'] = match.group('change_date').strip()
            elif key == 'COMP_DATA':
                while key != 'END_SEC_HEADER' and key != 'REPORTER':
                    key, match = parse_line_form4(line, func_time)
                    if key == 'CIK':
                        ZSECFORM4_dict['CIK_ISSUER'] = match.group('cik').strip()
                        ZSECFORM4_ISSUER_dict['CIK_ISSUER'] = match.group('cik').strip()
                    elif key == 'CONFDNAME':
                        ZSECFORM4_ISSUER_dict['ISSU_CONFDNAME'] = match.group('comp_name').strip()
                    elif key == 'SIC':
                        ZSECFORM4_ISSUER_dict['SIC'] = match.group('sic').strip()
                    elif key == 'IRS':
                        ZSECFORM4_ISSUER_dict['IRS'] = match.group('irs').strip()
                    elif key == 'STATE_INCORP':
                        ZSECFORM4_ISSUER_dict['STATE_INCORP'] = match.group('state_inc').strip()
                    elif key == 'FISCAL_YEAREND':
                        ZSECFORM4_ISSUER_dict['FISCAL_YEAREND'] = match.group('fiscal_year').strip()
                    elif key == 'BUS_ADDR':
                        while key and key != 'END_SEC_HEADER':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'STREET1':
                                ZSECFORM4_ISSUER_dict['BUS_STREET1'] = match.group('street1').strip()
                            elif key == 'STREET2':
                                ZSECFORM4_ISSUER_dict['BUS_STREET2'] = match.group('street2').strip()
                            elif key == 'CITY':
                                ZSECFORM4_ISSUER_dict['BUS_CITY'] = match.group('city').strip()
                            elif key == 'STATE':
                                ZSECFORM4_ISSUER_dict['BUS_STATE'] = match.group('state').strip()
                            elif key == 'ZIPCODE':
                                ZSECFORM4_ISSUER_dict['BUS_ZIPCODE'] = match.group('zip').strip()
                            elif key == 'BUS_PHONE':
                                ZSECFORM4_ISSUER_dict['BUS_PHONE'] = match.group('bus_phone').strip()
                            line = file.readline()
                    elif key == 'MAIL_ADDR':
                        while key and key != 'END_SEC_HEADER':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'STREET1':
                                ZSECFORM4_ISSUER_dict['MAIL_STREET1'] = match.group('street1').strip()
                            elif key == 'STREET2':
                                ZSECFORM4_ISSUER_dict['MAIL_STREET2'] = match.group('street2').strip()
                            elif key == 'CITY':
                                ZSECFORM4_ISSUER_dict['MAIL_CITY'] = match.group('city').strip()
                            elif key == 'STATE':
                                ZSECFORM4_ISSUER_dict['MAIL_STATE'] = match.group('state').strip()
                            elif key == 'ZIPCODE':
                                ZSECFORM4_ISSUER_dict['MAIL_ZIPCODE'] = match.group('zip').strip()
                            line = file.readline()
                    elif key == 'FORMER_COMP':
                        while key and key != 'END_SEC_HEADER':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'FCOMP_CONFORMEDNAME':
                                ZSECFORM4_ISSUER_dict[f'FCOMP_CONFORMEDNAME{form_comp_count}'] = match.group('fcomp_name').strip()
                            elif key == 'DATE_NAMECHANGE':
                                ZSECFORM4_ISSUER_dict[f'DATE_NAMECHANGE{form_comp_count}'] = match.group('date_name_change').strip()
                            line = file.readline()
                        form_comp_count += 1
                    line = file.readline()
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
                    key, match = parse_line_form4(line, func_time)
                    if key == 'CIK':
                        ZSECFORM4_REPTER_dict['CIK_REPORTER'] = match.group('cik').strip()
                    elif key == 'CONFDNAME':
                        ZSECFORM4_REPTER_dict['REPT_CONFDNAME'] = match.group('comp_name').strip()
                    elif key == 'SEC_ACT':
                        ZSECFORM4_REPTER_dict['SEC_ACT'] = match.group('sec_act').strip()
                    elif key == 'SEC_FILENO':
                        ZSECFORM4_REPTER_dict['SEC_FILENO'] = match.group('file_no').strip()
                    elif key == 'FILM_NO':
                        ZSECFORM4_REPTER_dict['FILM_NO'] = match.group('film_no').strip()
                    elif key == 'BUS_ADDR':
                        while key and key != 'END_SEC_HEADER':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'STREET1':
                                ZSECFORM4_REPTER_dict['BUS_STREET1'] = match.group('street1').strip()
                            elif key == 'STREET2':
                                ZSECFORM4_REPTER_dict['BUS_STREET2'] = match.group('street2').strip()
                            elif key == 'CITY':
                                ZSECFORM4_REPTER_dict['BUS_CITY'] = match.group('city').strip()
                            elif key == 'STATE':
                                ZSECFORM4_REPTER_dict['BUS_STATE'] = match.group('state').strip()
                            elif key == 'ZIPCODE':
                                ZSECFORM4_REPTER_dict['BUS_ZIPCODE'] = match.group('zip').strip()
                            elif key == 'BUS_PHONE':
                                ZSECFORM4_REPTER_dict['BUS_PHONE'] = match.group('bus_phone').strip()
                            line = file.readline()
                    elif key == 'MAIL_ADDR':
                        while key and key != 'END_SEC_HEADER':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'STREET1':
                               ZSECFORM4_REPTER_dict['MAIL_STREET1'] = match.group('street1').strip()
                            elif key == 'STREET2':
                               ZSECFORM4_REPTER_dict['MAIL_STREET2'] = match.group('street2').strip()
                            elif key == 'CITY':
                               ZSECFORM4_REPTER_dict['MAIL_CITY'] = match.group('city').strip()
                            elif key == 'STATE':
                               ZSECFORM4_REPTER_dict['MAIL_STATE'] = match.group('state').strip()
                            elif key == 'ZIPCODE':
                               ZSECFORM4_REPTER_dict['MAIL_ZIPCODE'] = match.group('zip').strip()
                            line = file.readline()
                    elif key == 'FORMER_COMP':
                        if not ZSECFORM4_REPTER_dict['FCOMP_CONFORMEDNAME']:
                            while key and key != 'END_SEC_HEADER':
                                key, match = parse_line_form4(line, func_time)
                                if key == 'FCOMP_CONFORMEDNAME':
                                    ZSECFORM4_REPTER_dict['FCOMP_CONFORMEDNAME'] = match.group('fcomp_name').strip()
                                elif key == 'DATE_NAMECHANGE':
                                    ZSECFORM4_REPTER_dict['DATE_NAMECHANGE'] = match.group('date_name_change').strip()
                                line = file.readline()
                    line = file.readline()
                ZSECFORM4_REPTER_arr.append(ZSECFORM4_REPTER_dict)
            elif key == 'FILENAME':
                ZSECFORM4_dict['FILENAME'] = match.group('filename').strip()
                line = file.readline()
                key, match = parse_line_form4(line, func_time)
                if key == 'FILEDESCRIP':
                    ZSECFORM4_dict['FILEDESCRIP'] = match.group('filedescrip').strip()
            elif key == 'XML_VERSION':
                ZSECFORM4_dict['XML_VERSION'] = match.group('xml_version').strip()
            elif key == 'SCHEMA_VERSION':
                ZSECFORM4_dict['SCHEMA_VERSION'] = match.group('schema').strip()
            elif key == 'DATE_REPORT':
                ZSECFORM4_REPTER_common_dict['DATE_REPORT'] = match.group('date_report').strip()
            elif key == 'ISSUER_SYMBOL':
                ZSECFORM4_dict['ISSUER_SYMBOL'] = match.group('iss_symbol').strip()
                ZSECFORM4_ISSUER_dict['ISSUER_SYMBOL'] = match.group('iss_symbol').strip()

            elif key == 'REPTOWN':
                while key != 'END_REPTOWN':
                    key, match = parse_line_form4(line, func_time)
                    if key == 'REPTOWN_CIK':
                        reptown_cik = match.group('cik').strip()
                        index = next((ix for (ix, d) in enumerate(ZSECFORM4_REPTER_arr) if d["CIK_REPORTER"].lower() == reptown_cik), None)
                        if not index:
                            break
                        else:
                            while key != 'END_REPTOWN':
                                key, match = parse_line_form4(line, func_time)
                                if key == 'DIRECTOR':
                                    ZSECFORM4_REPTER_arr[index]['DIRECTOR'] = match.group('is_director').strip()
                                elif key == 'OFFICER':
                                    ZSECFORM4_REPTER_arr[index]['OFFICER'] = match.group('is_officer').strip()
                                elif key == 'TENPERCENTOWNER':
                                    ZSECFORM4_REPTER_arr[index]['TENPERCENTOWNER'] = match.group('is_tenpercent').strip()
                                elif key == 'OTHER':
                                    ZSECFORM4_REPTER_arr[index]['OTHER'] = match.group('is_other').strip()
                                elif key == 'TEXT_OTHER':
                                    ZSECFORM4_REPTER_arr[index]['OFFICER'] = match.group('otherText').strip()
                                elif key == 'OFFICER_TITLE':
                                    ZSECFORM4_REPTER_arr[index]['OFFICER_TITLE'] = match.group('off_title').strip()
                                line = file.readline()
                            break
                    line = file.readline()

            elif key == 'NDH':
                ZSECFORM4_NDTAB_dict = {'MANDT': "100", 'ACCESSIONNO': ZSECFORM4_dict['ACCESSIONNO'], 'ACCESS_TRANXID': f"{ndh_index}", 
                                        'DATE_TRANS': None, 'DATE_EXECUTION': None, 'TRANS_CODE': None, 'TRANSCODE_FTNOTE': None,
                                        'FORM_TYPE': ZSECFORM4_dict['FORM_TYPE'], 'SECURITY_TYPETITLE': None, 'SECTITLE_FTNOTE': None, 
                                        'SWAP': None, 'SHARES': None, 'SHARE_FTNOTE': None, 'ACQ_DISPOSED': None, 'SHARE_VALUE': None, 
                                        'SHAREVALUE_FTNOTE': None,  'SHARES_AFTER': None, 'SHAREAFT_FTNOTE': None,'OWNERSHIPTYPE': None, 
                                        'OWNSHIP_FTNOTE': None, 'INDBENF_OWNER': None,'INDBENF_OWNER_FTNOTE': None}
                while key != 'END_NDH':
                    key, match = parse_line_form4(line, func_time)
                    if key == 'SECURITY_TYPETITLE':
                        while key != 'END_SECURITY_TYPETITLE':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_NDTAB_dict['SECURITY_TYPETITLE'] = match.group('value').strip()
                            elif key == 'FTNOTE_ID':
                                ZSECFORM4_NDTAB_dict['SECTITLE_FTNOTE'] = match.group('ftnote_id').strip()
                            line = file.readline()
                    elif key == 'SHARES':
                        while key != 'END_SHARES':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_NDTAB_dict['SHARES'] = match.group('value').strip()
                            elif key == 'FTNOTE_ID':
                                ZSECFORM4_NDTAB_dict['SHARE_FTNOTE'] = match.group('ftnote_id').strip()
                            line = file.readline()
                    elif key == 'SHARE_VALUE':
                        while key != 'END_SHARE_VALUE':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_NDTAB_dict['SHARE_VALUE'] = match.group('value').strip()
                            elif key == 'FTNOTE_ID':
                                ZSECFORM4_NDTAB_dict['SHAREVALUE_FTNOTE'] = match.group('ftnote_id').strip()
                            line = file.readline()
                    elif key == 'OWNERSHIPTYPE':
                        while key != 'END_OWNERSHIPTYPE':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_NDTAB_dict['OWNERSHIPTYPE'] = match.group('value').strip()
                            elif key == 'FTNOTE_ID':
                                ZSECFORM4_NDTAB_dict['OWNSHIP_FTNOTE'] = match.group('ftnote_id').strip()
                            line = file.readline()
                    elif key == 'INDBENF_OWNER':
                        while key != 'END_INDBENF_OWNER':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_NDTAB_dict['INDBENF_OWNER'] = match.group('value').strip()
                            elif key == 'FTNOTE_ID':
                                ZSECFORM4_NDTAB_dict['INDBENF_OWNER_FTNOTE'] = match.group('ftnote_id').strip()
                            line = file.readline()
                    line = file.readline()

                ZSECFORM4_NDTAB_arr.append(ZSECFORM4_NDTAB_dict)
                ZSECFORM4_dict['NDERV_TAB'] = True
                ndh_index += 1
            elif key == 'DH':
                ZSECFORM4_DTAB_dict = {'MANDT': "100", 'ACCESSIONNO': ZSECFORM4_dict['ACCESSIONNO'], 'ACCESS_TRANXID': f"{dh_index}",
                                       'DATE_TRANS': None, 'DATE_EXECUTION': None, 'TRANS_CODE': None, 
                                       'FORM_TYPE': ZSECFORM4_dict['FORM_TYPE'], 'SWAP': None, 'ACQ_DISPOSED':None, 
                                       'DERIVSECURITY_TYPETITLE': None, 'DATE_EXCISE': None, 'DATE_EXPIRE': None, 
                                       'SECURITY_TYPETITLE': None, 'SHARE_AMOUNT': None, 'EXPRICE_DERVSECURTY': None, 
                                       'PRICE_DERIV': None, 'SHARES_AFTER': None, 'OWNERSHIPTYPE': None, 'INDBENF_OWNER': None}

                while key != 'END_DH':
                    key, match = parse_line_form4(line, func_time)
                    if key == 'DERIVSECURITY_TYPETITLE':
                        while key != 'END_DERIVSECURITY_TYPETITLE':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_DTAB_dict['DERIVSECURITY_TYPETITLE'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'EXPRICE_DERVSECURTY':
                        while key != 'END_EXPRICE_DERVSECURTY':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_DTAB_dict['EXPRICE_DERVSECURTY'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'DATE_EXCISE':
                        while key != 'END_DATE_EXCISE':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_DTAB_dict['DATE_EXCISE'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'DATE_EXPIRE':
                        while key != 'END_DATE_EXPIRE':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_DTAB_dict['DATE_EXPIRE'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'UNDERSECURITY_TYPETITLE':
                        while key != 'END_UNDERSECURITY_TYPETITLE':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_DTAB_dict['SECURITY_TYPETITLE'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'SHARE_AMOUNT':
                        while key != 'END_SHARE_AMOUNT':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_DTAB_dict['SHARE_AMOUNT'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'OWNERSHIPTYPE':
                        while key != 'END_OWNERSHIPTYPE':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_DTAB_dict['OWNERSHIPTYPE'] = match.group('value').strip()
                            line = file.readline()
                    elif key == 'INDBENF_OWNER':
                        while key != 'END_INDBENF_OWNER':
                            key, match = parse_line_form4(line, func_time)
                            if key == 'VALUE':
                                ZSECFORM4_DTAB_dict['INDBENF_OWNER'] = match.group('value').strip()
                            line = file.readline()
                    line = file.readline()

                ZSECFORM4_DTAB_arr.append(ZSECFORM4_DTAB_dict)
                ZSECFORM4_dict['DERV_TAB'] = True
                dh_index += 1
            elif key == 'FOOTNOTE':
                ZSECFORM4_dict['FTNOTE_FLG'] = True
                ZSECFORM4_FTNOTE_arr.append({'MANDT': "100", 'ACCESSIONNO': ZSECFORM4_dict['ACCESSIONNO'], 
                                             'SEC_DOC': ZSECFORM4_dict['SEC_DOC'], 'FOOTNOTE_ID': match.group('id').strip(), 
                                             'FOOTNOTE_TXT': match.group('txt').strip()})
            elif key == 'SIGN_BLOCK':
                line = file.readline()
                key, match = parse_line_form4(line, func_time)
                if key == 'SIGN_NAME':
                    sign_names = match.group('sign_name').strip().split(",")
                    index = next((ix for (ix, d) in enumerate(ZSECFORM4_REPTER_arr) if d["REPT_CONFDNAME"].lower() == sign_names[0].lower()), None)
                    if index:
                        if len(sign_names) == 1:
                            ZSECFORM4_REPTER_arr[index]['SIGN_NAME'] = sign_names[0]
                        else:
                            ZSECFORM4_REPTER_arr[index]['SIGN_NAME'] = sign_names[0]
                            for sign_name in sign_names:
                                key, match = parse_line_form4(line, func_time)
                                if key == 'TITLE':
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
                        line = file.readline()
                        key, match = parse_line_form4(line, func_time)
                        if key == 'SIGN_DATE':
                            ZSECFORM4_REPTER_arr[index]['SIGN_DATE'] = match.group('sign_date').strip()

            line = file.readline()

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