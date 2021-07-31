try:
    hidden = ""
    with open("password.txt", "r") as f:
        hidden = f.readline()

    PATH = "/home/cyborg/Downloads/chromedriver"
    import mysql.connector
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.action_chains import ActionChains
    import json

    service = Service(PATH)
    

    import requests
    from bs4 import BeautifulSoup

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}
    mydb = mysql.connector.connect(
        host="localhost",
        user="pythonadmin",
        password="password1234",
        database="mysql"
    )
    cursorObj = mydb.cursor()
    # cursorObj.execute("CREATE DATABASE user")


    def check_user(func):
        print("Checking users credentials...")

        def check(*args, **kwargs):
            # print(args[0])
            try:
                cursorObj.execute(
                "SELECT * FROM user__ WHERE username = %s", (args[0],))
                data = cursorObj.fetchall()
                # print(data)
                if len(data) == 0:
                    print("\n\t\t\tInvalid Credentials!")
                    return 1
                else:
                    print("Credentials verified!")
                    cursorObj.execute("SELECT scrape_done FROM user__ WHERE username = %s", (args[0],))
                    data = cursorObj.fetchall()
                    if data[0][0] == 1:
                        cursorObj.execute("SELECT name, work, city,favs FROM user__ WHERE username = %s", (args[0],))
                        scrap = cursorObj.fetchall()
                        obj = ""
                        for row in scrap:
                            if len(json.loads(row[1])) == 0:
                                if row[2] != "" :
                                    obj = Person(name=row[0], city=row[2], fav=json.loads(row[3]))
                                else:
                                    obj = Person(name=row[0], fav=json.loads(row[3]))
                            else :
                                if row[2] != "":
                                    obj = Person(name=row[0],work=json.loads(row[1]) ,city=row[2], fav=json.loads(row[3]))
                                else:
                                    obj = Person(name=row[0],work=json.loads(row[1]), fav=json.loads(row[3]))
                        return obj
                    else:
                        return_val = func(args[0])
                        return return_val
            except Exception as e:
                print(e)
        return check


    class Person:
        def __init__(self, name, fav = None,work=None, city="Roorkee"):
            if(work != None):
                self.work = work
            self.name = name
            self.city = city
            if fav != None:
                if(len(fav) != 0):
                    self.fav = fav
                else:
                    self.fav= None
            else:
                self.fav = None
    @ check_user
    def scrape(username):
        try:
            obj = ""
            req = requests.get("https://m.facebook.com/"+username+"/about", headers=headers)
            
            soup = BeautifulSoup(req.content, "html5lib")

            # Scraping name

            strip = len(" | Facebook")
            strip = strip - 2*strip
            user_name = soup.title.get_text()[:strip]

            # Scraping work

            str_work = soup.body.find_all('header')
            string1 = "कार्य"
            
            work_header = ""
            for i in range(len(str_work)):
                if (str_work[i].get_text() == string1):
                    work_header = str_work[i]
                    break

            work_prep_divs = work_header.next_sibling.contents
            work = []
            for item in work_prep_divs:
                work.append(list(item.strings))
            
            # Scraping city

            str_city = "यहाँ रह चुके हैं"
            city_header = soup.find(lambda tag: tag.name == "header" and str_city in tag.text)
            user_city = (city_header.parent.find('h4').get_text())

            driver = webdriver.Chrome(service=service)
            actions = ActionChains(driver)
            driver.get("https://m.facebook.com/")
            driver.find_element_by_name('email').send_keys("conquerorpk@gmail.com")
            driver.find_element_by_name('pass').send_keys(hidden)
            driver.find_element_by_name('login').click()


            # ****Favorites/Likes****

            time.sleep(5) # working on this using drivers
            driver.find_element_by_tag_name('a').click()
            time.sleep(5)

            driver.execute_script("window.open('');")
            driver.switch_to.window(driver.window_handles[1])

            
            driver.get("https://m.facebook.com/"+username+"/about")
            time.sleep(5)
            
            
            # like_div = driver.find_element_by_id("my-id")
            SCROLL_PAUSE_TIME = 1
            favs = []
            # Get scroll height
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                # Scroll down to bottom
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)
                try:
                    like_div = driver.find_element(By.XPATH , '/html/body/div[1]/div[1]/div[4]/div/div[1]/div/div[2]/div[11]/div/div/div/div/header/div/div[3]/a').click()
                    time.sleep(3)
                    all_likes = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[4]/div/div/div/div/div/div[1]/div/header/div/div[3]/a').click()
                    time.sleep(2)
                    break

                except Exception as e:
                    # Calculate new scroll height and compare with last scroll height
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        print(e)
                        break
                    last_height = new_height
            
            for span in driver.find_elements(By.XPATH, '/html/body/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div/div[1]/div[*]/div/span'):
                favs.append(span.text)

            for span in driver.find_elements(By.XPATH, '/html/body/div[1]/div[1]/div[4]/div/div/div/div/div/div/div/div/div[2]/div[*]/div/span'):
                favs.append(span.text)
            
            json_favs = json.dumps(favs)
            
            # ****Creating Person :) ****
            
            if len(work) == 0:
                if user_city != "" :
                    obj = Person(name=user_name, city=user_city, fav=favs)
                else:
                    obj = Person(name=user_name, fav=favs)
            else :
                if user_city != "":
                    obj = Person(name=user_name,work=work ,city=user_city, fav=favs)
                else:
                    obj = Person(name=user_name,work=work, fav=favs)
            
            json_work = json.dumps(work)
            bool = True
            
            cursorObj.execute("UPDATE user__ SET scrape_done = %s, name=%s,work=%s,city=%s,favs=%s WHERE username=%s", (bool, obj.name, json_work, obj.city, json_favs ,username))
            mydb.commit()

            return obj
        except Exception as e:
            print("Can't scrape data: {}".format(e))
            # driver.quit

    
    user = input("Enter your Facebook username: ")
    user_Fobj = scrape(user)
    # print(user_Fobj)
    if user_Fobj == 1:
        exit()
    else:
        print(f'\n\nWelcome {user_Fobj.name}\n\n')
        i = 1
        for item in user_Fobj.work:
            print(f'{i}) {item[0]},{item[1]}')
            i += 1
        while True:
            print("Press f to view your favorites!")
            print("Press w to view your work profile!")
            print("Press c to see your city!")
            print("Press q to exit!")
            a = input()
            if a == 'q':
                exit()
            elif a == 'f':
                if user_Fobj.fav != None:
                    print(user_Fobj.fav)
                else:
                    print("No favorites!")
            elif a == 'c':
                print("Your current city is {}".format(user_Fobj.city))
            elif a == 'w':
                if user_Fobj.work == None:
                    print("Work Profile not modified")
                else:
                    i = 1
                    for item in user_Fobj.work:
                        print(f'{i}) {item[0]},{item[1]}')
                        i += 1
            else:
                print("\nEnter a valid key!!\n\n\n")

except Exception as e:
    print(e)