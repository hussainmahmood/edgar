import os
import time
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import pandas as pd


def main():
    opt = wd.ChromeOptions()
    opt.add_argument('--no-sandbox')
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--remote-debugging-port=9222')
    opt.add_argument('--incognito')
    opt.add_argument('--ignore-certificate-errors')
    drv = wd.Chrome('../chromedriver_win32/chromedriver' , options=opt)
    symbols = pd.read_excel('pak_stock_symbol.xlsx', header=0, squeeze=True)
    for symbol in symbols:
        name = []
        designation = []
        if not os.path.exists(f"data/{symbol}"):
            os.makedirs(f"data/{symbol}")

        drv.get(f'http://www.scstrade.com/stockscreening/SS_CompanySnapShotCP.aspx?symbol={symbol}')
        time.sleep(2)
        body = drv.find_element_by_tag_name('body')
        
        pret = bs(body.get_attribute('innerHTML'), features='lxml')

        try:
            table = pret.find("table", class_="ui-jqgrid-btable")
            for tr in table.find_all("tr", class_="ui-row-ltr"):
                td = tr.find_all("td")
                name.append(td[0].get_text().strip())
                designation.append(td[1].get_text().strip())

            df = pd.DataFrame({'Executive Name':name, 'Designation':designation})
            df.to_csv(f'data/{symbol}/profile.txt', sep="|", index=False)
        except:
            pass


    drv.quit()

if __name__ == "__main__":
    start_time = time.time()
    main()
    print(f"--- {time.time() - start_time} seconds ---")