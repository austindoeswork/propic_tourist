# upload.py
import getpass
import time

photoDir = "/home/adw/propic_tourist/images/"

ghUser = input("Username: ")
ghPw = getpass.getpass()

from selenium import webdriver
driver = webdriver.Firefox()
# driver = webdriver.PhantomJS()
driver.set_window_size(1120, 550) # necessary?

driver.get("https://github.com/login")
time.sleep(1)
field = driver.find_element_by_css_selector('#login_field')
field .send_keys(ghUser)
field = driver.find_element_by_css_selector('#password')
field .send_keys(ghPw)
time.sleep(1)
driver.find_element_by_css_selector('[value="Sign in"]').click()
time.sleep(1)
driver.get("https://github.com/settings/profile")
fileinput = driver.find_element_by_css_selector('#upload-profile-picture')
pdir = photoDir + "asdf.png" 
fileinput.send_keys(pdir);
time.sleep(1)
driver.find_element_by_css_selector('[name="op"]').click()
time.sleep(5)
# driver.find_element_by_id('header-search-scope').send_keys("realpython")
# driver.find_element_by_id("search_button_homepage").click()
# print (driver.current_url)
driver.quit()