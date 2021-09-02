import requests
from lxml import etree
from lxml import html
import json


def removeItem(src):
    pdDelItems = src.xpath("//div[@class='inner-detail-plan']")#作为根节点的创建，会自动补充上层<html><body>
    if len(pdDelItems)>0:
        for deleteItem in pdDelItems:
            print('删除节点:',etree.tostring(deleteItem,encoding="utf-8",pretty_print=True,method="html").decode())
            parentItem = deleteItem.getparent() 
            parentItem.remove(deleteItem)

errorsID = []

for i in range(715,716):
    url = f"http://47.102.205.71:3000/queryActivityDetail?id={i}"
    try:
        response = requests.get(url=url)
        jsonMap = json.loads(response.content.decode('utf-8'))
        pd = etree.HTML(jsonMap['data'][0]['detail'])
    except:
        errorfile = open('errorlog','a', encoding('utf-8'))
        errorfile.write(f"{i} write detail failed \n")
        errorsID.append(i)
    else:
        removeItem(pd)
        htmlfilesave = open('test6.html','w', encoding='utf-8')
        htmlfilesave.write(etree.tostring(pd,encoding="utf-8",pretty_print=True,method="html").decode())