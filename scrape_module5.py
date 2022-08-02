def change(name):
    # substitute for the weird words
    table = str.maketrans({
        '\u3000': ' ',
        ' ': '',
        '\t': ''
    })
    name = name.translate(table)
    
    # full-width to half-width
    name = name.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))
    
    return name

# import the modules and libraries
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import re


def scrape_convenience(search_word, lists_convenient_store, english_word):
    # https://chromedriver.chromium.org/downloads
    # version 103r"C:\Users\81808\document1\chromedriver.exe"
    # define the driver
    # please specify your driver
    driver = webdriver.Chrome(r"C:\Users\81808\document1\chromedriver.exe")
    sleep(2)


    # define all prefectures in Japan
    # Japanese words mean each prefecture in Japan like Tokyo, Kyoto
    prefectures = ['北海道','青森県','岩手県','宮城県','秋田県','山形県','福島県','茨城県','栃木県',
                '群馬県','埼玉県', '千葉県','東京都','神奈川県','新潟県','富山県','石川県','福井県',
                '山梨県','長野県','岐阜県','静岡県','愛知県','三重県','滋賀県','京都府','大阪府','兵庫県',
                '奈良県','和歌山県','鳥取県','島根県','岡山県','広島県','山口県','徳島県','香川県','愛媛県',
                '高知県','福岡県','佐賀県','長崎県','熊本県','大分県','宮崎県','鹿児島県','沖縄県']



    # scrape the name, latitude, and longitude of convenient store in MapFan

    # loop for each prefecture
    for prefecture in prefectures:
        
        # go to the MapFan site
        driver.get('https://mapfan.com/map/spots/search?c=35.681195934673795,139.7672311841094,12&s=std,pc,ja&p=none')
        sleep(1)        

        # search the search bar
        # enter the search word
        # get the result of the search
        search_input = driver.find_element_by_xpath('/html/body/mf-root/div/mat-sidenav-container/mat-sidenav-content/mf-map-page-map/mat-sidenav-container/mat-sidenav-content/div/div[1]/mf-map-page-search/div/form/mat-toolbar/mat-toolbar-row/mf-suggest-field/mat-form-field/div/div[1]/div[3]/input')
        search_input.send_keys("{} {}".format(search_word, prefecture))
        search_input.send_keys(Keys.ENTER)


        # loop for name list
        for elemh4 in driver.find_elements_by_xpath('//h4'):
            elem = elemh4.find_element_by_xpath("../../..")
            
            # click one of the componenets in the list
            elem.click()
            sleep(1)
            
            # get the url of the component
            s = driver.current_url
            list = []
            
            # search latitude and longitude by regular expression
            match = re.search(r'c=(\d+.\d+),(\d+.\d+)', s)
            
            # get latitude and longitude
            try:
                latitude = match.group(1)
                longitude = match.group(2)
            except: 
                pass
            
            # get the name of the component
            name = elemh4.text
            
            # chage to half-width and alter wierd words
            name = change(name)
            
                
            # find the IKEA by regular expression
            if re.compile(r"^{}.+?".format(search_word)).search(name):
                
                # append the name, latitude, and longitude
                name = name.replace(search_word, english_word, 1)
                            
                list.append(name)
                list.append(latitude)
                list.append(longitude)
                lists_convenient_store.append(list)
                
    # terminate the driver
    driver.close()
            
            
            
            
def show_lists(lists_convenient_store):        
    # show the lists 
    for i in range(len(lists_convenient_store)):
        print(lists_convenient_store[i])




def write_elem(lists, filename):
    filename += ".csv"
    filename = "CSV/" + filename
    for i in range(len(lists)):    
        with open(filename, "a", encoding="UTF-8") as f:
            f.write("{}, {}, {}\n".format(lists[i][0], lists[i][1], lists[i][2]))