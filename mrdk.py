import time
import requests
import base64
import json
from priv import conf, loc, notice


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
    return r[lt.tm_mday - 1] + u[lt.tm_hour - 1]


class AutoDk:
    app = {
        'check': 'https://we.cqupt.edu.cn/api/mrdk/get_mrdk_flag.php',
        'map': 'https://apis.map.qq.com/ws/geocoder/v1?location={1}%2C{0}&key=7IMBZ-XWMWW-D4FR5-R3NAG-G7A7S-FMBFN',
        'run': 'https://we.cqupt.edu.cn/api/mrdk/post_mrdk_info.php'
    }

    geo = {}

    def __init__(self, config=None, location=None, modify=None):
        print(
            f'[+] Starting time: {time.asctime(time.localtime(time.time()))}')
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
        self.count = 0

        print('[+] Configuration loaded. Waiting for time.')

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

    def get_geo(self, at_school: bool = False):
        if not at_school:
            res = requests.get(self.app['map'].format(*self.loc))
        # 没有网，我们就只能回家了
        # 拜托，我阿妈超凶的
        # School location: 106.614827,29.540015
        else:
            res = """
{
    "status": 0,
    "message": "query ok",
    "request_id": "065dad90-3c66-11ec-848d-525400dcfc96",
    "result": {
        "location": {
            "lat": 29.537429,
            "lng": 106.614951
        },
        "address": "重庆市南岸区黄明路",
        "formatted_addresses": {
            "recommend": "重庆邮电大学东北",
            "rough": "重庆邮电大学东北"
        },
        "address_component": {
            "nation": "中国",
            "province": "重庆市",
            "city": "重庆市",
            "district": "南岸区",
            "street": "黄明路",
            "street_number": "黄明路"
        },
        "ad_info": {
            "nation_code": "156",
            "adcode": "500108",
            "city_code": "156500000",
            "name": "中国,重庆市,重庆市,南岸区",
            "location": {
                "lat": 29.5,
                "lng": 106.745132
            },
            "nation": "中国",
            "province": "重庆市",
            "city": "重庆市",
            "district": "南岸区"
        },
        "address_reference": {
            "street_number": {
                "id": "",
                "title": "",
                "location": {
                    "lat": 29.534351,
                    "lng": 106.72261
                },
                "_distance": 349.8,
                "_dir_desc": "东"
            },
            "town": {
                "id": "500108007",
                "title": "南山街道",
                "location": {
                    "lat": 29.58695,
                    "lng": 106.642792
                },
                "_distance": 0,
                "_dir_desc": "内"
            },
            "street": {
                "id": "5663199003245115351",
                "title": "黄明路",
                "location": {
                    "lat": 29.534351,
                    "lng": 106.72261
                },
                "_distance": 349.8,
                "_dir_desc": "东"
            },
            "landmark_l2": {
                "id": "2695987747850306161",
                "title": "重庆邮电大学",
                "location": {
                    "lat": 29.532326,
                    "lng": 106.607956
                },
                "_distance": 357.4,
                "_dir_desc": "东北"
            }
        }
    }
}
"""
        res = json.loads(res.text)['result']
        # 我才不要回家（指手动打卡）
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
        self.count += 1
        print(
            f'\n[+] Checking time: {time.asctime(time.localtime(time.time()))}')
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
            # print(data)
            print('[+] Starting DaKa...')

            res = requests.post(self.app['run'], data=dump(data))
            if res.status_code == 200:
                notice(data, res.text + "没问题，打卡成功😊")
            else:
                notice(data, res.text + "今年毕业证要少印一张了🐶")

        else:
            notice(None, flag)
            print(f'[-] You have already clocked in {flag} time(s). Exit.')

        print('[+] Done.')


if __name__ == '__main__':
    ad = AutoDk(config=conf, location=loc)
    ad.run()
