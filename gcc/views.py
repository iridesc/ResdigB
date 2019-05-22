from django.shortcuts import render
import json,requests,traceback
from django.http import HttpResponse,JsonResponse,HttpResponseNotAllowed,HttpResponseBadRequest

# Create your views here.
def gcc(request):
    print('-------------------------------------------')
    if request.method=='POST':
        try:
            b=request.body
            data = json.loads(str(b,'utf8'))
            host = 'http://104.248.79.138/api/'
            r=requests.post(host,json=data)
            data=r.json()
        except:
            data={
                'agencyerror': {
                    'agencyname': 'local',
                    'error': traceback.format_exc()
                }
            }
        return JsonResponse(data)
    else:
        return HttpResponse(render(request, 'gcc_home.html'))