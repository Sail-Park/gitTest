# 위의 코드는 네이버 블로그 검색 API를 사용하여 "패밀리 레스토랑 할인"과 관련된 게시물을 검색하고, 
# 결과를 CSV 파일로 저장하는 파이썬 스크립트입니다. 주석을 통해 각 코드 라인의 기능을 설명하였습니다.


# 네이버 검색 API 예제 - 블로그 검색
import os
import sys
import urllib.request
import json
import pandas as pd
from tabulate import tabulate

# API 클라이언트 ID와 클라이언트 비밀번호 설정
client_id = "Yx6iW9L2lVCb80V3qoEX"
client_secret = "Jw57noJFYq"

# 검색어를 URL 인코딩
encText = urllib.parse.quote("패밀리 레스토랑 할인")

# 검색 결과 개수 설정 및 정렬 방식 설정 (날짜순)
display = '&display=15'
sort = '&sort=date'

# 검색 쿼리를 포함하는 요청 URL 생성 (JSON 결과 사용)
url = "https://openapi.naver.com/v1/search/blog?query=" + encText + display + sort

# 요청 객체 생성 및 헤더 설정
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)

# 요청 전송 및 응답 수신
response = urllib.request.urlopen(request)
rescode = response.getcode()

# 응답 코드가 200인 경우 (성공적으로 처리됨)
if(rescode==200):
    response_body = response.read()

    # 응답 본문을 JSON 형식으로 읽어들이고, 파이썬 딕셔너리로 변환
    result = json.loads(response_body)

    # 변환된 딕셔너리에서 'items' 키에 해당하는 부분만 데이터프레임으로 변환
    df = pd.DataFrame(result['items'])

    # 불필요한 컬럼 "bloggername"과 "bloggerlink"를 제거
    df = df.drop(["bloggername", "bloggerlink"], axis=1)

    # 데이터프레임을 CSV 파일로 저장 (한글 깨짐 방지를 위해 인코딩 명시)
    df.to_csv("blog_data.csv", index=False, encoding="utf-8-sig")
else:
    # 응답 코드가 200이 아닌 경우 오류 코드 출력
    print("Error Code:" + rescode)
