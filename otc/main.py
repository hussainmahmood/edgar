import os
import time
from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs
import pandas as pd

def main():
    opt = wd.ChromeOptions()
    opt.add_argument('--no-sandbox')
    # opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument('--remote-debugging-port=9222')
    opt.add_argument('--incognito')
    opt.add_argument('--ignore-certificate-errors')
    drv = wd.Chrome('../chromedriver_win32/chromedriver' , options=opt)
    drv.get(f'https://www.otcmarkets.com/research/stock-screener')
    time.sleep(2)
    country = drv.find_element_by_id('country')
    country.find_element_by_id('dropdownMenu1').click()
    country.find_element_by_css_selector('label[for=input_19]').click()
    time.sleep(2)
    head = []
    data = []
    table = bs(drv.find_element_by_id('main-table').get_attribute('innerHTML'), 'html.parser')
    for th in table.find_all('th'):
        head.append(th.get_text().strip().upper())

    paginator = bs(drv.find_element_by_id('pagination').get_attribute('innerHTML'), 'html.parser')
    lis = paginator.find_all('li')
    numOfPages = int(lis[len(lis)-3].get_text()) + 1
    for i in range(1, numOfPages):
        isHeader = True
        drv.find_element_by_link_text(str(i)).click()
        time.sleep(2)
        table = bs(drv.find_element_by_id('main-table').get_attribute('innerHTML'), 'html.parser')
        for tr in table.find_all('tr'):
            if isHeader:
                isHeader = False
            else:
                temp_arr = []
                for td in tr.find_all('td'):
                    temp_arr.append(td.get_text().strip())
                data.append(temp_arr)
        

    df = pd.DataFrame(data=data, columns=head)
    df.to_excel(f'otc.xlsx', index=False)


    drv.quit()

if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f'--- {time.time() - start_time} seconds ---')
