from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.proxy import ProxyType
import sys,traceback,time
import queries,const, user_agent
from user_agent import service
import soup_utility
try:
    hidden = ""
    with open("password.txt", "r") as f:
        hidden = f.readline()

    import json

    import requests
    from bs4 import BeautifulSoup

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0"}
    
    def check_user(func):

        def check(*args, **kwargs):
            # print(args[0])
            try:
                queries.cursorObj.execute(
                "{0}'{1}'".format(queries.username_query, args[0])) 
                data = queries.cursorObj.fetchall()
                # print(data)
                if len(data) == 0:
                    print("\n\t\t\tInvalid Credentials!")
                    return 1
                else:
                    print("Credentials verified!")
                    queries.cursorObj.execute("{0}'{1}'".format(queries.scrape_check, args[0]))
                    data, = queries.cursorObj.fetchone()
                    if data == 1:
                        return_val = Person.show(args[0])
                        return return_val
                    else:
                        return_val = func(args[0])
                        return return_val
            except Exception as e:
                print(e)
                print(traceback.format_exc())
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

        @staticmethod
        def show(user):
            queries.cursorObj.execute(queries.all_sql, (user,))
            scrap = queries.cursorObj.fetchall()
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
            print(f'\n\nMy name is {obj.name}, and my city is {obj.city}\n\n')
            
            return obj

        def for_test(self):
            return "Task Over"

    
    @ check_user
    def scrape(username):
        try:
            obj = ""
            req = requests.get(f"{const.fb}{username}/about", headers=headers)
            soup = BeautifulSoup(req.content, "html5lib")

            user_name = soup_utility.name(soup)

            work_ = soup_utility.work(soup)
            
            user_city = soup_utility.city(soup)


            driver = user_agent.webdriver.Chrome(service=service)
            driver.get(const.fb)
            while True:
                try:
                    driver.find_element_by_name('email').send_keys("conquerorpk@gmail.com")
                    driver.find_element_by_name('pass').send_keys(hidden)
                    time.sleep(2)
                    driver.find_element_by_name('login').click()


                    driver.implicitly_wait(5)


                    driver.find_element(user_agent.By.LINK_TEXT, 'Not Now').click()
                    time.sleep(2)
                    break
                except Exception as e:
                    time.sleep(5)
                    

            favs = soup_utility.favorites(driver, username)
            
            json_favs = json.dumps(favs) 

            if len(work_) == 0:
                if user_city != "" :
                    obj = Person(name=user_name, city=user_city, fav=favs)
                else:
                    obj = Person(name=user_name, fav=favs)
            else :
                if user_city != "":
                    obj = Person(name=user_name,work=work_ ,city=user_city, fav=favs)
                else:
                    obj = Person(name=user_name,work=work_, fav=favs)


            json_work = json.dumps(work_)

            bool = True
            
            queries.cursorObj.execute(queries.update_sql, (bool, obj.name, json_work, obj.city, json_favs ,username))
            queries.mydb.commit()
            driver.quit()

            print(f'\n\nMy name is {obj.name}, and my city is {obj.city}\n\n')

            return obj
        except Exception as e:
            print("Can't scrape data: {}".format(e))
            print(sys.exc_info())
            driver.quit()
    
except Exception as e:
    print(e)
    print(sys.exc_info())