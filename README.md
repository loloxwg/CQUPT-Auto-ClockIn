# 某高校自动打卡脚本

> 正在开发中，24日测试完毕后进行打包发布

你需要创建一个priv.py，自行填入以下信息
```python
conf = {
    'xh': xxx,
    'name': 'xxx',
    'xb': 'x',
    'lxdh': xxx,  # 联系电话
    'xxdz': 'xxx',  # 详细地址
    'openid': 'xxx'  # openId
}

# http://api.map.baidu.com/lbsapi/getpoint/index.html
loc = (x, x)  # 在以上链接获取您的经纬度信息，直接复制
```