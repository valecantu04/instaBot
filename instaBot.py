from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import time
import random
import sys


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()

class instagramBot:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Firefox()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)

        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(2)

        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)

        password_elem = driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)
        time.sleep(2)


    def likePic(self, hashtag):
            driver = self.driver
            driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
            time.sleep(2)

            # gathering photos
            pic_hrefs = []
            for i in range(1, 7):
                try:
                    driver.execute_script(
                        "window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    # get tags
                    hrefs_in_view = driver.find_elements_by_tag_name('a')
                    # finding relevant hrefs
                    hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                    if '.com/p/' in elem.get_attribute('href')]
                    # building list of unique photos
                    [pic_hrefs.append(href)
                    for href in hrefs_in_view if href not in pic_hrefs]
                    # print("Check: pic href length " + str(len(pic_hrefs)))
                except Exception:
                    continue

            # Liking photos
            unique_photos = len(pic_hrefs)
            for pic_href in pic_hrefs:
                driver.get(pic_href)
                time.sleep(2)
                driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);")
                try:
                    time.sleep(random.randint(2, 8))

                    def like_button(): return driver.find_element_by_xpath(
                        '//span[@aria-label="Like"]').click()
                    like_button().click()
                    for second in reversed(range(0, random.randint(18, 28))):
                        print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                        + " | Sleeping " + str(second))
                        time.sleep(1)
                except Exception as e:
                    time.sleep(2)
                unique_photos -= 1

'''Posting a comment doesn't work right now.
    """write comment in text area using lambda function"""
    def write_comment(self, comment_text):
        try:
            comment_button = lambda: self.driver.find_element_by_link_text('Comment')
            comment_button().click()
        except NoSuchElementException:
            pass

        try:
            comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
            comment_box_elem().send_keys('')
            comment_box_elem().clear()
            for letter in comment_text:
                comment_box_elem().send_keys(letter)
                time.sleep((random.randint(1, 7) / 30))

            return comment_box_elem

        except StaleElementReferenceException and NoSuchElementException as e:
            print(e)
            return False

    """actually post a comment"""
    def post_comment(self, comment_text):
        time.sleep(random.randint(1,5))

        comment_box_elem = self.write_comment(comment_text)
        if comment_text in self.driver.page_source:
            comment_box_elem().send_keys(Keys.ENTER)
            try:
                post_button = lambda: self.driver.find_element_by_xpath("//button[@type='Post']")
                post_button().click()
                print('clicked post button')
            except NoSuchElementException:
                pass

        time.sleep(random.randint(4, 6))
        self.driver.refresh()
        if comment_text in self.driver.page_source:
            return True
        return False
        '''

username = "toppostsofreddit"
password = "toppost123"

ig = instagramBot(username, password)
ig.login()

hashtags = ['funny', 'followme', 'follow','instagood', 'instagood', 'followme', 'fashion', 'prank', 'meme', 'memes']

while True:
    try:
        # Choose a random tag from the list of tags
        tag = random.choice(hashtags)
        ig.likePic(tag)
        #ig.post_comment('I love this, this is so funny!')
    except Exception:
        ig.closeBrowser()
        time.sleep(6)
        ig = instagramBot(username, password)
        ig.login()
