from inlinestyler.utils import inline_css
from premailer import transform
from time import sleep
import requests
from lxml import html
from lxml import etree
import sys
import json
import selenium
from selenium import webdriver

from requests.api import head


city = '成都'
if len(sys.argv) == 2:
    city = sys.argv[1]

url = f'https://www.damaotuanjian.com/product?offset=0&limit=10&city={city}'

head = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",

}

#ret = requests.get(url=url,headers=head)
#doc = etree.HTML(ret.text)
# print(ret.text)


# rootUrl = "//div[@class='inner-product-list product-list-content']/a"
# datas = doc.xpath(rootUrl)
# datalist = []
# index = 1

# for data in datas:

#     insertData = {
#     "title":"",             #标题，name
#     "images[0]":"",         #封面，//字符串，图片链接  cover
#     "jianjie":"",           #简介，   sellingPoints
#     "activityTab":"",       #活动标签，benifits
#     "fateDay":"",           #团建天数，days nights
#     "tripsNumber":"",       #出行人数，minBooking-maxBooking
#     "averagePrice":"",      #人均价格，price
#     "foodIndex":0,          #餐饮指数，recommendedIndexs
#     "stayIndex":0,          #住宿指数，recommendedIndexs
#     "leagueIndex":0,        #团建指数，recommendedIndexs
#     "powerIndex":0,         #团建指数，recommendedIndexs
#     "detail"""            #富文本详情，
#     "leaguePlay":"",        #团建玩法，playings
#     "type":"",              #团建类型 type
#     "moneySort":"",         #价格排序标识，
#     "swiperImages":""      #轮播图，#字符串，多张逗号分隔
#     }

#     href = doc.xpath(rootUrl + f"[{index}]/@href")
#     if len(href) > 0 :
#         insertData['detail'] = href[0]
#     title = doc.xpath(rootUrl + f"[{index}]//div[@class='inner-product-list-item-title']/text()")
#     if len(title) > 0:
#         insertData['title'] = title[0]
#     image = doc.xpath(rootUrl + f"[{index}]//div[@class='inner-product-list-item-img']/img/@lazy")

#     taglist = doc.xpath(rootUrl + f"[{index}]//div[@class='inner-product-list-item-tags']/span/text()")
#     tags=''
#     for tag in taglist:
#         tags = tags + tag + ','
#     types = doc.xpath(rootUrl + f"[{index}]//div[@class='inner-product-list-item-type']/text()")
#     if len(types) == 3:
#         insertData['fateDay'] = types[1]
#         insertData['tripsNumber'] = types[2]
#     prices = doc.xpath(rootUrl + f"[{index}]//div[@class='inner-product-list-item-price']/span/text()")
#     if len(prices) > 0:
#         insertData['averagePrice'] = prices[0]
#     print(prices)
#     index = index + 1
#     datalist.append(insertData)

# print(datalist)
hasdownload=[]

def downloadImage(imageurl):
    if imageurl in hasdownload:
        return ""
    hasdownload.append(imageurl)
    try:
        downloadImageUrl = f'http://47.102.205.71:3000/upload/downloadimgbyurl?url={imageurl}'
        downloadRes = requests.get(url=downloadImageUrl, headers=head)
        downloadDatas = json.loads(downloadRes.content.decode('utf-8'))
        if downloadDatas['code'] == 20000:
            return downloadDatas['data']['url']
        else:
            return ""
    except:
        return ""


requestUrl = 'https://www.damaotuanjian.com/open/product/list'

param = {
    "city": city,
    "limit": 49,
    "offset": 50
}

ret = requests.get(url=requestUrl, params=param, headers=head)
# print(ret.content.decode('utf-8'))


datamap = json.loads(ret.content.decode('utf-8'))


# print(datamap['items'])
# print(type(datamap['items']))

#datafile = open('datas','w')
#datafile.write('title   images[0]   jianjie activityTab ')
import random
addDataUrl = 'http://47.102.205.71:3000/addActivity'
datas = []
for item in datamap['items']:
    insertData = {
        "title": "",  # 标题，name
        "images[0]": "",  # 封面，//字符串，图片链接  cover
        "jianjie": "",  # 简介，   sellingPoints
        "activityTab": "",  # 活动标签，benifits
        "fateDay": "",  # 团建天数，days nights
        "tripsNumber": "",  # 出行人数，minBooking-maxBooking
        "averagePrice": "",  # 人均价格，price
        "foodIndex": "",  # 餐饮指数，recommendedIndexs
        "stayIndex": "",  # 住宿指数，recommendedIndexs
        "leagueIndex": "",  # 团建指数，recommendedIndexs
        "powerIndex": "",  # 团建指数，recommendedIndexs
        "detail": "",  # 富文本详情，
        "leaguePlay": "",  # 团建玩法，playings
        "type": "",  # 团建类型 type
        "moneySort": "",  # 价格排序标识，
        "swiperImages": "",  # 轮播图，#字符串，多张逗号分隔
        "_id": ""
    }
    insertData['title'] = item['name']
    titleImage = downloadImage(item['cover'])
    if titleImage != "":
        insertData['images[0]'] = titleImage
    else:
        insertData['images[0]'] = item['cover']

    insertData["jianjie"] = item['sellingPoints']
    for benifit in item['benifits']:
        insertData['activityTab'] += benifit
        insertData['activityTab'] += ','
    insertData["activityTab"] = insertData["activityTab"][0:len(
        insertData["activityTab"])-1]
    insertData["fateDay"] = f"{item['days']}天{item['nights']}晚"
    insertData["tripsNumber"] = f"{item['minBooking']}-{item['maxBooking']}"
    insertData["averagePrice"] = item['price']
    #recommendedIndexsMap = json.loads(item['recommendedIndexs'])
    if len(item['recommendedIndexs']) > 4:
        insertData["foodIndex"] =  str(item['recommendedIndexs'][0]['value']) if item['recommendedIndexs'][0]['value'] != None  else str(random.randint(3,5))
        insertData["stayIndex"] = str(item['recommendedIndexs'][1]['value']) if item['recommendedIndexs'][1]['value'] != None  else str(random.randint(3,5))
        insertData["leagueIndex"] = str(item['recommendedIndexs'][2]['value']) if item['recommendedIndexs'][2]['value'] != None  else str(random.randint(3,5))
        insertData["powerIndex"] = str(item['recommendedIndexs'][3]['value']) if item['recommendedIndexs'][3]['value'] != None  else str(random.randint(3,5))
    for play in item['playings']:
        insertData["leaguePlay"] += play
        insertData["leaguePlay"] += ','
    insertData["leaguePlay"] = insertData["leaguePlay"][0:len(
        insertData["leaguePlay"])-1]
    insertData["type"] = item['type']
    insertData["_id"] = item['_id']
    datas.append(insertData)
    #dataret = requests.post(url=addDataUrl, data=insertData)
    # print(dataret.content.decode('utf-8'))
file = open('test.html', 'w', encoding="utf-8")

# from selenium.webdriver.chrome.options import Options
# chrome_options =Options()
# chrome_options.add_argument('--headless')
# webdriver.driver = webdriver.Chrome(options=chrome_options)
cssfile = open('index.html', 'r', encoding="utf-8")
cssdatas = cssfile.read()


br = webdriver.Chrome()
nums = 1
for data in datas:
    swiperUrl = f"https://www.damaotuanjian.com/detail?id={data['_id']}"
    br.get(swiperUrl)
    height = br.execute_script("return action=document.body.scrollHeight")
    #将滚动条调到页面底部
    for i in range(0, height, 500):
        br.execute_script('window.scrollTo(0, {})'.format(i))
        sleep(0.5)

    srcs = br.find_elements_by_xpath(
        "//div[@class='swiper-wrapper']/div[@class='swiper-slide']/div/img")
    for src in srcs:
        imagUrl = src.get_attribute("src")
        trueUrl = downloadImage(imagUrl)
        if trueUrl != "":
            data['swiperImages'] += trueUrl
            data['swiperImages'] += ','

    data["swiperImages"] = data["swiperImages"][0:len(data["swiperImages"])-1]


    content = br.find_element_by_class_name(
        "detail-content-border").get_attribute("outerHTML")
    images = br.find_elements_by_tag_name("img")
    for img in images:
        #data-src = img.get_attribute("data-src")
        #print(img.get_attribute("data-src"))
        url = img.get_attribute("src")
        if img.get_attribute("src") != None:
            htmlImage = downloadImage(img.get_attribute("src"))
            if htmlImage != "":
                content = content.replace(img.get_attribute("src"), htmlImage)

    try:
        data['detail'] = transform(content+cssdatas)
        data.pop('_id')
        dataret = requests.post(url=addDataUrl, data=data)
        
    except:
        numFile = open('errolrog','a',encoding="utf-8")
        numFile.write(str(nums) + data['title'] + '\n')
        print(nums)
    else:
        nums = nums + 1
    # print(dataret.content.decode('utf-8'))

print(f'wiret data {nums}')
