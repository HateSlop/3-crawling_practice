#!/usr/bin/env python
# coding: utf-8

# # 알라딘 도서 페이지 정적 크롤링
# 알라딘 도서 페이지에서 데이터를 추출하면서 정적 크롤링을 복습합니다.

# ### 1. 필요한 라이브러리 설치 및 임포트
# 먼저, 웹 크롤링을 위해 필요한 라이브러리들을 설치하고 임포트합니다.
# 
# - bs4: BeautifulSoup 라이브러리는 HTML/XML 페이지를 파싱하여 데이터를 쉽게 추출할 수 있게 도와줍니다.
# - requests: HTTP 요청을 보내 웹 페이지의 HTML을 받아오는 라이브러리입니다.
# - pandas: 데이터를 표 형태로 처리하고, csv 파일로 저장하는 데 사용됩니다.

# In[24]:


get_ipython().system('pip install bs4')
get_ipython().system('pip install requests')
get_ipython().system('pip install pandas')


# ### 2. HTML 페이지 불러오기 및 파싱
# 이제 웹 페이지를 불러와서 HTML을 파싱하여 필요한 데이터를 추출하는 작업을 시작합니다.
# 
# - requests.get(url): 지정한 URL에 HTTP GET 요청을 보냅니다.
# - BeautifulSoup(html, 'html.parser'): 응답 받은 HTML을 BeautifulSoup을 사용해 파싱합니다.

# In[25]:


from bs4 import BeautifulSoup
import requests
"""
TODO
1. requests 라이브러리로 url을 받아옵니다.
2. Beautifulsoup로 html 문서를 파싱합니다.
"""

# 알라딘 베스트셀러 페이지 URL
url = "https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0&page=1&cnt=1000&SortOrder=1"
response = requests.get(url) 
html = response.text # 응답 받은 HTML 문서
soup = BeautifulSoup(html, 'html.parser')# BeautifulSoup으로 파싱
soup


# ### 3. 특정 HTML 요소 선택
# 크롤링할 HTML 요소를 선택하기 위해 CSS 선택자를 사용하여 데이터를 추출합니다.
# 
# - soup.select_one(): CSS 선택자를 사용하여 첫 번째 일치하는 요소를 선택합니다.
# - tree: 선택된 HTML 요소(첫 번째 단락)에 대한 정보를 담고 있습니다.

# In[26]:


# 먼저 페이지 구조를 확인해보겠습니다
print("페이지에서 찾을 수 있는 클래스들:")
for element in soup.find_all(class_=True)[:10]:  # 처음 10개 요소만 확인
    print(f"클래스: {element.get('class')}, 태그: {element.name}")

# 다른 선택자들을 시도해보겠습니다
tree = soup.select_one('.ss_book_box')
if tree is None:
    tree = soup.select_one('.ss_book_list')
if tree is None:
    tree = soup.select_one('li')

print(f"\n선택된 tree: {tree}")
tree


# 

# ### 4. 정보 추출: 제목, 링크, 할인가, 별점
# 선택한 HTML 요소에서 원하는 데이터를 추출합니다.  
# - title_tag.text: title_tag 요소에서 텍스트(제목)를 추출합니다.
# - title_tag.attrs['href']: title_tag 요소에서 링크를 추출합니다.
# - price_tag.text, review_tag.text : 각각 할인가, 별점을 추출합니다.

# In[27]:


# 제목과 링크 추출
title_tag = tree.select_one(".bo3")
title_tag.text, title_tag.attrs['href']


# In[29]:


# 할인가와 별점 추출
price_tag = tree.select_one('.ss_p2')
review_tag = tree.select_one('.star_score')
price_tag.text, review_tag.text


# ### 5. 한 페이지에서 모든 도서 정보 추출
# 한 페이지에 여러 도서가 있을 때, 모든 도서의 정보를 추출합니다.
# 
# - soup.select(): 여러 개의 요소를 선택하여 리스트로 반환합니다.
# - 각 질문에 대해 for 루프를 돌며 제목, 링크, 할인가, 별점을 추출합니다.

# In[42]:


"""
TODO
위 코드를 기반으로 빈칸을 채워 완성하세요.

참조 : try-except문을 통해 원하는 정보가 없는 도서의 경우를 넘어가도록 합니다.
웹사이트의 정보는 늘 균일하지 않기에 크롤링에서 예외처리는 중요합니다.
"""

trees = soup.select(".ss_book_box")
for tree in trees:
    try:
        title = tree.select_one(".bo3")
        title_text = title.text
        title_link = title.attrs['href']
        price = tree.select_one('.ss_p2').text
        review = tree.select_one('.star_score').text
        print(title_text, title_link, price, review)
    except: continue



# ### 6. 여러 페이지 크롤링
# 페이지를 변경하면서 여러 페이지의 데이터 크롤링을 해봅시다.
# 
# - for page_num in range(1, 4): 1페이지부터 3페이지까지 순차적으로 크롤링합니다.
# - 각 페이지에서 데이터를 추출하여 datas 리스트에 추가하고, 이를 pandas DataFrame으로 변환하여 csv 파일로 저장합니다.

# In[31]:


import pandas as pd


# In[45]:


"""
TODO
1. for loop을 통해 여러 페이지로 이동합니다.
HINT : formatted string을 활용합니다.
2. 내부 for loop에서 위 코드에서 실행했던 한 페이지에서 도서 정보 모으기를 실행합니다.
3. DataFrame에 정보를 저장합니다.
"""

datas = []
for page_num in range(1, 4):
    url = f"https://www.aladin.co.kr/shop/common/wbest.aspx?BestType=Bestseller&BranchType=1&CID=0&page={page_num}"
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    trees = soup.select(".ss_book_box")
    for tree in trees:
        try:
            title = tree.select_one(".bo3")
            title_text = title.text
            title_link = title.attrs['href']
            price = tree.select_one('.ss_p2').text
            review = tree.select_one('.star_score').text
            datas.append([title_text, title_link, price, review])
        except: continue

df = pd.DataFrame(datas, columns=['title_text', 'title_link', 'price', 'review'])
df


# ### 7. 결과 저장
# 위의 크롤링한 데이터를 csv 파일로 저장합니다.
# 
# - df.to_csv(): 추출한 데이터를 csv 파일로 저장합니다. index=False를 설정하여 인덱스를 제외하고 저장합니다.

# In[46]:


# csv 파일로 저장해 봅시다.
df.to_csv('aladin_bestseller.csv', index=False)

