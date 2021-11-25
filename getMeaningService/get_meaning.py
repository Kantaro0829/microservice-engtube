import requests
from bs4 import BeautifulSoup
from urllib import request

from werkzeug.wrappers import response

class GetMeaning():
    def __init__(self, eng_list):
        self.eng_list = eng_list
        self.default_url = "https://ejje.weblio.jp/content/"
        self.headers = {"User-Agent": "hoge"}
        self.result_list = []
        self.failure_list = []
    
    def scrape_from_weblio(self):
        for word in self.eng_list:
            try:
                eng_jp_dic = {} #英語＋意味（日本語）の辞書型配列を初期化
                url = self.default_url + word #default_url/英単語 でほしいページに飛べる

                resp = request.urlopen(url)
                soup = BeautifulSoup(resp, 'html.parser')
                jp = soup.find('td', class_="content-explanation ej") #HTML内のclass "content-explanation ej" を切り出し
                eng = soup.find(id="h1Query") #HTML内のid "h1Query"を切り出し
                print("type of the jp ##################")
                print(jp.get_text())
                eng_jp_dic['eng'] = eng.get_text() #jp のtext部分（英語）を切り取り辞書に追加
                eng_jp_dic['jp'] = jp.get_text() #engのtext部分（日本語意味）を切りとり辞書に追加

                self.result_list.append(eng_jp_dic) #日本語意味、英単語セットの辞書配列を追加
                resp.close()
            except:
                #スクレイピングできなかった単語を記録
                self.failure_list.append(word)
                resp.close()

        return self.result_list, self.failure_list
