from flask import Flask, json, request, jsonify
import sys
from queue import Empty
import requests,re
from bs4 import BeautifulSoup



def food():
    url = 'https://www.tu.ac.kr/tuhome/diet.do'

    response = requests.get(url)

    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        try:
            list = soup.select_one("table").find_all(text=True)
        except:
            print('식단 업데이트가 되지 않은 날입니다.')
            return '식단 업데이트가 되지 않은 날입니다.'            

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
        print(str1)
        return str1

    else : 
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
        dataSend = {
            "version" : "2.0",
            "template" : {
                "outputs" : [
                    {
                        "simpleText" : {
                            "text" : food()
                        }
                    }
                ]
            }
        }
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