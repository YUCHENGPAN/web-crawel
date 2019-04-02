import requests
from pyquery import PyQuery as pq
import pymongo
import time

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

}
def get_link(url):

    res = requests.get(url,headers=headers).text
    doc = pq(res)
    items = doc('.pic_list.clearfix li').items()
    for item in items:
        link = item.find('a').attr('href')
        #print(link)
        get_info(link)

def get_info(link):
    res = requests.get(link, headers=headers).text
    doc = pq(res)
    title = doc('.pho_info h4 em').text().strip()
    address = doc('.pho_info p').attr('title')
    scole = doc('.top_bar_w2.border_right_none').text()
    price = doc('.day_l').text() + doc('.day_r').text()
    house_owner = doc('.lorder_name').text()
    gender = doc('.lorder_name').siblings().attr('class')
    data = {
        'title':title,
        'address':address,
        'scole':scole,
        'price':price,
        'house_owner':house_owner,
        'gender':judge_sex(gender)
    }
    #print(data)
    #save_mongodb(data)
    save_to_csv(data)



def judge_sex(gender):
    if gender == 'member_girl_ico':
        return '女'
    else:
        return '男'


def save_mongodb(data):
    client = pymongo.MongoClient(host='localhost',port=27017)
    db = client.shuju
    collection = db.xiaozhu
    if collection.insert_one(data):
        print('存储至数据库成功！')
    else:
        print('存储失败！')










def main():
    urls = ('http://sh.xiaozhu.com/search-duanzufang-p{}-0/'.format(i) for i in range(0, 11))
    for url in urls:
        #print(url)
        get_link(url)

if __name__ == '__main__':
    main()
    time.sleep(2)
    #get_link('http://sh.xiaozhu.com/search-duanzufang-p0-0/')
    #get_info('http://sh.xiaozhu.com/fangzi/26594285803.html')
