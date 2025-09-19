from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
import pandas as pd
from collections import Counter
import re

# Selenium으로 페이지 로드
driver = webdriver.Chrome()
url = 'https://www.yanolja.com/reviews/domestic/10041505'
driver.get(url)

# 페이지 로딩을 위해 대기
time.sleep(3)

# 스크롤 설정: 페이지 하단까지 스크롤을 내리기
scroll_count = 10

for _ in range(scroll_count):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

reviews_class = soup.find_all(class_="review-item-container")
reviews = []

for review in reviews_class:
    cleaned_text = review.get_text(strip=True).replace('\r', '').replace('\n', '')
    reviews.append(cleaned_text)

ratings = []

# 각 리뷰 컨테이너에서 별점 추출
for review_container in reviews_class:
    star_container = review_container.find(class_="css-rz7kwu")
    
    if star_container:
        # SVG 별들 찾기
        stars = star_container.find_all("svg")
        
        # 채워진 별과 빈 별 구분
        filled_stars = 0
        for star in stars:
            # path 태그의 fill-rule 속성으로 빈 별 구분
            path = star.find("path")
            if path and path.get("fill-rule") == "evenodd":
                # 빈 별 (fill-rule="evenodd"가 있는 경우)
                filled_stars += 0
            else:
                # 채워진 별
                filled_stars += 1
        
        ratings.append(filled_stars)
    else:
        # 별점을 찾을 수 없는 경우 0점 처리
        ratings.append(0)

# 별점과 리뷰 개수가 맞지 않을 경우 조정
min_length = min(len(ratings), len(reviews))
ratings = ratings[:min_length]
reviews = reviews[:min_length]

# 데이터 정리 및 DataFrame으로 변환
data = list(zip(ratings, reviews))
df_reviews = pd.DataFrame(data, columns=['Rating', 'Review'])

# 평균 별점 계산
if ratings:
    average_rating = sum(ratings) / len(ratings)
else:
    average_rating = 0

# 자주 등장하는 단어 추출
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

# 분석 결과 요약
summary_df = pd.DataFrame({
    'Average Rating': [average_rating],
    'Common Words': [', '.join([f"{word}({count})" for word, count in common_words])]
})

print(f"총 {len(reviews)}개의 리뷰가 수집되었습니다.")
print(f"평균 별점: {average_rating:.2f}")
print(f"자주 등장하는 단어 상위 10개:")
for word, count in common_words[:10]:
    print(f"  {word}: {count}번")

df_reviews.to_excel('yanolja_reviews.xlsx', index=False)
print("\n리뷰 데이터가 'yanolja_reviews.xlsx' 파일로 저장되었습니다.")

# 드라이버 종료
driver.quit()

