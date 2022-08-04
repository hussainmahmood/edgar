# coding: utf-8
from sqlalchemy import Column, Date, DateTime, PrimaryKeyConstraint, BigInteger, Integer, Numeric, Boolean, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BasicInformation(Base):
    __tablename__ = 'basic_info'
    __table_args__ = ()

    cik = Column(String(12), primary_key=True)
    entityType = Column(String)
    sic = Column(String)
    sicDescription = Column(String)
    insiderTransactionForOwnerExists = Column(Boolean)
    insiderTransactionForIssuerExists = Column(Boolean)
    name = Column(String)
    tickers = Column(String)
    exchanges = Column(String)
    ein = Column(String)
    description = Column(String)
    website = Column(String)
    investorWebsite = Column(String)
    category = Column(String)
    fiscalYearEnd = Column(String)		
    stateOfIncorporation = Column(String)	
    stateOfIncorporationDescription = Column(String)
    phone = Column(String)
    flags = Column(String)	

class MailingAddress(Base):
    __tablename__ = 'mailing_address'
    __table_args__ = ()

    cik = Column(String(12), primary_key=True)
    street1 = Column(String)
    street2 = Column(String)
    city = Column(String)
    stateOrCountry = Column(String)	
    zipCode = Column(String)
    stateOrCountryDescription = Column(String)

class BusinessAddress(Base):
    __tablename__ = 'business_address'
    __table_args__ = ()

    cik = Column(String(12), primary_key=True)
    street1 = Column(String)
    street2 = Column(String)
    city = Column(String)
    stateOrCountry = Column(String)	
    zipCode = Column(String)
    stateOrCountryDescription = Column(String)

class FormerName(Base):
    __tablename__ = 'former_names'
    __table_args__ = ()

    former_name_id = Column(Integer, primary_key=True)
    cik = Column(String(12))
    name = Column(String)
    from_date = Column(Date)
    to_date = Column(Date)

class File(Base):
	__tablename__ = 'files'
	__table_args__ = ()

	file_id = Column(Integer, primary_key=True)
	cik = Column(String(12))
	name = Column(String)
	filingCount = Column(Integer)
	filingFrom = Column(Date)
	filingTo = Column(Date)	
    
class Filing(Base):
    __tablename__ = 'filings'
    __table_args__ = (PrimaryKeyConstraint('cik', 'accessionNumber'),)

    cik = Column(String(12))
    accessionNumber = Column(String(30))
    filingDate = Column(Date)
    reportDate = Column(Date)
    acceptanceDateTime = Column(DateTime)	
    act = Column(String)
    form = Column(String)
    fileNumber = Column(String)
    filmNumber = Column(String)
    items = Column(String)
    size = Column(Integer)
    isXBRL = Column(Boolean)
    isInlineXBRL = Column(Boolean)
    primaryDocument = Column(String)
    primaryDocDescription = Column(String)