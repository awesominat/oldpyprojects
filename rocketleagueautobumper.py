from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from selenium.common.exceptions import NoSuchElementException


def check_exists_by_xpath(driv, xpath):
    try:
        driv.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

options = Options()
#options.add_argument("--headless")
options.add_argument("window-size=1920,900")
ia = 0

def mainfunc():
    global ia
    print('starting {}'.format(str(ia)))
    driver = webdriver.Chrome('chromedriver', options=options)
    driver.get('https://rocket-league.com/');

    if check_exists_by_xpath(driver, '/html/body/div[1]/div/div/div/div[2]/div/button[2]') == True:
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/button[2]').click()

    a1 = driver.find_element_by_xpath('/html/body/div[3]/div/div/p/button')
    a1.click()

    time.sleep(4)

    if check_exists_by_xpath(driver, '/html/body/div[1]/div/div/div/div[2]/div/button[2]') == True:
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/button[2]').click()

    time.sleep(1)

    a = driver.find_element_by_xpath('/html/body/header/section[1]/div/div[2]/div[1]/form/input[2]')
    a.click()
    a.send_keys("blackmg51055@gmail.com")
    time.sleep(.2)
    b = driver.find_element_by_xpath('/html/body/header/section[1]/div/div[2]/div[1]/form/input[3]')
    b.click()
    b.send_keys("") # password
    driver.find_element_by_xpath('/html/body/header/section[1]/div/div[2]/div[1]/form/input[4]').click()

    driver.get('https://rocket-league.com/trades/Lorando');

    time.sleep(2)

    if check_exists_by_xpath(driver, '/html/body/div[1]/div/div/div/div[2]/div/button[2]') == True:
        driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/button[2]').click()

    time.sleep(1)

    x = driver.find_elements_by_xpath('/html/body/main/div/div/div/div[3]/*')

    for element in x:
        driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(.1)
        element.find_element_by_xpath(".//div[2]/button").click()
        time.sleep(4)
        driver.find_element_by_xpath("/html/body/div[2]/div/span/i").click()
        time.sleep(4)
    print('done {}'.format(str(ia)))
    ia = ia + 1

    while True == True:
        time.sleep(915)
        print('starting {}'.format(str(ia)))
        driver.refresh()

        time.sleep(7.5)

        if check_exists_by_xpath(driver, '/html/body/div[3]/div/div/p/button') == True:
            driver.find_element_by_xpath('/html/body/div[3]/div/div/p/button').click()
            time.sleep(4)

        if check_exists_by_xpath(driver, '/html/body/div[1]/div/div/div/div[2]/div/button[2]') == True:
            driver.find_element_by_xpath('/html/body/div[1]/div/div/div/div[2]/div/button[2]').click()
            time.sleep(4)

        x = driver.find_elements_by_xpath('/html/body/main/div/div/div/div[3]/*')

        for element in x:
            driver.execute_script("arguments[0].scrollIntoView();", element)
            time.sleep(.1)
            element.find_element_by_xpath(".//div[2]/button").click()
            time.sleep(4)
            driver.find_element_by_xpath("/html/body/div[2]/div/span/i").click()
            time.sleep(4)
        print('done {}'.format(str(ia)))
        ia = ia + 1

if __name__ == "__main__":
    print('welcome ahaha')
    mainfunc()
