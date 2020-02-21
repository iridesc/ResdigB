
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import json
import base64

BLOCKSIZE=16
PADSTYLE='pkcs7'
def GetMode():
    KEY=b'q863cqfiwyug72jc'
    IV=b'1234567812345678'
    MODE=AES.MODE_CBC
    return AES.new(KEY,MODE,IV)
    
def Encrypto(r_data_str):
    obj=GetMode()

    # print(data)
    r_data_bytes=bytes(r_data_str,'utf-8')
    #补齐字节
    r_data_paded_bytes= pad(r_data_bytes,BLOCKSIZE,PADSTYLE)
    #加密
    e_data_bytes = obj.encrypt(r_data_paded_bytes)#.hex()
    e_data_str=str(e_data_bytes,encoding='utf-8',errors="ignore")
    print(e_data_str)
    return e_data_str
    

def Decrypto(e_data_str):
    obj=GetMode()
    
    e_data_bytes= base64.b64decode(e_data_str)
    # print('e_data_bytes------------',e_data_bytes)
    r_data_paded_bytes=obj.decrypt(e_data_bytes)
    r_data_bytes=unpad(r_data_paded_bytes,BLOCKSIZE,PADSTYLE)
    # print('data_bytes------------',r_data_bytes)
    r_data_str=str(r_data_bytes,encoding='utf-8',errors="ignore")
    print('>',r_data_str,'<')
    return r_data_str
   


a="."
Decrypto( Encrypto(a) )