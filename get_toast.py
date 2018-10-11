#!/user/bin/python
#-*-coding:utf-8-*-
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import logging
logging.getLogger().setLevel(logging.INFO)

def find_Toast2(self,message):
    logging.info("查找toast值是：'%s'"%(message))
    try:
        message='//*[@text=\'{}\']'.format(message)
        #print message
        WebDriverWait(self.driver,5,0.5).until(expected_conditions.presence_of_element_located((By.XPATH,message)))
        logging.info("查找到toast：%s"%message)
        return True
    except:
        logging.info("ERROR 未查找到toast：%s"%message)
        return False





