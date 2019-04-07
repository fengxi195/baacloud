import requests as req
import base64

def captche_main(image_data):
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=【官网获取的AK】&client_secret=【官网获取的SK】'
    header = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    res = req.post(host) #获取百度access_token
    access_token = res.json()['access_token']
    temp_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token
    temp_data = {
        'image': base64.b64encode(image_data)
    }
    data = req.post(temp_url, data=temp_data, headers=header)
    Code = data.json()['words_result'][0]['words'].replace(' ', '')
    return Code
