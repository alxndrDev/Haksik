from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from .models import Menu
import re
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    
    return HttpResponse("Hello World. You're at Ayo")

# 매주 일요일 실행 될 크롤러. 
#크롤링 후 데이터베이스에 저장해야한다.
@csrf_exempt
def crawler(request):
    url = "http://www.kopo.ac.kr/incheon/content.do?menu=6893"
    header = {'user-agent': ''}
    response = requests.get(url)

    html = response.text

    soup = BeautifulSoup(html, 'html.parser') #html.parser를 사용해서 soup에 넣겠다.

    contents = soup.select('.tbl_table tbody tr')

    c =[]
    menu_db = Menu.objects.all()
    menu_db.delete()
    for i in range(1,6):
        a = contents[i].get_text().strip('\n').split('\n')
        c.append([x for x in a if x])
    when = ['Mon','Tue','Wed','Thu','Fri']
    for j in range(0,len(c)):
        for i in range(0,4):
            print(j , i)
            if i == 0:
                c[j][i] = when[j]+"/"+str(datetime.date.today() + datetime.timedelta(days=j))
            print(c[j][i])
            print("*"*50)
        
        fb = Menu(day=c[j][0], menu = c[j][1]+"/"+c[j][2]+"/"+c[j][3])
        fb.save()
    
    return HttpResponse(c)

@csrf_exempt
def keyboard(request):
    
    return JsonResponse({
        'type':'buttons',
        'button' : ['today','tomorrow'],
    }, json_dumps_params={'ensure_ascii': True})

@csrf_exempt
def today(request):
    today = datetime.date.today().weekday()
    when = ['Mon','Tue','Wed','Thu','Fri']
    meal = Menu.objects.get(day = when[0]+"/"+str(datetime.date.today())).menu
    splited = meal.split('/')
    morning = splited[0]
    lunch = splited[1]
    dinner = splited[2]
   # return HttpResponse(meal)
    return JsonResponse({
        'morning' : morning,
        'lunch' : lunch,
        'dinner' : dinner,
    }, json_dumps_params={'ensure_ascii': False})



@csrf_exempt
def deleteDB(request):
    queryset = Menu.objects.all()
    for menu in queryset :
        menu.delete()
    return HttpResponse("Succeessssdasds")
