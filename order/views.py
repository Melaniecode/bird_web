from contextlib import _RedirectStream, redirect_stderr
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from order.models import BirdModel
from django.db.models import Q


import json
import requests
from django.http import JsonResponse
# from openai import OpenAI
import openai

#global 實踐大學
mypos = {'lat' : 25.083275077002643, 'lng' : 121.54524968258359}

######  index
######  index
######  index
def index(request):
    google_api_key = 'AIzaSyDWEZFNIYdR26iHxXrLg9TtmzVVPvRIPNc'
    weather_msg = weather()
    if request.method == "POST":
        weather_msg = weather()
    return render(request,'index.html',locals())
#  index




######  about
######  about
######  about
def about(request):
    return render(request,'about/about.html')
#  about




######  birdlist
######  birdlist
######  birdlist
def birdlist(request):
    context = {}  # 初始化context

    if 'bird_search' in request.POST:
        bird_search_query = request.POST['bird_search']
        birds = BirdModel.objects.filter(Q(name__icontains=bird_search_query)
                                        |Q(nickName__icontains=bird_search_query)
                                        |Q(englishName__icontains=bird_search_query)
                                        |Q(familyName__icontains=bird_search_query)
                                        |Q(scientificName__icontains=bird_search_query)
                                        |Q(scientificName__icontains=bird_search_query)
                                        |Q(habitat__icontains=bird_search_query)
                                        |Q(season__icontains=bird_search_query)
                                        |(Q(startMonth__lte=bird_search_query) & Q(endMonth__gte=bird_search_query))
                                        )

        if len(birds) == 0: context['error_message'] = '未找到相關訊息。'
    else:
        birds = BirdModel.objects.all()
    return render(request, 'birdlist/birdlist.html', {'birds': birds, **context})

#  birdlist




######  guide
######  guide
######  guide
def guide(request):
    return render(request,'guide/guide.html')
#  guide




######  realtime
######  realtime
######  realtime
def realtime(request):
    # recent_msg = recent()
    return render(request,'realtime/realtime.html',locals())
#  realtime


#  index_test
def index_test(request):
    birds = BirdModel.objects.all().order_by('id')
    try:
        bird = BirdModel.objects.all()
        OK = "OKOK~"
    except:
        error_message = "error"
    return render(request,'index_test.html',locals())




######  openAI
######  openAI
######  openAI
openai.api_key = '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'

@csrf_exempt
def openAI_get_completion(message):
    ##### printinTerminal ######
    print('gptcom_message：')
    print(message)
    completion  = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages = [
            {"role": "system", "content": "請都用繁體中文回答"},
            #{"role": "system", "content": "你是Dr.owl，一個能夠回答問題和提供資訊的貓頭鷹博士"},
            {"role": "system", "content": "網站名稱或是你的網站名稱或是你們網站名稱叫做候鳥來了，是一個專門提供候鳥相關資訊的網站。"},
            {"role": "system", "content": "網站介紹或是你的網站介紹或是你們網站介紹：候鳥來了，是一個專門提供候鳥相關資訊的網站，我們提供下列資訊：即刻賞鳥、候鳥圖鑑、賞鳥須知、候鳥博士。1. 即刻賞鳥：提供一些熱門的候鳥觀察點，這些地點通常是候鳥遷徙的停歇點或是重要棲息地。2. 候鳥圖鑑：提供各種常見候鳥的介紹，包括圖片、特徵等。3. 賞鳥須知：提供賞鳥的行前須知和注意事項。4. 候鳥博士：解答各種鳥類相關問題。我們希望能夠幫助您更深入了解鳥類世界，享受賞鳥的樂趣。如果您有任何問題或建議，歡迎到「關於我們」與我們聯繫！"},

            {'role': 'user', 'content': message}
        ],
        max_tokens=2048,
        n=1,
        stop=None,
        temperature=0.9,

    )

    response = completion['choices'][0]['message']['content']
    ##### printinTerminal #####
    print('gpt_response：')
    print(response)
    return response

def openAI_gpt(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        ##### printinTerminal #####
        print('gpt_prompt：')
        print(prompt)
        response = openAI_get_completion(prompt)
        return JsonResponse({'response': response})
    return render(request, 'openAI_gpt.html')
#  openAI




######  getMyloc
######  getMyloc
######  getMyloc
@csrf_exempt
def getMyloc(request):
    if request.method == "POST":
        #posJson = request.POST.get('posJson')
        posJson = json.loads(request.body.decode('utf-8'))
        #print(posJson)
        global mypos  #global
        mypos = posJson
        #print('getMyloc')
        #print(mypos)
        #print(mypos.items())
        #print(request.body.decode('utf-8'))
        weather_msg = weather()
        myaddress = latlng_to_address(mypos)
        ##### printinTerminal #####
        print('weather_msg：')
        print(weather_msg)
        ##### printinTerminal #####
        print('myaddress：')
        print(myaddress)

        return JsonResponse({
                'message': 'success',
                'weather_msg': weather_msg,
                'myaddress' : myaddress
            })
    else:
        return JsonResponse({
                'message': 'error'
            })
#  getMyloc




######  upload_img
######  upload_img 
######  upload_img
def upload_img(request):
    Birds = BirdModel.objects.all()
    #findname
    if request.method == 'POST':
        mname = request.POST['name']  # get name
        try :
            #資料表.objects.get(查詢條件)
            mbird = BirdModel.objects.get(name=mname)
            #修改
            mbird.photo = request.FILES.get('photo')
            mbird.save()  # save image
            return HttpResponse('成功新增'+mname+'照片')
        except:
            return HttpResponse('找不到'+mname)
    return render(request, 'upload_img.html',locals())
#  upload_img




######  weather_API
######  weather_API
######  weather_API
def weather():
    global mypos  #global
    my_address_components = get_administrative_area_level_1(mypos)
    #print(str(my_address_components))
    for index in range(0,10):
        #print(str(index))
        if((str(my_address_components[index]['long_name']).find('市')!=-1) or (str(my_address_components[index]['long_name']).find('縣')!=-1)):
            #print(str(my_address_components[index]['long_name']))
            mytown = str(my_address_components[index]['long_name'])
            #print(mytown)
            mytown = mytown.replace('台','臺')
            #print(mytown)
            break
    url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        "Authorization": "CWB-A38B5122-DF26-47EB-A652-1AD1A5643F5C",
        "locationName": mytown,
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = json.loads(response.text)
        location = data["records"]["location"][0]["locationName"]
        weather_elements = data["records"]["location"][0]["weatherElement"]
        weather_state = weather_elements[0]["time"][0]["parameter"]["parameterName"]
        rain_prob = weather_elements[1]["time"][0]["parameter"]["parameterName"]
        min_tem = weather_elements[2]["time"][0]["parameter"]["parameterName"]
        comfort = weather_elements[3]["time"][0]["parameter"]["parameterName"]
        max_tem = weather_elements[4]["time"][0]["parameter"]["parameterName"]

        weather_msg = {
            'location' : location,
            'weather_state': weather_state,
            'rain_prob':rain_prob,
            'min_tem':min_tem,
            'comfort':comfort,
            'max_tem':max_tem }
        ##### printinTerminal #####
        print('weather_msg：')
        print(weather_msg)
    return weather_msg
#  weather_API





######  address_to_latlng
######  address_to_latlng
######  address_to_latlng
def address_to_latlng(loc):
    params = {
        'key':'AIzaSyDWEZFNIYdR26iHxXrLg9TtmzVVPvRIPNc',
        'address' : loc}
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(url, params=params)
    #print(response.text)
    json_to_dict_lat_lng = json.loads(response.text)
    lat_lng = {
        'lat' :json_to_dict_lat_lng['results'][0]['geometry']['location']['lat'],
        'lng' :json_to_dict_lat_lng['results'][0]['geometry']['location']['lng']
    }
    return lat_lng
#  address_to_latlng





######  latlng_to_address
######  latlng_to_address
######  latlng_to_address
def latlng_to_address(lat_lng):
    lat_lng_value = str(lat_lng['lat'])+','+str(lat_lng['lng'])
    params = {
        'key':'AIzaSyDWEZFNIYdR26iHxXrLg9TtmzVVPvRIPNc',
        'latlng' : lat_lng_value,
        'language':'zh-TW'}
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(url, params=params)
    #print(response.text)
    json_to_dict_address = json.loads(response.text)
    address = json_to_dict_address['results'][0]['formatted_address']
    #print(address)
    return address
#  latlng_to_address




######  get_administrative_area_level_1
######  get_administrative_area_level_1
######  get_administrative_area_level_1
def get_administrative_area_level_1(lat_lng):
    lat_lng_value = str(lat_lng['lat'])+','+str(lat_lng['lng'])
    params = {
        'key':'AIzaSyDWEZFNIYdR26iHxXrLg9TtmzVVPvRIPNc',
        'latlng' : lat_lng_value,
        'language':'zh-TW'}
    url = 'https://maps.googleapis.com/maps/api/geocode/json?'
    response = requests.get(url, params=params)
    #print(response.text)
    json_to_dict_address = json.loads(response.text)
    address_components = json_to_dict_address['results'][0]['address_components']
    #print(address_components)
    return address_components

#  get_administrative_area_level_1





######   test
######   test
######   test
@csrf_exempt
def test(request):
    global mypos  #global
    google_api_key = 'AIzaSyDWEZFNIYdR26iHxXrLg9TtmzVVPvRIPNc'
    weather_msg = weather()
    myaddress = latlng_to_address(mypos)
    if request.method == "POST":
        weather_msg = weather()
        #print(mypos)
        myaddress = latlng_to_address(mypos)
        #print(myaddress)
    return render(request,'test.html',locals())
######   test
