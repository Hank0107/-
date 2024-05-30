import requests
import pandas as pd
from bs4 import BeautifulSoup

# 建立空的 DataFrame 用於存儲所有 ETF 的資料
all_etf_data = pd.DataFrame()

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
        code = row.find("td").text.strip()

        detail_url = f"https://tw.stock.yahoo.com/quote/{code}/holding"
        detail_response = requests.get(detail_url)
        if detail_response.status_code == 200:
            detail_soup = BeautifulSoup(detail_response.content.decode('utf-8'), "html.parser")
            detail_list_items = detail_soup.find_all('ul', class_="Bxz(bb) Bgc($c-light-gray) Bdrs(8px) P(20px)")

            # 確保有兩個表格存在，並且僅選擇第二個表格
            if len(detail_list_items) >= 2:
                detail_list_item = detail_list_items[1]

                headers = ["股票名稱", "持股(%)"]
                result = []

                list_items = detail_list_item.find_all('li', class_="D(f) Ai(c) Jc(sb) C($c-link-text) Fz(16px) Lh(24px) Pt(8px) Pb(7px) Bdbs(s) Bdbw(1px) Bdbc($bd-primary-divider)")

                for li_item in list_items:
                    # 檢查每個 <li> 元素是否包含股票名稱和持股百分比
                    divs = li_item.find_all('div', recursive=False)
                    if len(divs) >= 2:
                        stock_name = divs[0].text.strip()
                        holding_percentage = divs[1].text.strip()
                        result.append([stock_name, holding_percentage])

                df = pd.DataFrame(result, columns=headers)
                print(f"代號 {code} 的表格内容:")
                print(df)
                file_name = f"C:/stock/stockhold/{code}.csv"
                df.to_csv(file_name, index=False)
else:
    print("Failed to retrieve data")

print("下載完成")
