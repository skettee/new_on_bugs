#%% [markdown]
# ## 벅스 최신음악 🤖
#
# 벅스의 최신 음악을 모아주는 봇입니다.
# 
# - 개발자: skettee
#
# - 깃허브 주소: [new_on_bugs](https://github.com/skettee/new_on_bugs)
# 
#
# ### 개발 환경 만들기
# 
# 봇을 개발하기 위해서는 몇가지 소프트웨어를 설치하고 환경을 설정해야 합니다. 
# [개발 환경 만들기](https://github.com/moabogey/docs/wiki/개발환경만들기)를 참조 하세요.
# 
# ### 코드 실행
# 
# - 터미널 실행
#
#   - 🖼  Windows PowerShell을 실행한다.
#
#   - 🍎 Terminal을 실행한다.
#
# - 작업할 폴더를 생성한다.
# 
# ```
# mkdir MyWork
# ```
# 
# - 작업할 폴더로 이동한다.
#  
# ```
# cd MyWork
# ```
# 
# - 깃 클론 (Git Clone)을 수행한다.
# 
# ```
# git clone https://github.com/skettee/new_on_bugs.git
# ```
# 
# - 복사한 코드의 폴더로 이동한다.
# 
# ```
# cd new_on_bugs
# ```
# 
# - VSCode를 실행한다.
# 
# ```
# code .
# ```
# 
# - 왼쪽 EXPLORE에서 `new_on_bugs.py`를 선택한다.
# 
# - 하단 바에 `Python3.7.3 64-bit('base':conda)`를 누른다.
# 
# - `Python 3.6.8 64-bit ('moabogey':conda)`를 선택한다.
# 
# - 소스 코드에 `RunCell | Run Below`에서 `Run Below`를 누른다.
# 
# - 데이터가 정상적으로 수집이 되는지 오른쪽 Python Interactive에서 확인한다. 
#    
#
# ### 코드 분석
# 
# new_on_bugs.py를 분석합니다.  
# 봇의 소스 코드는 크게 세단계로 나눌 수 있습니다.  
# 
# 1. 사이트의 HTML에서 데이터를 수집
# 
# 2. 포스트의 HTML에서 데이터를 수집
# 
# 3. 데이터 저장
# 
#  
# **사이트의 HTML에서 데이터를 수집**
#  
# - 데이터를 수집할 사이트의 정보와 주소를 설정합니다. 여기에서는 https://music.bugs.co.kr/newest 에서 데이터를 수집합니다.
# 
# - requests와 beautifulsoup4를 이용해서 사이트의 HTML을 가져오고 파일로 저장합니다.
# 
# - 저장된 HTML파일 (bugs_source.html)을 열어 봅니다. 여기서 우리는 "포스트의 리스트"를 표현하는 구간을 찾을 것입니다. **포스트**는 제목, 내용, 이미지, 작성자, 작성 날짜 및 페이지 위치(URL)를 가지고 있는 하나의 문서를 나타내는 용어로 사용합니다.
# 
# ```
# +-------------- +-> <ul class="... albumList">
# +
# +-------------+ +->   <figure albumid=...>
# |   Post 1    
# |  (Item 1)
# +-------------+ +->   </figure>
# 
# +-------------+ +->   <figure albumid=...>
# |   Post 2    
# |  (Item 2)
# +-------------+ +->   </figure>
# 
# +-------------+ +->  <figure albumid=...>
# |   Post3     
# |  (Item 3)
# +-------------+ +->   </figure>
# ```
#  
# - 각각의 포스트는 `<figure albumid=...>` 에서 시작 되고 `</figure>`로 끝난다는 것을 알아내는 것이 중요합니다. 이것은 사이트마다 다르기 때문에 이것을 찾아내는 것은 약간의 경험이 필요합니다.
# 
# - 발견한 포스트에서 아래와 같이 제목, 작성자, 올린 시간 및 포스트 위치(URL)를 찾습니다.
# 
# ```
# +-------------+
# |   Post 1    
# +-------------+
# |  title      +->  <a class="albumTitle"... title=...>
# |             
# |  post URL   +->  <a class="albumTitle"... href=...>
# |             
# |  createdBy  +->  <a class="artistTitle"... title=...>
# |             
# |  createdAt  +-> <time datetime=...>
# +-------------+
# ```
#  
# - 나머지 데이터를 수집하기 위해서 포스트 HTML로 이동합니다.
#  
#
# **포스트의 HTML에서 데이터를 수집**
# 
# - 데이터를 수집할 포스트의 주소를 설정합니다.
# 
# - requests와 beautifulsoup4를 이용해서 사이트의 HTML을 가져오고 파일로 저장합니다.
# 
# - 저장된 HTML파일 (bugs_post_source.html)을 열어 봅니다. 여기서 우리는 포스트의 이미지를 수집할 것입니다.
#  
#
# **Open Graph Protocol**
# 
# - 대부분의 사이트들은 우리가 수집할 데이터를 사이트의 첫머리에 미리 모아 놓고 있습니다. 이 규약(Protocol)은 사이트를 모두 분석하지 않고도 사이트의 내용을 파악하는데 도움이 됩니다.
# 
# - 아래와 같은 메타 태그를 사용합니다.
# 
# ```html
# <head>
# ...
#     <meta content="..." property="og:url"/>
#     <meta content="..." property="og:title"/>
#     <meta content="..." property="og:image"/>
#     <meta content="..." property="og:description"/>
#     <meta content="..." property="og:site_name"/>
# ...
# </head>
# ```
# 
# - 메타 태그에서 데이터를 수집합니다.
# 
# - 메타 태그의 정보가 부족한 경우에는 본문에서 직접 데이터를 수집합니다.
#  
#
# **데이터 저장**
# 
# - 수집한 데이터를 선별해서 중복되는 것을 제외하고 데이터베이스에 저장합니다. 모아보기 봇은 하루에 24번 이상 동작 하도록 되어 있기 때문에 한번에 모든 데이터를 수집하지 않고 가장 최근의 데이터 1~2개를 수집하는 것이 원칙입니다.
#  
#
# ### 참고 사이트
#  
# - [개발 환경 만들기](https://github.com/moabogey/docs/wiki/개발환경만들기)
#
# - [예제 코드 실행](https://github.com/moabogey/docs/wiki/예제코드실행)
#
# - [코딩을 하기 전에](https://github.com/moabogey/docs/wiki/코딩하기전에)
#
# - [예제 코드 분석](https://github.com/moabogey/docs/wiki/예제코드분석)
#
# - [봇 개발 하기](https://github.com/moabogey/docs/wiki/봇개발하기)
# 
#
# ### ⬇️소스코드

#%%
import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
from datetime import timedelta

if __debug__:
    import os.path

# 모아보기 컴포넌트를 가져온다.
import moabogey_database as moabogey
from moabogey_id import *

# 사이트 이름
site_name = 'bugs'
# 사이트에서 가져올 주제
subject_name = 'newest'
# 사이트 주소
site_url = 'https://music.bugs.co.kr/newest'
if __debug__:
    print('{} 데이터 수집 중...'.format(site_url))

# 사이트의 HTML을 가져온다.
try:
    response = requests.get(site_url)
    # 에러가 발생 했을 경우 에러 내용을 출력하고 종료한다.
    response.raise_for_status()
except HTTPError as http_err:
    print(f'HTTP error occurred: {http_err}')
except Exception as err:
        print(f'Other error occurred: {err}')
else:
    html_source = response.text
    #print(response.status_code)
    #print(html_source)
    
    # BeautifulSoup 오브젝트를 생성한다.
    soup = BeautifulSoup(html_source, 'html.parser')
    
    # HTML을 분석하기 위해서 페이지의 소스를 파일로 저장한다.
    if __debug__:
        file_name = site_name + '_source.html'
        if not os.path.isfile(file_name):
            print('file save: ', file_name)
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(soup.prettify())
       
    # 데이터를 저장할 데이터베이스를 생성한다. 
    # bot_id는 moabogey_id에서 가져온 값이다.
    db_name = subject_name + '_on_' + site_name 
    my_db = moabogey.Dbase(db_name, bot_id)
            
    # 사이트 이름을 수집한다.
    moa_site_name = soup.find('meta', property="og:site_name")
    if moa_site_name:
        moa_site_name = moa_site_name['content']
    
    # 앨범 목록을 찾는다.
    albumList = soup.find('ul', class_='albumList')
    #print(albumList)

    # 반복해서 리스트의 목록을 하나씩 검색하고 데이터를 수집한다.
    for post in albumList.find_all('figure', albumid=True):
        #moa_image = post.find('img', src=True)
        #if moa_image:
        #    moa_image = moa_image['src']
        #print('image: ', moa_image)

        moa_title = post.find('a', class_='albumTitle')['title']
        #print('title: ', moa_title)

        moa_url = post.find('a', class_='albumTitle')['href']
        #print('url: ', moa_url)

        moa_createdBy = post.find('a', class_='artistTitle')['title']
        moa_createdAt = post.find('time', datetime=True).text.strip()
        # String to DateTime format으로 변환한다.
        # "2019.03.21"
        moa_createdAt = datetime.strptime(moa_createdAt, '%Y.%m.%d') 
        # UTC 값으로 변경하기 위해서 9시간을 뺀다. 
        moa_createdAt = moa_createdAt - timedelta(hours=9)
        #print('moa_createdAt', moa_createdAt)
        
        # 현재 날짜와 시간을 수집한다.
        moa_timeStamp = datetime.now()

        # 포스트의 주소로 이동한다.
        try:
            response =  requests.get(moa_url)
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
                print(f'Other error occurred: {err}')
        else:
            subhtml_source = response.text
            
            # BeautifulSoup 오브젝트를 생성한다.
            post = BeautifulSoup(subhtml_source, 'html.parser')

            # HTML을 분석하기 위해서 포스트의 소스를 파일로 저장한다.
            if __debug__:
                file_name = site_name + '_post_source.html'
                if not os.path.isfile(file_name):
                    print('file save: ', file_name)
                    with open(file_name, 'w', encoding='utf-8') as f:
                        f.write(post.prettify())
            
            # 포스트의 대표 이미지(앨범 표지)의 주소를 수집한다.
            moa_image = post.find('meta', property="og:image")
            if moa_image:
                moa_image = moa_image['content']
            #print('image: ', moa_image)
        
            # 데이터베이스에 있는 포스트와 중복되는지를 확인하고 
            # JSON형식으로 수집한 데이터를 변환한다.
            if my_db.isNewItem('title', moa_title):
                # 데이터 타입을 확인한다.
                assert type(moa_title) == str, 'title: type error'
                assert type(moa_url) == str, 'url: type error'
                assert type(moa_image) == str, 'image: type error'
                assert type(moa_site_name) == str, 'siteName: type error'
                assert type(moa_createdBy) == str, 'createBy: type error'
                assert type(moa_createdAt) == datetime, 'createdAt: type error'
                assert type(moa_timeStamp) == datetime, 'timeStamp: type error'

                db_data = { 'title': moa_title, 
                    'url': moa_url,
                    'image': moa_image,
                    'siteName': moa_site_name,
                    'createdBy': moa_createdBy,
                    'createdAt': moa_createdAt,
                    'timeStamp': moa_timeStamp
                }

                if __debug__:
                    # 디버그를 위해서 수집한 데이터를 출력한다.
                    temp_data = db_data.copy()
                    #temp_data['desc'] = temp_data['desc'][:20] + '...'
                    print('collected json data: ')
                    print(json.dumps(temp_data, indent=4, ensure_ascii=False, default=str))

                # 수집한 데이터를 데이터베이스에 전송한다.
                my_db.insertTable(db_data)

                # 수집이 완료되면 프로그램을 종료한다.
                break
                
    # 데이터 베이스에 저장된 데이터를 디스플레이 한다.
    if __debug__:
        my_db.displayHTML()
        
    # 데이터 베이스를 닫는다.
    my_db.close()
