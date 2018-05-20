from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from scrapy.selector import Selector

from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
prefs = {
    'profile.default._content_setting_values':{
        'images': 2
    }
}
chrome_options.add_experimental_option('prefs', prefs)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://www.baidu.com')
t_seletor = Selector(text=browser.page_source)
print(t_seletor.css('#u1 a.mnav::text').extract())

