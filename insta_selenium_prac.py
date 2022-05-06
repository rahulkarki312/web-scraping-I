import os

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, sys
from pathlib import Path
#  login to instagram and follow/like some account


browser = webdriver.Chrome()

browser.get("https://www.instagram.com/")
browser.implicitly_wait(5)

# login

username = "user12_"        # enter your username/ use a fake account
pw = "combatboots98"         # enter password

loginUsernameElem = browser.find_element_by_xpath('''//*[@id="loginForm"]/div/div[1]/div/label/input''')
passwordElem = browser.find_element_by_xpath('''//*[@id="loginForm"]/div/div[2]/div/label/input''')
loginBtn = browser.find_element_by_xpath('''//*[@id="loginForm"]/div/div[3]/button''')

loginUsernameElem.send_keys(username)
passwordElem.send_keys(pw)
loginBtn.click()
# logged in

# search profile
searchProfile = browser.find_element_by_xpath('''//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/input''')
searchAcc = "shraddha_bohora"     # instagram account name to scrape (must be public account)
# sulav_baral_58 44 posts
searchProfile.send_keys(searchAcc)
searchProfile.submit

topmostProfile = browser.find_element_by_xpath('''//*[@id="react-root"]/section/nav/div[2]/div/div/div[2]/div[3]/div/div[2]/div/div[1]/a''')
# print(topmostProfile.get_attribute("href"))  # profile selected
topmostProfile.click()
# opened the searched profile

# OBSERVE - the element with class name 'className' is accessed by :
#   element.className

e = browser.find_element_by_css_selector('#react-root > section > main > div > div._2z6nI')
allPostsElem = e.find_element_by_css_selector("article.ySN3v")  # contains the article(element) with all the posts insta
htmlElem = browser.find_element_by_tag_name('html')

# TODO 1.first find all the post divs in the page (currently only 4 divs accessed)  2. find out how many keystrokes it takes to load a new row

imgUrls = []

# OBSERVE - the element with class name 'className' is accessed by :
#   element.className

try:
    # postsCountElem = browser.find_element_by_css_selector('span.g47SY')
    # postsCount = postsCountElem.text
    postsCount = 46  # enter number of posts by the user
    rowCount = 0
    postNum = 0

    while True:
        for j in range(10):
            htmlElem.send_keys(Keys.DOWN)
        for row in allPostsElem.find_elements_by_css_selector('div.Nnq7C'):     # div with all posts with class = 'Nnq7C' when the page loads once
            for post in row.find_elements_by_css_selector('div.v1Nh3'):         # individual post in a row with class v1Nh3
                photoElem = post.find_element_by_css_selector("img.FFVAD")        # photo elem with class name FFVAD
                imgUrl = photoElem.get_attribute('src')

                if imgUrl not in imgUrls:
                    imgUrls.append(photoElem.get_attribute('src'))
        if len(imgUrls) == postsCount:
            break
    print("in list: \n")

    for i, u in enumerate(imgUrls):
        print(u+" "+ str(i))

    print("Total URLS fetched: " + str(len(imgUrls)))

#     TODO download images
    folderName = searchAcc + "-fetched"
    os.makedirs(folderName)

    path = Path(folderName)
    for i, imgUrl in enumerate(imgUrls):
        imgName = str(i) + ".jpeg"
        file = open(path/Path(imgName), 'wb')
        res = requests.get(imgUrl)
        res.raise_for_status()

        for chunk in res.iter_content(100000):
            file.write(chunk)
        file.close()


except :
    print("ERR:\n", sys.exc_info()[0], sys.exc_info()[1])

finally :
    # print("err")
    time.sleep(60)
    browser.quit()
#     executed no matter what

