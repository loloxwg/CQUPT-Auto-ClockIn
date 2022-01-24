import requests

conf = {
    'xh': 20,  # 学号
    'name': '王尼玛',  # 名字
    'xb': '男',  # 性别
    'lxdh': 110,  # 联系电话
    'xxdz': '太阳系地球村',  # 详细地址
    'openid': '自己抓'  # openId
}

# http://api.map.baidu.com/lbsapi/getpoint/index.html

loc = (x, y)  # 在以上链接获取您的经纬度信息，直接复制


# 通知处理函数，用于打卡信息推送
# 以下是接入 server酱 微信推送 的一个示例

# https://sct.ftqq.com/ 注册绑定 把SendKey填写进下方
SendKey = '自己复制'


def notice(data, txt):
    url = 'https://sctapi.ftqq.com/' + SendKey + '.send'
    print('[+] Receive data:', txt)
    print('[+] Notice: posting to sever酱...')
    title = txt
    if not data:
        txt = f'今日已打卡：{txt} 次'
        title = '已经打过卡了😁'

    res = requests.post(url, params={
        'title': title,
        'desp': txt
    })
