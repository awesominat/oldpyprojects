import math
import os
import time
from random import randint

import numpy as np
import requests
from imageai.Prediction.Custom import CustomImagePrediction
from selenium import webdriver
from selenium.webdriver import ActionChains
from PIL import Image

# PROXY = ""

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
chrome_options.add_argument('--disable-extensions')
chrome_options.add_argument('--profile-directory=Default')
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--disable-plugins-discovery");
chrome_options.add_argument("--start-maximized")

execution_path = os.getcwd()


prediction = CustomImagePrediction()
prediction.setModelTypeAsResNet()
prediction.setModelPath(os.path.join(execution_path, "idenprof_061-0.7934.h5")) # dataset for fire hydrants
prediction.setJsonPath("idenprof_model_class.json")
prediction.loadModel(num_objects=2)

api_key = '' # removed
api_secret = '' # removed


def crop(im, height, width):
    imgwidth, imgheight = im.size
    rows = np.int(imgheight/height)
    cols = np.int(imgwidth/width)
    for i in range(rows):
        for j in range(cols):
            #  print (i,j)
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)


def ASKAPI(url):
    response = requests.get(
        'https://api.imagga.com/v2/tags?image_url=%s' % url,
        auth=(api_key, api_secret))
    return  response.json()


def ParseJSONForSidewalk(str):
    # json1_data = json.loads(str)
    ISSIDEWALK = False

    for w in str['result']['tags']:
        if w['tag']['en'] == "sidewalk":
            ISSIDEWALK = True
            break

    return ISSIDEWALK


def GetAllImagePortions():
    im = Image.open('img.jpg')

    imgwidth, imgheight = im.size
    print(('Image size is: %d x %d ' % (imgwidth, imgheight)))

    for k, piece in enumerate(crop(im, 100, 100), 0):
        img=Image.new('RGB', (100,100), 255)
        img.paste(piece)
        path = os.path.join("cam%d.jpg" % (int(k+1)))
        img.save('./test/' + path)


def ContactWebsiteToSplit(url):
    first = url.split("&k=", 1)[0]
    second = url.split("&k=", 1)[1]

    payload = {'u': first, 'k': second}

    r = requests.get(url='https://diet-jam.000webhostapp.com/data.php/', params=payload)


# driver = webdriver.Chrome('chromedriver', options=chrome_options)

#  chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']) ONLY CHROME v78, AND < 79.0.3945.16

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome('chromedriver', options=options)
# driver = webdriver.Firefox()


driver.maximize_window()
driver.get('https://www.google.com/recaptcha/api2/demo')
builder = ActionChains(driver)
time.sleep(2)


def ClickCheckmark():
    driver.switch_to.default_content()
    driver.switch_to.frame(
        driver.find_element_by_xpath('/html/body/div[1]/form/fieldset/ul/li[5]/div/div/div/div/iframe'))

    builder.move_to_element(driver.find_element_by_xpath('/html/body/div/div[3]/div[1]/div/div/span/div[1]')).perform()
    time.sleep(randint(1, 2))
    builder.click().perform()


def SafeClickCheckmark():
    a = driver.execute_script("""
    
    function getElementByXpath(path, doc) {
      return document.evaluate(path, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    }
    
    var b = getElementByXpath('/html/body/div[1]/form/fieldset/ul/li[5]/div/div/div/div/iframe', document)
    console.log(b.contentWindow.document)
    var c = getElementByXpath('/html/body/div[2]/div[3]/div[1]/div/div/span/div[1]', b.contentWindow.document)
    c.click()
    
    """)


def Solve_Captcha():
    SafeClickCheckmark()

    time.sleep(2)

    driver.switch_to.default_content()

    driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[2]/div[4]/iframe'))
    category_name = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/div[1]/div/strong').get_attribute(
        'innerText')
    reset_challenge = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[1]')

    finalimage = driver.find_element_by_xpath(
                    '/html/body/div/div/div[2]/div[2]/div[1]/table/tbody/tr/td[1]/div/div[1]/img').get_attribute('src')
    tempimagetype = driver.find_element_by_xpath(
        '/html/body/div/div/div[2]/div[2]/div[1]/table/tbody/tr/td[1]/div/div[1]/img').get_attribute('class')

    print('------------------------')
    print(category_name)
    print(tempimagetype)
    print('------------------------')

    if category_name != "a fire hydrant":
        while True:
            driver.switch_to.default_content()
            abec = driver.execute_script("""
            function getElementByXpath(path, doc) {
              return document.evaluate(path, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
            }

            var b = getElementByXpath('/html/body/div[2]/div[4]/iframe', document)
            console.log(b.contentWindow.document)
            var c = getElementByXpath('/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[1]/button', b.contentWindow.document)
            c.click()
            """)
            driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[2]/div[4]/iframe'))

            # driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div[1]/div[1]').click()
            time.sleep(2)
            tempname = driver.find_element_by_xpath('/html/body/div/div/div[2]/div[1]/div[1]/div/strong')
            tempimagetype = driver.find_element_by_xpath(
                '/html/body/div/div/div[2]/div[2]/div[1]/table/tbody/tr/td[1]/div/div[1]/img').get_attribute('class')
            print('------------------------')
            print(category_name)
            print(tempimagetype)
            print('------------------------')
            if tempname.get_attribute('innerText') == "a fire hydrant" and tempimagetype == "rc-image-tile-33":
                finalimage = driver.find_element_by_xpath(
                    '/html/body/div/div/div[2]/div[2]/div[1]/table/tbody/tr/td[1]/div/div[1]/img').get_attribute('src')
                break

    with open('img.jpg', 'wb') as handle:
        response = requests.get(finalimage, stream=True)
        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)

    # ContactWebsiteToSplit(finalimage)


    GetAllImagePortions()

    TempClicked = []

    for filename in os.listdir('./test/'):
        if filename.endswith(".jpg"):
            predictions, probabilities = prediction.predictImage(os.path.join('./test/', filename), result_count=3)

            for eachPrediction, eachProbability in zip(predictions, probabilities):
                print(filename, " : ", eachPrediction, " : ", eachProbability)
                if eachPrediction == "firehydrant" and eachProbability >= 98:

                    tempfilename = filename.replace(".jpg", "")
                    tempfilename = int(tempfilename.replace("cam", ""))

                    column = math.ceil(tempfilename / 3)
                    row = tempfilename % 3
                    if row == 0: row = 3
                    TempClicked.append(tempfilename)
                    print('column: ', column, " row: ", row)
                    thingtofind = '/html/body/div/div/div[2]/div[2]/div[1]/table/tbody/tr[{}]/td[{}]/div/div[1]/img'.format(column,
                                                                                                      row)
                    # driver.switch_to.default_content()
                    anjw = driver.execute_script("""
                    function getElementByXpath(path, doc) {
                      return document.evaluate(path, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    }

                    var c = getElementByXpath('%s', document)
                    c.click()
                    """  % (thingtofind))

                    # finalimage = driver.find_element_by_xpath(
                    #     thingtofind).click()
                    print('CLICKING IMAGE ROW ', row, ", COLUMN ", column)
            time.sleep(.5)
            continue
        else:
            continue

    time.sleep(5)

    for i in range(1, 4):
        for w in TempClicked:
            column = math.ceil(w / 3)
            row = w % 3
            if row == 0: row = 3
            thingtofindt = '/html/body/div/div/div[2]/div[2]/div[1]/table/tbody/tr[{}]/td[{}]/div/div[1]/img'.format(column,row)

            thingtofindt = driver.find_element_by_xpath(thingtofindt).get_attribute('src')
            with open('img.jpg', 'wb') as handle:
                response = requests.get(thingtofindt, stream=True)
                for block in response.iter_content(1024):
                    if not block:
                        break

                    handle.write(block)
            predictionst, probabilitiest = prediction.predictImage('img.jpg', result_count=3)

            for eachPrediction, eachProbability in zip(predictionst, probabilitiest):
                print(filename, " : ", eachPrediction, " : ", eachProbability)
                if eachPrediction == "firehydrant" and eachProbability >= 98:
                    column = math.ceil(w / 3)
                    row = w % 3
                    if row == 0: row = 3

                    thingtofind = '/html/body/div/div/div[2]/div[2]/div[1]/table/tbody/tr[{}]/td[{}]'.format(column,
                                                                                                             row)
                    driver.switch_to.default_content()
                    wefa = driver.execute_script("""
                    function getElementByXpath(path, doc) {
                      return document.evaluate(path, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    }

                    var b = getElementByXpath('/html/body/div[2]/div[4]/iframe', document)
                    console.log(b.contentWindow.document)
                    var c = getElementByXpath('%s', b.contentWindow.document)
                    c.click()
                    """ % (thingtofind))
                    driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[2]/div[4]/iframe'))

                    # finalimage = driver.find_element_by_xpath(
                    #     thingtofind).click()
            time.sleep(.5)
        time.sleep(3)

    driver.switch_to.default_content()

    # driver.switch_to.frame(driver.find_element_by_xpath('/html/body/div[2]/div[4]/iframe'))

    bbsd = driver.execute_script("""
    function getElementByXpath(path, doc) {
      return document.evaluate(path, doc, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
    }

    var b = getElementByXpath('/html/body/div[2]/div[4]/iframe', document)
    console.log(b.contentWindow.document)
    var c = getElementByXpath('/html/body/div/div/div[3]/div[2]/div[1]/div[2]/button', b.contentWindow.document)
    c.click()
    """)

    # driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div[1]/div[2]/button').click()



Solve_Captcha()

# driver.quit()
