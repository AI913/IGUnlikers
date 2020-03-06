from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from time import sleep
from secrets import username, pw
from pandas import DataFrame
import pandas as pd
import sys
import os

class InstaBot:
    def __init__(self, username, pw):
        self.driver = webdriver.Chrome()
        self.username = username
        self.driver.get("https://instagram.com")
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(text(), 'Log in')]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(pw)
        self.driver.find_element_by_xpath('//button[@type="submit"]').click()
        sleep(4)
        self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]").click()
        sleep(2)
        self.driver.find_element_by_xpath("//a[contains(@href,'/{}')]".format(self.username)).click()
        sleep(3)

    #In case you want to do something with the "Followers"
    def get_followers(self): 
        self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]").click()
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        return names

    def get_following(self):
        self.driver.find_element_by_xpath("//a[contains(@href,'/following')]").click()
        sleep(2)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[4]/div/div[2]")
        last_ht, ht = 0, 1
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            ht = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
        links = scroll_box.find_elements_by_tag_name('a')
        names = [name.text for name in links if name.text != '']
        return names

    def get_likers(self):
        sleep(2)
        #show "others"
        self.driver.find_element_by_xpath("/html/body/div[4]/div[2]/div/article/div[2]/section[2]/div/div[2]/button").click()
        likers = self._get_names()
        print(likers)
        #close pop up
        self.driver.find_element_by_xpath("/html/body/div[5]/div/div[1]/div/div[2]/button").click()
        # next photo
        self.driver.find_element_by_tag_name("html").send_keys(Keys.ARROW_RIGHT)
        return(likers)

    def total_likers(self, n):
        likers = []
        while n > 0:
            liker_cur = my_bot.get_likers()
            n -= 1
            [likers.append(liker) for liker in liker_cur if liker not in likers]
        else:
            return likers

    def open_1st_pic(self):
        self.driver.find_element_by_xpath("/html/body/div[4]/div/div[1]/div/div[2]/button").click()
        self.driver.find_element_by_class_name("_9AhH0").click()

    def _get_names(self):
        sleep(1)
        scroll_box = self.driver.find_element_by_xpath("/html/body/div[5]/div/div[2]/div")
        last_ht, ht = 0, 1
        names = []
        while last_ht != ht:
            last_ht = ht
            sleep(1)
            links = scroll_box.find_elements_by_tag_name('a')
            newname = [name.text for name in links if name.text != '']
            [names.append(name) for name in newname if name not in names]
            ht = self.driver.execute_script("""arguments[0].scrollTo(0, arguments[0].scrollHeight); return arguments[0].scrollHeight;""", scroll_box)

        return names
        
my_bot = InstaBot(username, pw)
sleep(2)
following = my_bot.get_following()
sleep(1)
my_bot.open_1st_pic()
sleep(1)

#people who have liked at least one of my past n posts
total_likers = my_bot.total_likers(int(sys.argv[1]))
print(total_likers)
unlikers = [user for user in following if user not in total_likers]
print(unlikers)
df = DataFrame(unlikers)
export_excel = df.to_excel (r'/Users/chiuyiuwah/Data/unlikers.xlsx', index = None, header=True) #Don't forget to add '.xlsx' at the end of the path
os.system("open -a '/Applications/Microsoft Excel.app' '/Users/chiuyiuwah/Data/unlikers.xlsx'")