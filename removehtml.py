import requests
from lxml import etree
from lxml import html
import json

postdata = {
"id": 0,
"title": "",
"images[0]": "",
"jianjie": "",
"activityTab": "",
"fateDay": "",
"tripsNumber": "",
"averagePrice": "",
"foodIndex": "",
"stayIndex": "",
"leagueIndex": "",
"powerIndex": "",
"detail": "",
"leaguePlay": "",
"type": "",
"moneySort":0, 
"swiperImages":""
}

header = {
  'Connection': 'keep-alive',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
  'Accept': 'application/json, text/plain, */*',
  'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
  #'Content-Type': 'application/x-www-form-urlencoded',
  'Origin': 'http://47.102.205.71:3000',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cookie': 'SHRIOSESSIONID=0d62f6d8-b988-4641-9ba8-4498a598bdf7; vue_admin_template_token=admin-token; request_token=t1sbekpirNodiwWrEFGcfgdnq8BRD3lIQqAhjLQXMbXbRJ5I; bt_config=%5Bobject%20Object%5D; order=id%20desc; backup_path=C%3A/backup'
}

def removeItem(src):
    pdDelItems = src.xpath("//div[@class='inner-detail-plan']")#作为根节点的创建，会自动补充上层<html><body>
    if len(pdDelItems) > 0:
        for deleteItem in pdDelItems:
            print('删除节点:',etree.tostring(deleteItem,encoding="utf-8",pretty_print=True,method="html").decode())
            parentItem = deleteItem.getparent()
            parentItem.remove(deleteItem)
    styleItems = src.xpath("//div[@class='inner-detail-fee-border-left']")
    if len(styleItems) > 0:
        for item in styleItems:
            item.attrib['style'] = "padding: 17px; border-right: 2px solid #fff;"
            item.attrib['data-mce-style'] = "padding: 17px; border-right: 2px solid #fff;"

errorsID = []

# postdata = {
#     "activity_tab": "null",
#     "average_price": 0,
#     "create_time": "2021-9-3",
#     "detail": "",
#     "fate_day": ""
#     "food_index": "",
#     "id": "203"
#     "images": "null"
#     "jianjie": "华东第一漂；“逃离”烈日炎炎焦躁的市区，清幽的峡谷参天的绿荫、全程是清澈冰凉的享受。",
#     "league_index": "",
#     "league_play": "",
#     "money_sort": "",
#     "power_index": "",
#     "stay_index": "",
#     "swiper_images": "",
#     "title": "【“漂”离办公室 “流”走烈日炎炎】安吉仙龙峡漂流+溯溪2日清凉团建",
#     "trips_number": "",
#     "type": "旅行团建"
# }


for i in range(205,805):
    url = f"http://47.102.205.71:3000/queryActivityDetail?id={i}"
    try:
        response = requests.get(url=url)
        jsonMap = json.loads(response.content.decode('utf-8'))
        pd = etree.HTML(jsonMap['data'][0]['detail'])
    except:
        errorsID.append(i)
        continue
    else:
        removeItem(pd)
        htmlfilesave = open('test6.html','w', encoding='utf-8')
        formatData = etree.tostring(pd,encoding="utf-8",method="html").decode()
        copyPostData = jsonMap['data'][0]
        postdata ={}
        postdata['id'] = int(copyPostData['id'])
        postdata['title'] = copyPostData['title']
        postdata['images[0]']=copyPostData['images']
        postdata['jianjie'] = copyPostData['jianjie']
        postdata['detail'] = formatData
        postdata['activityTab'] = copyPostData['activity_tab']
        postdata['fateDay'] = copyPostData['fate_day']
        postdata['tripsNumber'] = copyPostData['trips_number']
        postdata['averagePrice'] = copyPostData['average_price']
        postdata['foodIndex'] = copyPostData['food_index']
        postdata['stayIndex'] = copyPostData['stay_index']
        postdata['leagueIndex'] = copyPostData['league_index']
        postdata['powerIndex'] = copyPostData['power_index']
        postdata['leaguePlay'] = copyPostData['league_play']
        postdata['type'] = copyPostData['type']
        postdata['moneySort']=int(copyPostData['money_sort'])
        postdata['swiperImages'] = copyPostData['swiper_images']
        removeItemUrl = 'http://47.102.205.71:3000/updateActivity'

    #header['Content-Length'] = str(len(str(postdata)))
    ret = requests.post(url=removeItemUrl, headers=header, json=postdata)
    #ret = requests.request("POST", url, headers=header, data=postdata)
    removeData = json.loads(ret.content.decode('utf-8'))
    if removeData['code'] != 20000:
        errorsID.append(i)
        continue
    print(f"removeItem success {i}")
    htmlfilesave.write(formatData)

errorfile = open('errorlog','a', encoding='utf-8')
for i in errorsID:
     errorfile.write(f"{i} write detail failed \n")
