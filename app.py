from urllib import response
from flask import Flask, json, request, jsonify
import sys
from queue import Empty
import requests,re
from bs4 import BeautifulSoup
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def kakao_data(information_data):
    data = {
            "version" : "2.0",
            "template" : {
                "outputs" : [
                    {
                        "simpleText" : {
                            "text" : information_data
                        }
                    }
                ]
            }
        }

    return data

def food():
    url = 'https://www.tu.ac.kr/tuhome/diet.do'

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            list = soup.select_one("table").find_all(text=True)
        except:
            print('식단 업데이트가 되지 않는 날입니다.')
            return '식단 업데이트가 되지 않는 날입니다.(주말/공휴일)'

        while '\n' in list:
            list.remove('\n')

        title_list = []
        ul = soup.select_one("#cms-content > div > div > div.table-wrap > table > tbody")
        titles = ul.select('tr > th')

        for title in titles:
            title_list.append(title.get_text())

        for i in range(len(list)):
            list[i] = re.sub(':크림스프/야채샐러드/피클 김치', '', list[i])
            list[i] = re.sub('\r', ' ', list[i])
            for title in title_list:
                if(list[i] == title):
                    list[i] = '\n\n['+title+']'

        list[0] = re.sub('\n\n', '', list[0])

        str1 = ''
        for menu in list:
            str1 += menu +'\n'
        print(str1.strip())
        return str1.strip()

    else : 
        print('학교 홈페이지 문제 발생')
        return '학교 홈페이지 문제 발생'

def cup_food():
    menu = '''[컵밥]
    참치마요 - 4,700
    제육 - 5,000
    치즈 - 5,000
    오리훈제 - 5,200
    닭갈비 - 5,500
    베이컨 - 5,200
    떡갈비 - 5,200
    소불고기 - 5,500

[라면]
    신라면(컵) - 1,500
    진라면(컵) - 1,500
    김치사발면(컵) - 1,500
    육개장(컵) - 1,500
    튀김우동(컵) - 1,500
    너구리(컵) -1,500
    컵누들(컵) - 1,500
    신라면 - 3,000
        
[스낵/샌드위치]
    떡볶이  - 4,000
    라볶이 - 5,500
    바닐라와플 - 3,000
    초코와플 - 3,000
    딸기와플 - 3,000
    햄에그샌드위치 - 4,000
    햄치즈샌드위치 - 4,500

[음료/기타]
    콜라(190ml) - 1,000
    사이다(190ml) - 1,000
    콜라(500ml) - 2,000
    사이다(500ml) - 2,000
    골드메달 스파클링 애플주스 - 2,500
    마르티넬리 골드메달 애플주스 - 2,500
    팁코 쇼군 오렌지주스 - 1,700
    팁코 블로콜리주스 - 1,700
    공기밥 - 1,000'''

    print(menu)
    return menu

def china_food():
    menu = '''[메뉴]
    짜장면 4,500
    짜장면 곱배기 - 5,500
    우동 - 5,000
    우동 곱배기 - 7,000
    짬뽕 - 6,000
    짬뽕 곱빼기 - 7,000
    볶음밥 - 5,000
    볶음밥 곱배기 - 6,000
    새우볶음밥 - 7,000
    세우볶음밥 곱배기 - 8,000
    짜장밥 - 5,000
    짬뽕밥 - 6,000
    만두 - 5,000
    미니등심탕수육 - 10,000
    등심탕수육 - 15,000
    깐풍육 - 17,000
    미니깡풍육 - 12,000

[세트]
    베이징A세트(짜장면2+미니탕수육) - 17,000
    베이징B세트(짜장면1+짬뽕1+미니탕수육) - 19,000
    베이징C세트(짬뽕2+미니탕수육) - 21,000
    스토리A세트(짜장2+깐풍육) - 20,000
    스토리B세트(짜장1+짬뽕1+깐풍육) - 21,000
    스토리C세트(짬뽕2+깐풍육) - 23,000

[음료/기타]
    공기밥 - 1,000
    사이다 - 2,000
    콜라 - 2,000'''
    print(menu)

    return menu

def notice():
    url = "https://www.tu.ac.kr/tuhome/sub07_01_01.do"
    response = requests.get(url, verify=False)
    

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        try:
            notices = soup.find_all("td", attrs={"class":"subject"})
        except:
            print('등록 페이지에 글이 없습니다.')
            return '등록 페이지에 글이 없습니다.'
    
        i = 1
        str1 = '[학교 공지]\n\n'
        for notice in notices:
            title = notice.get_text().strip()
            link = notice.find("a")["href"]
            str1 += "["+str(i)+"] "+title+'\n'
            str1 += url+link+'\n\n'
            i = i+1
        
        print(str1.strip())
        return str1.strip()
    else:
        print('학교 홈페이지 문제 발생')
        return '학교 홈페이지 문제 발생'

def tu_cal():
    url = "https://www.tu.ac.kr/tuhome/scheduleTable.do"
    response = requests.get(url, verify=False)
    

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        try:
            notices = soup.find_all("tr", attrs={"class":"notice"})
        except:
            print('등록 페이지에 글이 없습니다.')
            return '등록 페이지에 글이 없습니다.'
    
        #print(notices)

        str1='학시일정 \n'
        for notice in notices:
            try:
                month = '\n'+'['+notice.find('th').get_text().strip()+'] \n'
                str1+=month
            except:
                pass
            finally:
                event = notice.select('td')[0].get_text()+' - '+notice.select('td')[1].get_text()+'\n'
                str1+=event

        print(str1.strip())
        return str1.strip()
    else:
        print('학교 홈페이지 문제 발생')
        return '학교 홈페이지 문제 발생'

app = Flask(__name__)

@app.route('/message', methods=['POST'])
def Message():
    content = request.get_json()
    content = content['userRequest']['utterance']
    content=content.replace("\n","")
    
    print(content)

    if content == "오늘의 학식":
        dataSend = kakao_data(food())
    elif content == "경대컵밥":
        dataSend = kakao_data(cup_food())
    elif content == "베이징스토리":
        dataSend = kakao_data(china_food())
    elif content == "포썸":
        pass
    elif content == "맘스터치":
        pass
    elif content == "동명기숙사 식단":
        pass
    elif content == "학교공지":
        dataSend = kakao_data(notice())
    elif content == "학사일정":
        dataSend = kakao_data(tu_cal())
    else:
        dataSend = {
            "version" : "2.0",
            "template" : {
                "outputs" : [
                    {
                        "simpleText" : {
                            "text" : 'error'
                        }
                    }
                ]
            }
        }
    return jsonify(dataSend)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)