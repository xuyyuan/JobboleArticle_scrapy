from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from scrapy.selector import Selector

import time

from selenium.webdriver.chrome.options import Options

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)

# 第一个实例利用scrapy自带的的Selector进行提取数据，因为会比selenium的要快
browser.get('http://www.baidu.com')
t_selector = Selector(text=browser.page_source)
print(t_selector.css('#u1 a.mnav::text').extract())
browser.quit()

#模拟登陆微博;以及通过selenim完成鼠标的一个下滑
browser.get('http://www.weibo.com')
input_username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#loginname')))
input_password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pl_login_form > div > div:nth-child(3) > div.info_list.password > div > input')))
input_username.send_keys('18109442438')
input_password.send_keys('abc456000') # 待填写
submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#pl_login_form > div > div:nth-child(3) > div.info_list.login_btn > a')))
submit.click()
for i in range(5):
    browser.execute_script('window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage')
    #browser实际上是可以直接执行javascrip代码的，而javascript代码是可以控制鼠标下滑的
    time.sleep(10)
browser.quite() #browser.close()也是可以的哦

# 创建无头模式的chromedriver
chrome_options = Options()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://www.baidu.com')
print(browser.page_source)

# 设置chromedriver不加载图片(以下有两种方法)
#方法一
chrome_options = Options()
prefs = {'profile.managed_default_content_settings.images': 2}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://www.taobao.com')
print(browser.page_source)

# 方法二
chrome_options = Options()
prefs = {
    'profile.default_content_setting_values' : {
        'images' : 2
    }
}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(chrome_options = chrome_options)
browser.get("http://www.taobao.com")
print(browser.page_source)

#添加扩展应用的方法
options = Options()
extension_path = '/extension/path'
options.add_extension(extension_path)
driver = webdriver.Chrome(chrome_options = options)

# 增加代理的方法
PROXY = "proxy_host:proxy:port"
options = Options()
desired_capabilities = options.to_capabilities()
desired_capabilities['proxy'] = {
    "httpProxy":PROXY,
    "ftpProxy":PROXY,
    "sslProxy":PROXY,
    "noProxy":None,
    "proxyType":"MANUAL",
    "class":"org.openqa.selenium.Proxy",
    "autodetect":False
}
browser = webdriver.Chrome(desired_capabilities = desired_capabilities)










