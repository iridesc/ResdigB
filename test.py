import requests


data = {
    # 'reason': 'getEngines'

    # 'reason': 'getTasks',

    # 'reason': 'checkKeyword',
    # 'keyword': 'batman1',

    # 'reason': 'getRess',
    # 'keyword': 'batmanisdgf',

    # 'reason': 'dig',
    # 'keyword': 'batman',

    # 'reason': 'getHots',

    # 'reason': 'getAmount',



    'reason': 'getCasts',

    # 'reason': 'getDonors',


    # 'reason': 'sendFeedback',
    # 'info':'hahahha'

    # 'reason': 'sendMsg',
    # 'info':'hahahhaisdg\>>'

    # 'reason': 'getMsgs',


}
r = requests.post('http://127.0.0.1:8000/api/', json=data)
print(r.json())
