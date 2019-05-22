from django.test import TestCase
from Crypto.Cipher import AES
import requests,json
# Create your tests here.


class cstring(bytes):
    key=b'q863cqfiwyug72jc'
    mode=AES.new(key,AES.MODE_ECB)

    def encrypto(self):
        #补齐字节
        s=self
        while len(s) % 16 != 0:
            s = s + b' '
        #加密
        return self.mode.encrypt(s).hex()

    def decrypto(self):

        selfbytes=bytes().fromhex(str(self, 'utf-8'))
        b=self.mode.decrypt(selfbytes)
        return str(b,encoding='utf-8',errors="ignore")



url='https://www.resdig.cn/api'
data={
    'reason':'getElist'
}
data = cstring(bytes(json.dumps(data), 'utf-8')).encrypto()
#data=cstring(data).decrypto()
print(data)
r=requests.post(url,data)
print(r.status_code)
print(r.text)
print('---------------------------------')