#import pymongo
from selenium import webdriver
from selenium.common.exceptions import  TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
from urllib.parse import quote


browser = webdriver.Chrome()
wait = WebDriverWait(browser,12)

#MONGO_URL = 'localhost'
#MONGO_DB = 'taobao'  #指定数据库
#MONGO_COLLECTION = 'products'
#client = pymongo.MongoClient(MONGO_URL)
#db = client[MONGO_DB]

KEYWORD = 'ipad'

def index_page(page):  #获得商品列表
    print('正在爬取第',page,'页')
    try:
        url = 'https://s.taobao.com/search?q='+ quote(KEYWORD)
        browser.get(url)
        if page > 1:
            input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
            submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager div.form > span.btn.J_Submit')))
            input.clear()
            input.send_keys(page)
            submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager li.item.active > span'),str(page)))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.m-itemlist .items .item')))
        get_products()
    except TimeoutException:
        index_page(page)

def get_products():   #提取商品数据
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image':item.find('.pic .img').attr('data-src'),   #商品图片
            'price':item.find('.price').text(),          #价格
            'deal':item.find('.deal-cnt').text(),        #付款人数
            'title':item.find('.title').text(),          #商品标题
            'shop':item.find('.shop').text(),            #店铺名称
            'location':item.find('.location').text()     #地址
        }
        print(product)
        #save_to_mongo(product)

'''def save_to_mongo(result):
    try:
        if db[MONGO_COLLECTION].insert(result):
            print("存储到MongoDB成功！")
    except Exception:
        print("存储到MongoDB失败！")'''

def main():
    for i in range(1,3):
         index_page(i)
    browser.close()

if __name__ == '__main__':
    main()
