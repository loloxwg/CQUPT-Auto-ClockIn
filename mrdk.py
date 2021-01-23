import time
import requests
import base64
import json
from priv import conf, loc


# 坐标来这查
# http://api.map.baidu.com/lbsapi/getpoint/index.html


def dump(data):
    enc = json.dumps(data)
    mod = {'key': base64.b64encode(enc.encode()).decode()}
    return mod


def get_key():
    r = ["s9ZS", "jQkB", "RuQM", "O0_L", "Buxf", "LepV", "Ec6w", "zPLD", "eZry", "QjBF", "XPB0", "zlTr", "YDr2",
         "Mfdu", "HSoi", "frhT", "GOdB", "AEN0", "zX0T", "wJg1", "fCmn", "SM3z", "2U5I", "LI3u", "3rAY", "aoa4",
         "Jf9u", "M69T", "XCea", "63gc", "6_Kf"]
    u = ["89KC", "pzTS", "wgte", "29_3", "GpdG", "FDYl", "vsE9", "SPJk", "_buC", "GPHN", "OKax", "_Kk4", "hYxa",
         "1BC5", "oBk_", "JgUW", "0CPR", "jlEh", "gBGg", "frS6", "4ads", "Iwfk", "TCgR", "wbjP"]
    lt = time.localtime(time.time())
    return r[lt.tm_mday] + u[lt.tm_hour]


class AutoDk:
    app = {
        'check': 'https://we.cqu.pt/api/mrdk/get_mrdk_flag.php',
        'map': 'https://apis.map.qq.com/ws/geocoder/v1?location={1}%2C{0}&key=7IMBZ-XWMWW-D4FR5-R3NAG-G7A7S-FMBFN',
        'run': 'https://we.cqu.pt/api/mrdk/post_mrdk_info.php'
    }

    geo = {}

    def __init__(self, config=None, location=None, modify=None):
        print(
            f'[+] Running time: {time.asctime(time.localtime(time.time()))}')
        print('[+] Initializing script.')
        if modify is None:
            modify = {}
        if config is None:
            exit('[-] Cannot found config.')
        if location is None:
            exit('[-] Cannot found location.')

        self.loc = location
        self.conf = config
        self.modify = modify

    def check(self):
        data = {
            'xh': self.conf['xh'],
            'timestamp': round(time.time())
        }

        print(f"[+] Checking statues of {self.conf['xh']}...")

        res = requests.post(self.app['check'], data=dump(data))
        res = json.loads(res.text)['data']
        if res is not None:
            return res['count']
        else:
            exit('[-] Flag Check Error')

    def get_geo(self):
        res = requests.get(self.app['map'].format(*self.loc))
        res = json.loads(res.text)['result']
        t = res['address_component']
        a, b, c, d, e = (
            t['nation'], t['province'], t['city'], t['district'], t['street']
        )
        self.geo = {
            'szdq': f'{b},{c},{d}',
            'locationBig': f"{res['ad_info']['name']}",
            'locationSmall': f'{b}{c}{d}{e}',
            'latitude': f"{res['location']['lat']}",
            'longitude': f"{res['location']['lng']}"
        }
        return self.geo  # 供查询

    def run(self):
        flag = self.check()
        if flag == '0':
            print('[+] Loading configurations...')
            data = {"openid": "",
                    "ywjcqzbl": "低风险", "ywjchblj": "无", "xjzdywqzbl": "无", "twsfzc": "是",
                    "ywytdzz": "无", "beizhu": "无", "mrdkkey": get_key(), "timestamp": round(time.time())}
            self.get_geo()
            data.update(self.modify)
            data.update(self.conf)
            data.update(self.geo)

            # start data
            print(data)
            print('[+] Starting DaKa...')

            res = requests.post(self.app['run'], data=dump(data))
            print(res.text)
        else:
            print(f'[-] You have already clocked in {flag} time(s). Exit.')

        print('[+] Done.')


if __name__ == '__main__':
    ad = AutoDk(config=conf, location=loc)
    ad.run()
