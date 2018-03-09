from selenium import webdriver
import requests,time,random,os
from lxml import etree
'''
    功  能：爬取妹子图中颜值控中的所有妹子照片
    技  术：使用了selenium模块中的 webdriver,安装了PhantomJS初始化浏览器（无界面的浏览器），
            我这里是安装的Windows版的还有requests请求模块,time时间模块,random随机模块,os模块
            还使用了lxml模块中的etree,使用header利用user-agent反反爬手段还有cookie
    返回值：使用webdriver.PhantomJS()返回browser值,browser.get()发起http请求
            etree.HTML(browser.page_source)获取网页的代码，然后利用xpath解析每一个妹子
            的地址在遍历一次向每一个地址发出http请求，再次解析获取每一个图片的地址和文件夹的名字，
            判断文件夹是否已经存在，不存在就创建文件夹，然后使用time.sleep()进行睡眠，利用随机模块
            选择睡眠的时间，最后在对图片的最终地址发出http请求，把图片保存保存在相应的的位置
            
'''
#副
def getPic(html_small):
    html_small_urls = html_small.xpath('//div[@id="picture"]/p/img/@src')
    name = html_small.xpath('//div[@class="metaRight"]/h2/a/text()')[0]
    dirname = 'img'+name
    # 判断文件夹是否存在，不存在就创建文件夹
    if not os.path.exists(dirname):
        os.mkdir('img/'+name)
    print(name)
    # 遍历
    time.sleep(random.choice([1, 1.5, 2, 1.3]))
    for html_small_url in html_small_urls:
        headers = {
            "Host": "nsclick.baidu.com",
            "Connection": "keep-alive",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
            "Referer": "http://www.meizitu.com/a/5575.html",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cookie": "BAIDUID=6DA45F7116292C42806F45BCF2653ECD:FG=1; BIDUPSID=6DA45F7116292C42806F45BCF2653ECD; PSTM=1508920736; __cfduid=dab1e5b9e324d00e14575d73cd318f23b1509975900; MCITY=-131%3A; BDUSS=FBelpMMTZTR3ZSVGtXVlc4YzdvU01vZ1ZmVmxRbXEtaTN4MFJ6fnlvcTFEWnhhQVFBQUFBJCQAAAAAAAAAAAEAAADygixYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALWAdFq1gHRaYn; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=25641_1432_21120_17001_20927; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; PSINO=2; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; userFrom=null"

        }
        #获取图片的名 fname
        fname = html_small_url.split('/')[-1]
        print(fname)
        #对图片最终地址发出http请求
        response = requests.get(html_small_url,headers=headers)
        with open('./img/'+name+'/'+fname,'wb') as f:
            #保存图片
            f.write(response.content)
#主
def picPage():
    #发起http请求
    browser.get('http://www.meizitu.com/a/pure.html')
    #获取网页代码
    html = etree.HTML(browser.page_source)
    #解析字段 获取到的是列表
    name_urls = html.xpath('//div[@class="inWrap"]//ul/li//div[@class="pic"]/a/@href')
    #遍历 把列表中的索引转变成字符串
    for name_url in name_urls:
        name = name_url.split('/')[-1]
        #对每一个妹子的地址发出http请求
        browser.get('http://www.meizitu.com/a/' + name)
        #获取网页代码
        html_small = etree.HTML(browser.page_source)
        #调用函数
        getPic(html_small)

if __name__ == '__main__':
    #初始化一个浏览器
    browser = webdriver.PhantomJS()
    picPage()