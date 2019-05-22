from django.test import TestCase
import requests
# Create your tests here.
code=''
data = {
    'js_code': code,
    'compilation_level': '',
                        'output_format': 'json',
'output_info': ['compiled_code', 'errors', 'warnings', 'statistics']
}
r=requests.post('https://resdig.cn/oco-gcc',json=data)
print(r.text)