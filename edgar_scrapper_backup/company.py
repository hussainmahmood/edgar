import re
from datetime import datetime
import pandas as pd
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import requests

class Company():
	def __init__(self, cik, drv):
		self.cik = cik
		self.drv = drv
		self.dir = f"companies/{self.cik}"
		self.errorReported = False

		try:
			self.ledger = pd.read_excel(f"{self.dir}/ledger.xlsx", header=0)
			if self.ledger.empty:
				self.create_ledger()
		except:
			self.create_ledger()
			

	def create_ledger(self):
		temp_ledger = []
		self.drv.get(f'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={self.cik}&owner=include&count=100')
		filename_regex = re.compile("-index.htm[l]{0,1}$")
		next_button = True
		while next_button:
			try:
				table_div = self.drv.find_element_by_id('seriesDiv')
				pret = bs(table_div.get_attribute('innerHTML'), features='lxml')
				for tr in pret.find_all("tr"):
					tds = tr.find_all("td")
					if tds:
						form_type = tds[0].get_text().strip()
						link = tds[1].find('a', id='documentsbutton').get('href').strip()
						link = re.sub(filename_regex, '.txt', link)
						filename = link.split('/')[-1]
						temp_ledger.append([form_type, link, filename, False, False, ""])
				try:
					self.drv.find_element_by_css_selector("input[value='Next 100']").click()
				except:
					next_button = False 
			except Exception as e:
				next_button = False
				with open(f"error_log.txt", "a") as error_log:  
					error_log.write(f"CIK: {self.cik} ({datetime.now()})\n")
					error_log.write(f"Error: {e}\n")
					error_log.close()

		self.ledger = pd.DataFrame(data=temp_ledger, columns=['FORM_TYPE', 'LINK', 'FILENAME', 'DOWNLOADED', 'UPLOADED', 'ERROR'])
		

	def download_forms(self, forms_required=[]):
		req = requests.session()
		req.keep_alive = False
		for i, entry  in self.ledger.iterrows():
			if not entry['DOWNLOADED'] and entry['FORM_TYPE'] in forms_required:
				try:
					r = req.get(f"https://www.sec.gov{entry['LINK']}", timeout=3)
				except Exception as e:
					self.ledger['ERROR'][i] = e
					self.errorFound = True
					with open(f"{self.dir}/error_log.txt", 'a') as comp_err_log:
						comp_err_log.write(f"Filename: {entry['FILENAME']} ({datetime.now()})\n")
						comp_err_log.write(f"Error: {e}\n")
						comp_err_log.close()
				else:
					with open(f"{self.dir}/{entry['FILENAME']}", 'wb') as f:
						soup = bs(r.text, "lxml")
						f.write(soup.encode("utf-8")) 
						f.close()
					self.ledger['DOWNLOADED'][i] = True
					self.ledger['ERROR'][i] = ""
	
	def upload_forms(self, conn, forms_required=[]):
		for i, entry  in self.ledger.iterrows():
			if entry['DOWNLOADED'] and entry['FORM_TYPE'] in forms_required and not entry['UPLOADED']:
				try:
					with open(f"{self.dir}/{entry['FILENAME']}", 'r') as file:
						form_name = re.sub('[^0-9a-zA-Z]', '', entry['FORM_TYPE']).lower()
						if form_name == '3a':
							form_name = '3'
						parser = getattr(__import__('parsers'), f"form_{form_name}")(file, conn)
						file.close()
					self.ledger['UPLOADED'][i] = True
					self.ledger['ERROR'][i] = ""
				except Exception as e:
					self.ledger['ERROR'][i] = e
					self.report_error()
					with open(f"{self.dir}/error_log.txt", 'a') as comp_err_log:
						comp_err_log.write(f"Filename: {entry['FILENAME']} ({datetime.now()})\n")
						comp_err_log.write(f"Error: {e}\n")
						comp_err_log.close()

	def report_error(self):
		if not self.errorReported:
			with open("error_log.txt", 'a') as err_log:
				err_log.write(f"Error at {self.cik} ({datetime.now()})\n")
				err_log.close()
			self.errorReported = True

	def save_ledger(self):
		self.ledger.to_excel(f"{self.dir}/ledger.xlsx", index=False)
