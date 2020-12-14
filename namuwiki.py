import requests
from bs4 import BeautifulSoup
import re
import pandas as pd 

url = "https://namu.wiki/RecentChanges"

class NamuWiki:
    
    # 나무위키 최근 문서에서 a 태그 url들을 수집합니다. 
    def GetAurl(self, url):
        req = requests.get(url)
        html = req.content
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find(name='table') #이름이 table인 태그의 내용들을 가져옵니다.
        table_body = table.find(name='tbody') #이름이 table인 태그의 내용들 중 하위 태그가 tbody인 내용을 가져옵니다.
        table_body_tr = table_body.find_all(name='tr') #table>tbdoy>tr인 태그들을 모두 가져옵니다.  

        #a 태그의 href 속성을 리스트로 추출해, 크롤링 할 페이지 리스트 생성 
        page_url_base = "https://namu.wiki"
        page_urls = []
        for index in range(0, len(table_body_tr)):
            first_td = table_body_tr[index].find_all('td')[0]
            td_url = first_td.find_all('a')
            if len(td_url) > 0:
                page_url = page_url_base + td_url[0].get('href')
                if 'png' not in page_url: #이미지로 연결되는 링크는 제외합니다.
                    page_urls.append(page_url)

        # 중복 url을 제거합니다.
        page_urls = list(set(page_urls))
        return(page_urls)

    #수집한 a 태그 문서 각각에서 title, 카테고리, contents를 수집한뒤 데이터프레임으로 만듭니다. 
    def MakeDf(self, page_urls):
        columns = ['title', 'category', 'content']
        df = pd.DataFrame(columns=columns)

        for page_url in page_urls[:3]:
            req = requests.get(page_url)
            html = req.content
            soup = BeautifulSoup(html, 'lxml')
            contents_table = soup.find(name="article")
            title = contents_table.find_all('h1')[0]

            # 카테고리 정보가 없는 경우를 확인합니다.
            if len(contents_table.find_all('ul')) > 0:
                category = contents_table.find_all('ul')[0]
            else:
                category = None

            content_paragraphs = contents_table.find_all(name="div", attrs={"class":"wiki-paragraph"})
            content_corpus_list = []

            # 페이지 내 제목 정보에서 개행 문자를 제거한 뒤 추출합니다. 만약 없는 경우, 빈 문자열로 대체합니다.
            if title is not None:
                row_title = title.text.replace("\n", " ")
            else:
                row_title = ""

            # 페이지 내 본문 정보에서 개행 문자를 제거한 뒤 추출합니다. 만약 없는 경우, 빈 문자열로 대체합니다.
            if content_paragraphs is not None:
                for paragraphs in content_paragraphs:
                    if paragraphs is not None:
                        content_corpus_list.append(paragraphs.text.replace("\n", " "))
                    else:
                        content_corpus_list.append("")
            else:
                content_corpus_list.append("")

            # 페이지 내 카테고리정보에서 “분류”라는 단어와 개행 문자를 제거한 뒤 추출합니다. 만약 없는 경우, 빈 문자열로 대체합니다.
            if category is not None:
                row_category = category.text.replace("\n", " ")
            else:
                row_category = ""

            row = [row_title, row_category, "".join(content_corpus_list)]
    
            series = pd.Series(row, index=df.columns)
            df = df.append(series, ignore_index=True)
        return(df)

if __name__ == "__main__":
    A = NamuWiki()
    A_urls = NamuWiki.GetAurl(A, url)
    Df = NamuWiki.MakeDf(A, A_urls)
    print(Df.head())
    

