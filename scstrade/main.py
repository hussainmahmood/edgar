import os
import re
import time
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import pandas as pd


def main():
    opt = wd.ChromeOptions()
    opt.add_argument('--no-sandbox')
    #opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--remote-debugging-port=9222')
    opt.add_argument('--incognito')
    opt.add_argument('--ignore-certificate-errors')
    drv = wd.Chrome('../chromedriver_win32/chromedriver' , options=opt)
    table_types = ['Earnings', 'Important Ratios', 'Equity Ratios', 'Dividends', 'Sales', 
                   'Enterprise Value (EV)', 'Cash', 'Profitablility', 'Liquidity', 'Solvency', 
                   'Advances & Deposits']
    symbols = pd.read_excel('pak_stock_symbol.xlsx', header=0, squeeze=True)
    for symbol in symbols:
        if not os.path.exists(f"data/{symbol}"):
            os.makedirs(f"data/{symbol}")

        drv.get(f'http://www.scstrade.com/stockscreening/SS_CompanySnapShot.aspx?symbol={symbol}')
        body = drv.find_element_by_tag_name('body')
        
        pret = bs(body.get_attribute('innerHTML'), features='lxml')
        for table_type in table_types:
            headings = []
            values = []
            try:
                table = pret.find("div", text=re.compile(f'\s*{table_type}\s*')).parent
                table_headings = table.find_all("div", class_="mainheading")
                table_values = table.find_all("div", class_="mainheadingvalue")
                for heading in table_headings:
                    headings.append(heading.get_text())
                for value in table_values:
                    values.append(value.get_text())
                df = pd.DataFrame({'HEADING':headings, 'VALUE':values})
                df.to_excel(f'data/{symbol}/{table_type}.xlsx', index=False)
            except:
                pass


    drv.quit()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")
