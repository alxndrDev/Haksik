from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup

def index(request):
    
    return HttpResponse("Hello World. You're at Ayo")

# 매주 일요일 실행 될 크롤러. 
#크롤링 후 데이터베이스에 저장해야한다.
def crawler(request):
    url = "http://www.kopo.ac.kr/incheon/content.do?menu=6893"
    header = {'user-agent': ''}
    response = requests.get(url)

    html = response.text

    soup = BeautifulSoup(html, 'html.parser') #html.parser를 사용해서 soup에 넣겠다.

    contents = soup.select('.tbl_table tbody tr')

    print(type(contents))
    c =[]
    for i in range(1,6):
        a = contents[i].text.strip('\n').split('\n')
        c.append([x for x in a if x])

    for j in c:
        for i in j:
            print(i)
        print("*"*50)
    return HttpResponse(c)