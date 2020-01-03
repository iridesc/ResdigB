import requests


data = {
    # 静态数据请求
    'reason': 'getStaticData',
    # 'reason': 'getCasts',
    # 'reason': 'getHots',
    # 'reason': 'getDonors',
    # 'reason': 'getAmount',

    # 动态数据请求
    'reason': 'getDynamicData'
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
r = requests.post('http://127.0.0.1:8000/api/', json=data)
print(r.json())
