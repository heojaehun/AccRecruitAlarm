import requests
from bs4 import BeautifulSoup
import send_mail
import os
import logging
import logging.config

dir = os.path.dirname(os.path.abspath(__file__)

class AccRecruitAlarm(object):
    def __init__(self):
        logging.config.fileConfig(dir + 'logging.conf')
        self.logger = logging.getLogger(__name__)

        self.url = 'https://www.acc.go.kr/notice/Employ/list'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'}
        self.history_dir = dir + '/history/'
        self.history_file_name = self.history_dir + 'acc_recruit.html'
        self.html = ''

        if not os.path.isdir(self.history_dir):
            os.mkdir(self.history_dir)


    def run(self):
        self.html = self.get_html()
        fresh_titles = self.get_title(self.html)
        old_titles = self.get_title(self.load_file())
        result = self.list_check(fresh_titles, old_titles)
        if len(result) > 0:
            message = '{:=^35}\n\n'.format('국립 아시아 문화전당 채용 공고 게시판 알림')
            for item in result:
                message = message + '  * {}\n'.format(str(item))

            message = message + '\n\n게시판 바로가기({})'.format(self.url)
            self.save_file(self.html)
            send_mail.send_mail(message)
            self.logger.info('업데이트 되었습니다.')
        else:
            self.logger.info('업데이트 할 내용이 없습니다.')
            
    def get_title(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        titles_tag = soup.select('.tr_title')
        titles = []

        for i in titles_tag:
            item = i.text.strip()
            if item != '제목':
                titles.append(item)

        return titles    # list type


    def load_file(self):
        file = ''
        try:
            file = open(self.history_file_name, 'rt').read()
        except:
            pass
            self.logger.info('불러올 파일이 없습니다.')

        return file     # str type


    def save_file(self, html):
        with open(self.history_file_name, 'wt', encoding = 'utf8') as file:
            file.write(html)


    def get_html(self):
        try:
            html = requests.get(self.url, headers = self.headers).text
            #self.logger.info('접속 성공')
        except:
            html = ''
            #self.logger.error('접속 실패')
        return html    # str type


    def list_check(self, list1, list2):
        '''
        Result = List1 - List2

        두 개의 리스트를 입력 받아 비교하는 함수
        리스트1의 항목 중 리스트2에 있는 것을 찾아 제거한다.
        '''
        result = []
        for item in list2:
            try:
                list1.remove(item)
            except:
                pass

        return list1


if __name__ == '__main__':
    print('Start ACC recruit alarm')
    ara = AccRecruitAlarm()
    ara.run()
