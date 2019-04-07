# coding = utf-8
import requests as req
import json
import datetime
import re
from time import sleep
import baiduyun_captcha


class baacloud(object):
    """docstring for ClassName"""

    def __init__(self):
        """初始化"""
        email = 'baacloud账号'
        passwd = 'baacloud密码'
        self.Login_url = "https://{}/modules/_login.php"
        self.captcha_url = "https://{}/other/captcha.php"
        self.Login_data = {
            'email': email,
            'passwd': passwd,
            'remember_me': 'week'
        }
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3739.0 Safari/537.36 Edg/75.0.111.0"
        }
        self.session = req.session()

    def __del__(self):
        print('Project_wait_5_s')
        sleep(5)

    def get_cat(self, domain):
        """获取&识别验证码"""
        try:
            content = self.session.get(self.captcha_url.format(domain), headers=self.header).content
            yzm = baiduyun_captcha.captche_main(content)
            print(yzm)
            Code_Url = 'https://' + domain + '/modules/_checkin.php?captcha=' + yzm
            print(Code_Url)
            data = self.session.get(str(Code_Url), headers=self.header)
        except Exception as e:
            print('Project_Error...')
            with open("Error.data", 'a+', encoding='utf-8') as f:
                f.write(str(datetime.datetime.now()) + ':' + str(e) + '\n')
        else:
            result = re.findall(r'<script>alert(.*);self.location=document.referrer;</script>', data.text)
            if result[0] == "('验证码错误!')":
                print('%s' % (result[0]))
                self.get_cat(domain)
            else:
                with open('ok.jj', 'a+', encoding='utf-8') as f:
                    f.write(str(datetime.datetime.now()) + ':' + str(result[0]) + '\n')
                print('%s' % (result[0]))

    def login(self, domain='www.baacloud61.com'):
        """登录baacloud"""
        try:
            html = self.session.post(self.Login_url.format(domain), data=self.Login_data, headers=self.header,
                                     timeout=30)
            html.encoding = html.apparent_encoding
            Login_data = json.loads(html.text)
        except Exception as e:
            print('Login_Error')
            with open("Error.data", 'a+', encoding='utf-8') as f:
                f.write(str(datetime.datetime.now()) + '：' + str(e) + '\n')
        else:
            if Login_data['ok'] == '1':
                print('Login_Ok!')
                self.get_cat(domain)

    def run(self):
        while True:
            now_time = datetime.datetime.now()
            # if (now_time.hour) and (now_time.minute) and (now_time.second):
            # 设置登陆时间
            if (int(now_time.hour) == int(7)) and (int(now_time.minute) == int(5)):
                # if now_time.hour and now_time.minute:
                # 获取Baacloud最新地址
                Code_url = req.get('http://api.cn3.me/url.php?id=3')
                domain = Code_url.url.split('/')[-3]
                print(domain)
                self.login(domain)
                sleep(60)
            sleep(1)
            # break


if __name__ == '__main__':
    bc = baacloud()
    bc.run()
