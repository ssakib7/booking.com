from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import undetected_chromedriver as uc
from time import sleep
from selenium.common.exceptions import TimeoutException 
from selenium.common.exceptions import ElementClickInterceptedException 
from selenium import webdriver
import random
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium_stealth import stealth

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.41',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
]
custom_ua = random.choice(user_agents)
# chrome_driver_path = "/usr/local/bin/chromedriver" 
options = Options()
options.add_argument(f'user-agent={custom_ua}')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-popup-blocking")
options.add_argument('window-size=1920x1080');
# executable_path=chrome_driver_path,
driver = uc.Chrome(chrome_options=options)
stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )

driver.implicitly_wait(20)
wait = WebDriverWait(driver, 30)
driver.maximize_window()
website="https://www.booking.com"
driver.get(website)
print("Website Opened")
data=[]
try:
    popup=WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH,'//button[@aria-label="Dismiss sign-in info."]'))).click()
except:
    pass

try:
    cityn=input("Enter City Name: ")
    city=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id=":Ra9:"]'))).send_keys(cityn)
    check_in_date=input("Enter Check In Date (yyyy-mm-dd): ")
    check_out_date=input("Enter Check Out Date (yyyy-mm-dd): ")
    date_picker=wait.until(EC.presence_of_element_located((By.XPATH,'//div[@data-testid="searchbox-dates-container"]'))).click()
    sleep(1)
    i=0
    while True:
        try:
            check_in=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//span[@data-date="'+check_in_date+'"]'))).click()
            break
        except:
            if i==0:
                next_month=wait.until(EC.presence_of_element_located((By.XPATH,'//div[@data-testid="searchbox-datespicker-calandar"]/button[1]'))).click()
                i=i+1
            else:
                next_month=wait.until(EC.presence_of_element_located((By.XPATH,'//div[@data-testid="searchbox-datepicker-caaLndar"]/button[2]'))).click()

    while True:
        try:
            check_out=WebDriverWait(driver,3).until(EC.presence_of_element_located((By.XPATH,'//span[@data-date="'+check_out_date+'"]'))).click()
            break
        except Exception as e:
            print(e)
            if i==0:
                next_month=wait.until(EC.presence_of_element_located((By.XPATH,'//div[@data-testid="searchbox-datepicker-calendar"]/button[1]'))).click()
                i=i+1
            else:
                next_month=wait.until(EC.presence_of_element_located((By.XPATH,'//div[@data-testid="searchbox-datepicker-calendar"]/button[2]'))).click()
        

    search=wait.until(EC.presence_of_element_located((By.XPATH,'//button[@type="submit"]'))).click()

    sleep(5)
    while True:
        try:
            hottels=wait.until(EC.presence_of_all_elements_located((By.XPATH,'//a[@data-testid="availability-cta-btn"]')))
            for hottel in hottels:
                hottel.send_keys(Keys.CONTROL + Keys.RETURN)
                sleep(1) # wait for the new tab to open
                driver.switch_to.window(driver.window_handles[-1])
                title=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#hp_hotel_name>div>h2'))).text
                available_rooms=len(wait.until(EC.presence_of_all_elements_located((By.XPATH,'//span[@class="hprt-roomtype-icon-link "]'))))
                web_data={
                    "Hotel Name":title,
                    "Available Rooms":available_rooms
                }
                data.append(web_data)
                print(web_data)
                sleep(random.randint(5,7))
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            next_page=WebDriverWait(driver,3).until(EC.element_to_be_clickable((By.XPATH,'//button[@aria-label="Next page"]'))).click()
            sleep(7)
        except:
            break
except TimeoutException:
    pass
except Exception as e:
    print(e)
    sleep(200)
df=pd.DataFrame(data)
df.to_csv(cityn+".csv",index=False)
driver.quit()