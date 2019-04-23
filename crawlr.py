import requests
from bs4 import BeautifulSoup
import datetime
import json
c =[]
def crawler():
    url = "http://www.kopo.ac.kr/incheon/content.do?menu=6893"
    
    response = requests.get(url)

    html = response.text

    soup = BeautifulSoup(html, 'html.parser') #html.parser를 사용해서 soup에 넣겠다.

    contents = soup.select('.tbl_table tbody tr')

    

    for i in range(1,6):
        a = contents[i].get_text().strip('\n').split('\n')
        c.append([x for x in a if x])
    when = ['월','화','수','목','금',]
    for j in range(0,len(c)):
        for i in range(0,4):
            if i == 0:
                c[j][i] = when[j]+"/"+str(datetime.date.today() + datetime.timedelta(days=j))

def send_slack():
   
    n = datetime.datetime.today().weekday()
    string = make_str(c[n])

    url = "Your Key"
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
def make_str(arr):
    meal = ["\t\t\t",'조식 | ','중식 | ', '석식 |']
    string = ""
    j = 0
    for i in arr:
        string+= meal[j]+"\t"+i + "\n"
        j = j+ 1
    return string
if __name__ == "__main__":
    crawler()
    send_slack()
