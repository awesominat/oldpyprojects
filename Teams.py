from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome("chromedriver.exe")
driver.set_page_load_timeout(60)
driver.get("https://teams.microsoft.com/")

wait = WebDriverWait(driver, 10)
wait3 = WebDriverWait(driver, 20)
wait2 = WebDriverWait(driver, .5)

men_menu = wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div/form[1]/div/div/div[2]/div/div/div["
                                                                  "1]/div[2]/div[2]/div/div/div/div[2]/div["
                                                                  "2]/div/input[1]")))
men_menu.send_keys("") # username / email here

continue_from_email = wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div/form[1]/div/div/div["
                                                                             "2]/div/div/div[1]/div[2]/div["
                                                                             "2]/div/div/div/div["
                                                                             "4]/div/div/div/div/input")))

driver.execute_script("arguments[0].click();", continue_from_email)

password_put = wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div/form[1]/div/div/div["
                                                                      "2]/div/div/div[1]/div[2]/div[2]/div/div["
                                                                      "2]/div/div[2]/div/div[2]/input")))
password_put.send_keys("") # password

continue_from_pass = wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div/form[1]/div/div/div["
                                                                            "2]/div/div/div[1]/div[2]/div[2]/div/div["
                                                                            "2]/div/div[3]/div["
                                                                            "2]/div/div/div/div/input")))

driver.execute_script("arguments[0].click();", continue_from_pass)

no_stay_signed_in = wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div/form/div/div/div[1]/div["
                                                                           "2]/div/div[2]/div/div[3]/div["
                                                                           "2]/div/div/div[1]/input")))

driver.execute_script("arguments[0].click();", no_stay_signed_in)

profile_pic = wait3.until(
    ec.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[1]/app-header-bar/div/div/button")))

driver.execute_script("arguments[0].click();", profile_pic)


def change_status(text):
    try:
        edit_or_create = wait2.until(
            ec.visibility_of_element_located((By.XPATH, "/html/body/div[5]/settings-dropdown/div/div[2]/div[1]/div["
                                                        "1]/div[2]/div[2]/div/div/div")))
        driver.execute_script("arguments[0].click();", edit_or_create)
    except TimeoutException:
        edit_or_create = wait2.until(
            ec.visibility_of_element_located((By.XPATH, "/html/body/div[5]/settings-dropdown/div/div/ul/li[3]/button")))
        driver.execute_script("arguments[0].click();", edit_or_create)

    textbox = wait.until(
        ec.visibility_of_element_located((By.XPATH, "/html/body/div[5]/settings-dropdown/div/div[2]/div[1]/div["
                                                    "1]/div[2]/div[2]/div/div/div")))

    if text == "DELETE":
        textbox.send_keys(
            Keys.CONTROL + "a")
        textbox.send_keys(
            Keys.DELETE)
    else:
        textbox.send_keys(text)

    show_when_msg = wait.until(
        ec.visibility_of_element_located((By.XPATH, "/html/body/div[5]/settings-dropdown/div/div[2]/div[1]/div["
                                                    "2]/teams-checkbox/div/label")))

    if show_when_msg.get_attribute("aria-checked") == "false":
        driver.execute_script("arguments[0].click();", show_when_msg)


    done_button = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "/html/body/div[5]/settings-dropdown/div/div[2]/div[5]/div/button")))

    driver.execute_script("arguments[0].click();", done_button)


string_name = "test"

try:
    delete = wait.until(
        ec.visibility_of_element_located(
            (By.XPATH, "/html/body/div[5]/settings-dropdown/div/div/ul/li[3]/button[2]")))

    driver.execute_script("arguments[0].click();", delete)
except TimeoutException:
    print('ok')

while True:
    for element in range(0, len(string_name)):
        change_status(string_name[element])
        sleep(3)
    change_status("DELETE")
