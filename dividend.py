<<<<<<< HEAD
import requests
import pandas as pd
from bs4 import BeautifulSoup

# 初始化 headers 和 result
headers = ["代號", "股票名稱", "發放期間", "所屬期間", "現金股利", "股票股利", "現金殖利率", "除息日昨收價", "除息日", "除權日", "現金股利發放日", "股票股利發放日", "填息天數"]
result = []

# 迴圈日期下載資料
# 下載證交所資料
url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&type=ALLBUT0999'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 判斷是否有空資料存在 若存在則跳離此次迴圈
if 'none' not in soup.text:
    # 整理證交所每日收盤行情表
    table = soup.find_all('table')[8]
    columnNames = table.find('thead').find_all('tr')[2].find_all('td')
    columnNames = [elem.getText() for elem in columnNames]
    rowDatas = table.find('tbody').find_all('tr')

    for row in rowDatas:
        code = row.find_all("td")[0].text.strip()
        stock_name = row.find_all("td")[1].text.strip()

        detail_url = f"https://tw.stock.yahoo.com/quote/{code}/dividend"
        detail_response = requests.get(detail_url)
        if detail_response.status_code == 200:
            detail_soup = BeautifulSoup(detail_response.content.decode('utf-8'), "html.parser")
            no_data_msg = detail_soup.find('div', class_="W(100%) H(104px) D(f) Ai(c) Jc(c) Fz(16px) C($c-secondary-text) Fw(b)")
            if no_data_msg and "查無資料" in no_data_msg.text:
                print(f"No dividend data found for {code} - {stock_name}")
            else:
                detail_list_items = detail_soup.find('ul', class_="M(0) P(0) List(n)")
                if detail_list_items:
                    for li_item in detail_list_items.find_all('li'):
                        divs = li_item.find_all('div')
                        if len(divs) >= 7:
                            data = [div.text.strip() for div in divs[2:]]
                            result.append([code, stock_name] + data)
                            print([code, stock_name] + data)
                else:
                    print(f"No dividend data found for {code} - {stock_name}")

# 創建 DataFrame
df = pd.DataFrame(result, columns=headers)

# 儲存資料
if not df.empty:
    print(f"表格内容:")
    print(df)
    file_name = f"C:/stock/dividend/dividend.csv"
    df.to_csv(file_name, index=False)
else:
    print("Failed to retrieve data")

print("下載完成")
=======
import requests
import pandas as pd
from bs4 import BeautifulSoup

# 初始化 headers 和 result
headers = ["代號", "股票名稱", "發放期間", "所屬期間", "現金股利", "股票股利", "現金殖利率", "除息日昨收價", "除息日", "除權日", "現金股利發放日", "股票股利發放日", "填息天數"]
result = []

# 迴圈日期下載資料
# 下載證交所資料
url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX?response=html&type=ALLBUT0999'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# 判斷是否有空資料存在 若存在則跳離此次迴圈
if 'none' not in soup.text:
    # 整理證交所每日收盤行情表
    table = soup.find_all('table')[8]
    columnNames = table.find('thead').find_all('tr')[2].find_all('td')
    columnNames = [elem.getText() for elem in columnNames]
    rowDatas = table.find('tbody').find_all('tr')

    for row in rowDatas:
        code = row.find_all("td")[0].text.strip()
        stock_name = row.find_all("td")[1].text.strip()

        detail_url = f"https://tw.stock.yahoo.com/quote/{code}/dividend"
        detail_response = requests.get(detail_url)
        if detail_response.status_code == 200:
            detail_soup = BeautifulSoup(detail_response.content.decode('utf-8'), "html.parser")
            no_data_msg = detail_soup.find('div', class_="W(100%) H(104px) D(f) Ai(c) Jc(c) Fz(16px) C($c-secondary-text) Fw(b)")
            if no_data_msg and "查無資料" in no_data_msg.text:
                print(f"No dividend data found for {code} - {stock_name}")
            else:
                detail_list_items = detail_soup.find('ul', class_="M(0) P(0) List(n)")
                if detail_list_items:
                    for li_item in detail_list_items.find_all('li'):
                        divs = li_item.find_all('div')
                        if len(divs) >= 7:
                            data = [div.text.strip() for div in divs[2:]]
                            result.append([code, stock_name] + data)
                            print([code, stock_name] + data)
                else:
                    print(f"No dividend data found for {code} - {stock_name}")

# 創建 DataFrame
df = pd.DataFrame(result, columns=headers)

# 儲存資料
if not df.empty:
    print(f"表格内容:")
    print(df)
    file_name = f"C:/stock/dividend/dividend.csv"
    df.to_csv(file_name, index=False)
else:
    print("Failed to retrieve data")

print("下載完成")
>>>>>>> c27964713d91f11e5dc82abea39da1eee755db22
