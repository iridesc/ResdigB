import requests
import re,json
from unlit.encrypto import encrypto,decrypto

from AesEverywhere import aes256
PASSWORD="q863cqfiwyug72jc"

data = {
    # 静态数据请求
    "reason": "getStaticData",
    # 'reason': 'getCasts',
    # 'reason': 'getHots',
    # 'reason': 'getDonors',
    # 'reason': 'getAmount',
    # 动态数据请求
    # "reason": "getDynamicData"
    # 'reason': 'getEngines'
    # 'reason': 'getMsgs',
    # 'reason': 'getTasks',
    # 即时数据请求
    # 'reason': 'checkKeyword',
    # 'keyword': 'batman1',
    # 'reason': 'getRess',
    # 'keyword': 'batmanisdgf',
    # 'reason': 'dig',
    # 'keyword': 'batman',
    # 'reason': 'sendFeedback',
    # 'info':'hahahha'
    # 'reason': 'sendMsg',
    # 'info':'hahahhaisdg\>>'
}

r = requests.post('http://127.0.0.1:8000/api/', data=aes256.encrypt(json.dumps(data),PASSWORD))
print(aes256.decrypt(r.content,PASSWORD))
# # 测试加密解密
# a=json.dumps({})

# # encryption
# encrypted = aes256.encrypt(a, PASSWORD)
# print(encrypted)
# # decryption
# print(aes256.decrypt(encrypted, 'PASSWORD'))


# e=encrypto(a)
# print(e)
# print('************************')
# d=decrypto(e)
# print(d)