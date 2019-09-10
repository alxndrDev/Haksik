import re
from django.shortcuts import render
from django.http import HttpResponse
import requests
from bs4 import BeautifulSoup
from .models import Menu
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import datetime
import json

when = ['Mon','Tue','Wed','Thu','Fri']


@csrf_exempt
def index(request):

    return HttpResponse("Hello World. You're at Ayo")

# 매주 일요일 실행 될 크롤러.
#크롤링 후 데이터베이스에 저장해야한다.
@csrf_exempt
def crawler(request):
    try:
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
        for j in range(0,len(c)):
            for i in range(0,4):
                if i == 0:
                    c[j][i] = when[j]+"/"+str(datetime.date.today() + datetime.timedelta(days=j))
                    print(c[j][i])
            
            
            fb = Menu(day=c[j][0], menu = c[j][1]+"/"+c[j][2]+"/"+c[j][3])
            fb.save()
        send_slack("삐빅..크롤러 정상 작동중입니다.")
    except Exception as ex:
        send_slack("뭔가 문제가 생겼다 임마!!! \n "+str(ex))

    return HttpResponse(c)


@csrf_exempt
def today(request):

    none_today = "학식없음"
    morning = none_today
    lunch = none_today
    dinner = none_today
    today_num = getWeekday()
    
    if((today_num != 5) & (today_num != 6)):  
        meal = get_Menu(1, today_num)
        if not meal is None:
            splited = meal.split('/')
            morning = splited[0]
            lunch = splited[1]
            dinner = splited[2]
   # return HttpResponse(meal)
    return JsonResponse({
        'date': datetime.date.today(),
        'morning' : morning,
        'lunch' : lunch,
        'dinner' : dinner,
    }, json_dumps_params={'ensure_ascii': False})

def getWeekday():
    return datetime.date.today().weekday()

@csrf_exempt
def tomorrow(request):
    today_num = getWeekday()
    none_today = "학식없음"
    morning = none_today
    lunch = none_today
    dinner = none_today
    if today_num == 6 :
        today_num = 0
    else :
        today_num = today_num + 1
        
    if((today_num != 5) & (today_num != 6)):
        meal = get_Menu(0, today_num)
        if not meal is None:
            splited = meal.split('/')
            morning = splited[0]
            lunch = splited[1]
            dinner = splited[2]
    return JsonResponse({
        'date': str(datetime.date.today()+datetime.timedelta(days = 1)),
        'morning' : morning,
        'lunch' : lunch,
        'dinner' : dinner,
    }, json_dumps_params={'ensure_ascii': False})


def get_Menu(flag, today_num):
    date_str = ""

    if flag == 0 : # 내일
        date_str = str(datetime.date.today()+datetime.timedelta(days = 1))
        try :
            meal = Menu.objects.get(day = when[today_num]+"/"+date_str).menu
        except ObjectDoesNotExist as a:
            return
    elif flag == 1: # 오늘
        date_str = str(datetime.date.today())
        try:
            meal = Menu.objects.get(day = when[today_num]+"/"+date_str).menu
        except ObjectDoesNotExist:
            return
    return meal

@csrf_exempt
def select_date(request):

    return 0

@csrf_exempt
def deleteDB(request):
    queryset = Menu.objects.all()
    for menu in queryset :
        menu.delete()
    return HttpResponse("Succeessssdasds")

@csrf_exempt
def available(request):
    try:
        send_slack("Server is still alive!")
        return HttpResponse(None)
    except Exception as ex:
        send_slack("Server has Something Problem. :(")
        return HttpResponse(None)


def send_slack(message):
   
    n = datetime.datetime.today().weekday()
    string = message

    url = "https://hooks.slack.com/services/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"
    content = string  
    payload = {
        "username":"BOT",
        "icon_emoji": ":ghost:",
        "text" : content,
    }
    requests.post(
        url, data = json.dumps(payload),
        headers={'Content-Type':'application/json'}
    )