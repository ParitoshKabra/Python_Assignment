from const import SCROLL_PAUSE_TIME
import time
import user_agent
def name(soup):
    strip = len(" | Facebook")
    strip = strip - 2*strip
    return soup.title.get_text()[:strip]

def work(soup):
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
    return work
def city(soup):
    str_city = "यहाँ रह चुके हैं"
    city_header = soup.find(lambda tag: tag.name == "header" and str_city in tag.text)
    return (city_header.parent.find('h4').get_text())
def favorites(driver, username):
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    
    driver.get(f"https://m.facebook.com/{username}/about")
    time.sleep(2)
    
    favs = []
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    current_scroll_position = 0
    speed = 300
    new_height = 1
    while current_scroll_position <= new_height:
        driver.execute_script("window.scrollTo(0, {});".format(current_scroll_position))
        current_scroll_position += speed
        like_div=""
        try:
            time.sleep(SCROLL_PAUSE_TIME)
            like_div = driver.find_element(user_agent.By.XPATH , "//div[contains(text(),'Likes')]/../../div[3]/a").click()
            time.sleep(3)
            break
            
        except Exception:
            print(like_div)
            new_height = driver.execute_script("return document.body.scrollHeight")
    
    driver.find_element(user_agent.By.XPATH, '//*[@id="timelineBody"]/div/div/div/div[1]/div/header/div/div[3]/a').click()
    time.sleep(2)       
    for span in driver.find_elements(user_agent.By.XPATH, '/html/body/div[1]/div[1]/div[4]/div/div/div/div/div/divdiv/div/div[1]/div[*]/div/span'):
        favs.append(span.text)
    for span in driver.find_elements(user_agent.By.XPATH, '/html/body/div[1]/div[1]/div[4]/div/div/div/div/div/divdiv/div/div[2]/div[*]/div/span'):
        favs.append(span.text)
    return favs