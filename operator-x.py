import requests

imagepath='./static/resdig/background.jpg'
url='https://cn.bing.com/HPImageArchive.aspx'
data={
    'n':1,
    'format':'js'
}
baselink=requests.get(url,data).json()['images'][0]['url']
link='https://cn.bing.com'+baselink
image=requests.get(link,)
with open(imagepath, 'wb') as fd:
        fd.write(image.content)
