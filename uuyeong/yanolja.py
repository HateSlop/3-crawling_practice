#!/usr/bin/env python
# coding: utf-8

# # Yanolja 리뷰 크롤링 및 분석
# 
# 이번 노트북에서는 Selenium을 사용하여 Yanolja의 호텔 리뷰 페이지에서 데이터를 크롤링하고, 수집한 데이터에 대해 분석을 진행합니다. 이 과정에서는 웹페이지 로드, 데이터 추출, 텍스트 처리 및 분석 결과를 Excel 파일로 저장하는 작업을 포함합니다.

# ### 1단계: Selenium으로 웹페이지 로드
# 
# Selenium을 사용하여 Yanolja 리뷰 페이지를 로드하고, 스크롤을 내려서 더 많은 데이터를 가져옵니다.

# In[2]:


get_ipython().system('pip install selenium')
get_ipython().system('pip install bs4')
get_ipython().system('pip install pandas')
get_ipython().system('pip install openpyxl')


# In[9]:


from selenium import webdriver
import time

# Selenium 드라이버 설정 (Chrome 사용)
driver = webdriver.Chrome()

# Yanolja 리뷰 페이지로 이동
url = 'https://www.yanolja.com/reviews/domestic/10041505'
######## your code here ########
driver.get(url)
# 페이지 로딩을 위해 대기
time.sleep(3)

# 스크롤 설정: 페이지 하단까지 스크롤을 내리기
scroll_count = 10  # 스크롤 횟수 설정
for _ in range(scroll_count):
    ######## your code here ########
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)  # 스크롤 이후 대기


# ### 2단계: 페이지 소스 가져오기
# 웹페이지의 HTML 소스를 가져와서 BeautifulSoup을 사용해 데이터를 파싱합니다.

# In[10]:


from bs4 import BeautifulSoup

# 웹페이지 소스 가져오기
page_source = driver.page_source

# BeautifulSoup를 사용하여 HTML 파싱
soup = BeautifulSoup(page_source, 'html.parser')


# ### 3단계: 리뷰 텍스트 추출
# 리뷰 텍스트를 추출하고 불필요한 공백이나 줄 바꿈을 제거합니다.

# In[11]:


# 리뷰 텍스트 추출
################################
reviews_class = soup.select('.content-text')
################################
reviews = []

# 각 리뷰 텍스트 정리 후 추가
for review in reviews_class:
    cleaned_text = review.get_text(strip=True).replace('\r', '').replace('\n', '')
    reviews.append(cleaned_text)

reviews


# ### 4단계: 별점 데이터 추출
# HTML에서 별점 데이터를 추출하고, 각 리뷰의 별점을 계산합니다.

# In[13]:


# 별점 추출
ratings = []
################################
rating_containers = soup.select('.css-1mdp7n')
################################

# 각 리뷰별로 별점 계산
for container in rating_containers:
    ################################
    ######## your code here ########
    stars = container.select('.css-1mj121y')
    rating = len(stars)
    ################################

    ratings.append(rating)

ratings


# ### 5단계: 데이터 정리 및 DataFrame으로 변환
# 수집된 데이터를 Pandas DataFrame으로 변환하여 후속 분석을 용이하게 만듭니다.

# In[14]:


import pandas as pd

# 별점과 리뷰를 결합하여 리스트 생성
data = list(zip(ratings, reviews))

# DataFrame으로 변환
df_reviews = pd.DataFrame(data, columns=['Rating', 'Review'])
df_reviews


# ### 6단계: 리뷰 분석 - 평균 별점 계산
# 수집된 리뷰에서 평균 별점을 계산합니다.

# In[ ]:


# 평균 별점 계산
average_rating = round(sum(ratings) / len(ratings), 2)


# ### 7단계: 자주 등장하는 단어 추출
# 리뷰 텍스트에서 자주 등장하는 단어를 추출하고, 불용어를 제거하여 분석합니다.

# In[19]:


from collections import Counter
import re

# 불용어 리스트 (한국어)
korean_stopwords = set(['이', '그', '저', '것', '들', '다', '을', '를', '에', '의', '가', '이', '는', '해', '한', '하', '하고', '에서', '에게', '과', '와', '너무', '잘', '또','좀', '호텔', '아주', '진짜', '정말'])

# 모든 리뷰를 하나의 문자열로 결합
all_reviews_text = ' '.join(reviews)

# 단어 추출 (특수문자 제거)
words = re.findall(r'[가-힣]+', all_reviews_text)

# 불용어 제거
filtered_words = [word for word in words if word not in korean_stopwords and len(word) > 1]

# 단어 빈도 계산
word_counts = Counter(filtered_words)

# 자주 등장하는 상위 15개 단어 추출
common_words = word_counts.most_common(15)


# ### 8단계: 분석 결과 요약
# 평균 별점과 자주 등장하는 단어를 DataFrame으로 만들어 최종 분석 결과를 요약합니다.

# In[20]:


# 분석 결과 요약
summary_df = pd.DataFrame({
    'Average Rating': [average_rating],
    'Common Words': [', '.join([f"{word}({count})" for word, count in common_words])]
})

# 최종 DataFrame 결합
final_df = pd.concat([df_reviews, summary_df], ignore_index=True)
final_df


# ### 9단계: Excel 파일로 저장
# 최종 결과를 Excel 파일로 저장합니다.

# In[21]:


# Excel 파일로 저장
final_df.to_excel('yanolja_reviews_analysis.xlsx', index=False)


# ### 10단계: 드라이버 종료
# 크롤링이 끝난 후, Selenium 드라이버를 종료합니다.

# In[22]:


# 드라이버 종료
driver.quit()

