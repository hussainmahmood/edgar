# coding: utf-8
from sqlalchemy import Column, Date, PrimaryKeyConstraint, BigInteger, Integer, Numeric, Boolean, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


# class ZSECFORM13(Base):
#     __tablename__ = 'ZSECFORM13'
#     __table_args__ = ()

#     MANDT = Column(String)
#     ZACCESSIONNO = Column(String(20), primary_key=True)
#     ZSECDOC = Column(String)
#     ZSEC_ACCEPTTIME = Column(String(14))
#     ZCIK_ISSUER = Column(String)
#     ZFORM_TYPE = Column(String)
#     ZISSUER_SYMBOL = Column(String)		# needs consult
#     ZSECHEADER = Column(String)
#     ZDOC_COUNT = Column(Integer)
#     ZREPORT_PERIOD = Column(Date)
#     ZDATE_FILED = Column(Date)
#     ZDATE_CHANGED = Column(Date)
#     ZAMEND = Column(String)			# needs consult
#     ZAMEND_NUMBER = Column(Integer)		# needs consult
#     ZAMEND_RESTATE = Column(String)		# needs consult
#     ZAMEND_NEWHOLDING = Column(String)	# needs consult
#     VERSION = Column(String)			# needs consult
#     ZSEC_FILENO = Column(String)		
#     ZSEC_FILENAME = Column(String)		# needs consult
#     ZFILE_DESCRIP = Column(String)		# needs consult
#     ZXML_VERSION = Column(String)
#     ZSCHEMA_VERSION = Column(String)	# needs consult
#     ZSECTION16 = Column(String)		# needs consult
#     ZSIGN_TITLE = Column(String)
#     ZSIGN_NAME = Column(String)
#     ZSIGN_DATE = Column(Date)
#     ERDAT = Column(Date)			# needs consult
#     ERNAME = Column(String)			# needs consult
#     ZTOTAL_TABENTRY = Column(String)         
#     ZTOTAL_TABVALUE = Column(Integer)

# class ZSECFORM13_FILER(Base):
#     __tablename__ = 'ZSECFORM13_FILER'
#     __table_args__ = ()

#     MANDT = Column(String)
#     ZACCESSIONNO = Column(String(20), primary_key=True)
#     ZCIK_ISSUER = Column(String)
#     ZCOMPCONFDNAME = Column(String)
#     ZSEC_IRSNO = Column(String)
#     ZINCORP_STATE = Column(String)
#     ZFISCAL_YREND = Column(String)
#     BUS_STRAS = Column(String)
#     BUS_CITY = Column(String)
#     BUS_REGION = Column(String)
#     BUS_BEZEI20 = Column(String)
#     BUS_POST_CODE = Column(String)
#     BUS_TELF = Column(String)
#     MAIL_STRAS = Column(String)
#     MAIL_CITY = Column(String)
#     MAIL_REGION = Column(String)
#     MAIL_POST_CODE = Column(String)
#     ZFCOMPCONFDNAME1 = Column(String)
#     ZDATE_NAMECHANGE1 = Column(Date)
#     ZFCOMPCONFDNAME2 = Column(String)
#     ZDATE_NAMECHANGE2 = Column(Date)
#     ZFCOMPCONFDNAME3 = Column(String)
#     ZDATE_NAMECHANGE3 = Column(Date)


# class ZSECFORM13F_INFO(Base):
#     __tablename__ = 'ZSECFORM13F_INFO'
#     __table_args__ = (PrimaryKeyConstraint('ZACCESSIONNO', 'ZCIK_ISSUER', 'ZCUSIP', 'ZINVST_DISCRET'),)

#     MANDT = Column(String)
#     ZACCESSIONNO = Column(String(20), ForeignKey("ZSECFORM13.ZACCESSIONNO"))
#     ZCIK_ISSUER = Column(String)
#     ZCUSIP = Column(String)
#     ZSHAREPRINCIPAL = Column(String)
#     ZCOMPCONFDNAME = Column(String)
#     ZCLASS_TITLE = Column(String)
#     ZVALUE = Column(Numeric(precision=25, scale=2))
#     ZSHARES = Column(String)
#     ZSSHPRNAMTYPE = Column(String)
#     ZPUT_CALL = Column(String)
#     ZINVST_DISCRET = Column(String)
#     ZOTHERMANAGERS = Column(String)
#     ZVOTEAUTHSOLE = Column(Integer)
#     ZVOTEAUTHSHARED = Column(Integer)
#     ZVOTEAUTHNONE = Column(Integer)

class ZSECFORM3(Base):
    __tablename__ = 'ZSECFORM3'
    __table_args__ = ()

    MANDT = Column(String)
    ACCESSIONNO = Column(String(20), primary_key=True)
    SEC_DOC = Column(String)
    ACCEPT_TIME = Column(String)
    CIK_ISSUER = Column(String)
    FORM_TYPE = Column(String)
    ISSUER_SYMBOL = Column(String)
    SEC_HEADER = Column(String)
    DOC_FILE_COUNT = Column(Integer)
    REPORT_PERIOD = Column(Date)
    DATE_FILED = Column(Date)
    DATE_CHANGED = Column(Date)
    VERSION = Column(String)       
    FILENAME = Column(String)   
    FILEDESCRIP = Column(String)   
    XML_VERSION = Column(String)
    SCHEMA_VERSION = Column(String) 
    SECTION_16 = Column(String)   
    SIGN_TITLE = Column(String)
    SIGN_NAME = Column(String)
    SIGN_DATE = Column(Date)
    DERV_TAB = Column(Boolean)
    NDERV_TAB = Column(Boolean)
    FTNOTE_FLG = Column(Boolean)
    ERDAT = Column(Date)
    ERNAME = Column(String)

class ZSECFORM3_ISSUER(Base):
    __tablename__ = 'ZSECFORM3_ISSUER'
    __table_args__ = ()

    MANDT = Column(String)
    ACCESSIONNO = Column(String(20), primary_key=True)
    CIK_ISSUER = Column(String)
    SEC_DOC = Column(String)
    FORM_TYPE = Column(String)
    ISSUER_SYMBOL = Column(String) 
    ISSU_CONFDNAME = Column(String)
    SIC = Column(String)
    IRS = Column(String)
    STATE_INCORP = Column(String)
    FISCAL_YEAREND = Column(String)
    BUS_STREET1 = Column(String)
    BUS_STREET2 = Column(String)
    BUS_CITY  = Column(String)
    BUS_STATE = Column(String)
    BUS_STATETXT = Column(String)
    BUS_ZIPCODE = Column(String)
    BUS_PHONE = Column(String)
    MAIL_STREET1 = Column(String)
    MAIL_STREET2 = Column(String)
    MAIL_CITY = Column(String)
    MAIL_STATE = Column(String)
    MAIL_STATETXT = Column(String)
    MAIL_ZIPCODE = Column(String)
    FCOMP_CONFORMEDDNAME1 = Column(String)
    DATE_NAMECHANGE1 = Column(Date)
    FCOMP_CONFORMEDDNAME2 = Column(String)
    DATE_NAMECHANGE2 = Column(Date)
    FCOMP_CONFORMEDDNAME3 = Column(String)
    DATE_NAMECHANGE3 = Column(Date)

class ZSECFORM3_REPTER(Base):
    __tablename__ = 'ZSECFORM3_REPTER'
    __table_args__ = ()

    MANDT = Column(String)
    ACCESSIONNO = Column(String(20), primary_key=True)
    CIK_REPORTER = Column(String)
    SEC_DOC = Column(String)
    DATE_REPORT = Column(Date)
    FORM_TYPE = Column(String)
    REPT_CONFDNAME = Column(String)
    FIRST_NAME = Column(String)
    LAST_NAME = Column(String)
    MIDDLE_NAME = Column(String)
    OFFICER_TITLE = Column(String)
    SEC_ACT = Column(String)
    SEC_FILENO = Column(String)
    FILM_NO = Column(String)
    BUS_STREET1 = Column(String)
    BUS_STREET2 = Column(String)
    BUS_CITY  = Column(String)
    BUS_STATE = Column(String)
    BUS_STATETXT = Column(String)
    BUS_ZIPCODE = Column(String)
    BUS_PHONE = Column(String)
    MAIL_STREET1 = Column(String)
    MAIL_STREET2 = Column(String)
    MAIL_CITY = Column(String)
    MAIL_STATE = Column(String)
    MAIL_STATETXT = Column(String)
    MAIL_ZIPCODE = Column(String)
    FCOMP_CONFORMEDNAME = Column(String)
    DATE_NAMECHANGE = Column(Date)
    DIRECTOR = Column(String)
    OFFICER = Column(String)
    TENPERCENTOWNER = Column(String)
    OTHER = Column(String)
    TEXT_OTHER = Column(String)
    SIGN_TITLE = Column(String)
    SIGN_NAME = Column(String)
    SIGN_DATE = Column(Date)

class ZSECFORM3_DTAB(Base):
    __tablename__ = 'ZSECFORM3_DTAB'
    __table_args__ = (PrimaryKeyConstraint('ACCESSIONNO', 'ACCESS_TRANXID'),)

    MANDT = Column(String)
    ACCESSIONNO = Column(String(20), ForeignKey('ZSECFORM3.ACCESSIONNO'))
    ACCESS_TRANXID = Column(Integer)
    DERIVSECURITY_TYPETITLE = Column(String)
    DATE_EXCISE = Column(String)
    DATE_EXPIRE = Column(String)
    SECURITY_TYPETITLE = Column(String)
    SHARE_AMOUNT = Column(String)
    EXPRICE_DERVSECURTY = Column(String)
    OWNERSHIPTYPE = Column(String)
    INDBENF_OWNER = Column(String)

class ZSECFORM3_NDTAB(Base):
    __tablename__ = 'ZSECFORM3_NDTAB'
    __table_args__ = (PrimaryKeyConstraint('ACCESSIONNO', 'ACCESS_TRANXID'),)

    MANDT = Column(String)
    ACCESSIONNO = Column(String(20), ForeignKey('ZSECFORM3.ACCESSIONNO'))
    ACCESS_TRANXID = Column(Integer)
    FORM_TYPE = Column(String)
    SECURITY_TYPETITLE = Column(String)
    SECTITLE_FTNOTE = Column(String)
    SHARES = Column(String)
    SHARE_FTNOTE = Column(String)
    SHARE_VALUE = Column(String)
    SHAREVLAUE_FTNOTE = Column(String)
    OWNERSHIPTYPE = Column(String)
    OWNSHIP_FTNOTE = Column(String)
    INDBENF_OWNER = Column(String)
    INDBENF_OWNER_FTNOTE = Column(String)

class ZSECFORM3_FTNOTE(Base):
    __tablename__ = 'ZSECFORM3_FTNOTE'
    __table_args__ = (PrimaryKeyConstraint('ACCESSIONNO', 'FOOTNOTE_ID'),)

    MANDT = Column(String)
    ACCESSIONNO = Column(String(20), ForeignKey('ZSECFORM3.ACCESSIONNO'))
    SEC_DOC = Column(String)
    FOOTNOTE_ID = Column(String(5))
    FOOTNOTE_TXT = Column(String)