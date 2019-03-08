#import necessary packages
from selenium       import webdriver
from urllib.request import urlretrieve
from time           import sleep
from getpass        import getpass
import os
import json
import re
import sys
import platform
import argparse
import requests
from selenium.webdriver.common.keys       import Keys

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", metavar="", help="User username")
    parser.add_argument("-p", "--password", metavar="", help="User password")
    
    global args 
    args = parser.parse_args()

    
#configure json file
def create_config_if_not_exist():
    if not os.path.isfile("config.json"):
        try:
            data = {"username" : "", "password" : ""}
            text = json.dumps(data)
            with open("config.json", "w") as file:
                file.write(text)
        except:
            print("Config file could not be created!")
            return

def read_json():
    if not os.path.isfile("config.json"):
        return None
    else:
        try:
            with open("config.json") as data_file:
                data = json.load(data_file)
            return data
        except:
            return None

        
#fetching the user name
def get_username():
    if args.username:
        return args.username
    else:
        config = read_json()
        if config and config["username"] != "":
            return config["username"]
        else:
            return input("Username : ")

        
#fetching the user password
def get_password():
    if args.password:
        return args.password
    else:
        config = read_json()
        if config and config["password"] != "":
            return config["password"]
        else:
            return getpass("Password : ")

#getting path to config file
def get_path():
    if args.path:
        return args.path
    else:
        config = read_json()
        if config and config["path"] != "":
            return config["path"]
        else:
            return "pictures"
#choose driver (using selenium) modify if require different browser(Firefox or phantomJs)
def choose_driver():
        driver = webdriver.Chrome("C:/Users/a/Downloads/chromedriver_win32/chromedriver.exe")
        print("Driver : Chrome")
        return driver
    
#signing to user account
def signing_in(driver):
    username = get_username()
    password = get_password()
    driver.get("https://www.instagram.com/accounts/login")
    sleep(2)
    print("a")
    usernameinput = driver.find_element_by_name("username")
    print("b")
    passwordinput = driver.find_element_by_name("password")
    usernameinput.send_keys(username)
    passwordinput.send_keys(password)
    passwordinput.send_keys(Keys.ENTER)
    user_id = getID(username)
    sleep(2)
    
#checking the valid user_id
def getID(username):    
    url = "https://www.instagram.com/{}"
    r = requests.get(url.format(username))
    html = r.text
    if r.ok:
        return re.findall('"id":"(.*?)",', html)[0]

    else:
        print("Invalid username")
        sys.exit()

        
#fetching userdp
def fetchDP(userID):
    url = "https://i.instagram.com/api/v1/users/{}/info/"

    r = requests.get(url.format(userID))

    if r.ok:
        data = r.json()
        return data['user']['hd_profile_pic_url_info']['url']

    else:
        print("--Can't find user--")
        
        

def followWithUsername(driver, username):

        driver.get('https://www.instagram.com/' + username + '/')
        sleep(2)
        url = "https://www.instagram.com/{}"
        r = requests.get(url.format(username))

        html = r.text

        if r.ok:
            followButton = driver.find_element_by_css_selector('button')
            if (followButton.text != 'Following'):
                followButton.click()
                sleep(2)
            else:
                print("You are already following this user")
            

        else:
             print("---Invalid username---")
             


def unfollowWithUsername(driver, username):
          driver.get('https://www.instagram.com/' + username + '/')
          sleep(2)
          url = "https://www.instagram.com/{}"
          r = requests.get(url.format(username))
          html = r.text
          if r.ok:
              followButton = driver.find_element_by_css_selector('button')
              if (followButton.text == 'Following'):
                  followButton.click()
                  sleep(2)
                  confirmButton = driver.find_element_by_xpath('//button[text() = "Unfollow"]')
                  confirmButton.click()
              else:
                  print("You are not following this user")
          else:
                     print("---Invalid username---")
                     



def core():
    print("------AUTO_INSTA------")
    parse_args()
    create_config_if_not_exist()
    driver = choose_driver()
    signing_in(driver)
   
    while True :
        i = int(input("Want to 1)Follow  \ 2)Unfollow \3) Download the dp user[ 1/ 2 / 3]"))
        if i==1:
            user = input("username")
            followWithUsername(driver,user)
        elif i==2:
            user = input("username")
            unfollowWithUsername(driver,user)
        elif i==3:
             user = input("username")
             user_id = getID(user)
             file_url = fetchDP(user_id)
             fname = user + ".jpg"
             r = requests.get(file_url, stream=True)
             if r.ok:
                 with open(fname, 'wb') as f:
                     f.write(r.content)
                     print(" Downloaded:{}".format(fname))
             else:
                 print("OOPS!!No Internet Connection")
        else:
            print("---Wrong Choice.. Try Again---")

        ans = input("Use again(y/N)? : ")
        if ans == "N" or ans == "n":
             break

   
    
    input("---Press any key to exit---")
    driver.close()
    print(" ****Closed.****")
    
if __name__ == "__main__":
    core()
        
    
    
