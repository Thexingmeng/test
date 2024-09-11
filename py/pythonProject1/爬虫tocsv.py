import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import time
import re  # Ensure you import re for regular expressions

# 创建 data 文件夹（如果它不存在）
if not os.path.exists('data'):
    os.makedirs('data')

# 豆瓣电影的 URL
base_url = 'https://movie.douban.com/top250'

# 设置 User-Agent，模拟真实浏览器请求
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 用于存储数据的列表
data = []

# 抓取数据
for page in range(0, 10):  # 10 页，每页包含 25 部电影
    url = f'{base_url}?start={page * 25}&filter='
    response = requests.get(url, headers=headers)

    # 检查响应状态
    if response.status_code == 200:
        print(f"Successfully fetched page {page + 1}")
    else:
        print(f"Failed to retrieve page {page + 1}: Status code {response.status_code}")
        continue

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取电影数据
    for item in soup.find_all('div', class_='item'):
        title = item.find('span', class_='title').get_text(strip=True)
        rating = item.find('span', class_='rating_num').get_text(strip=True)
        info_div = item.find('div', class_='bd')
        info_paragraphs = info_div.find_all('p') if info_div else []

        # 确保有足够的 <p> 元素
        if len(info_paragraphs) > 1:
            info = info_paragraphs[1].get_text(strip=True)
        else:
            info = 'No info available'

        # 提取上映时间
        release_date = re.search(r'\d{4}', info)
        release_date = release_date.group(0) if release_date else 'No release date'

        data.append({
            'Title': title,
            'Rating': rating,
            'Release Date': release_date,
            'Timestamp': datetime.now().isoformat()
        })

    # 防止过于频繁地请求同一网页，添加延迟
    time.sleep(1)

# 创建 DataFrame
df = pd.DataFrame(data)

# 打印抓取的前几条数据
print(df.head())

# 保存为 CSV 文件到 'data' 文件夹下
csv_file_path = os.path.join('data', 'douban_movies.csv')
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

# 输出总共抓取的行数
print(f"CSV file saved to: {csv_file_path}")
print(f"Total number of rows scraped: {len(df)}")
