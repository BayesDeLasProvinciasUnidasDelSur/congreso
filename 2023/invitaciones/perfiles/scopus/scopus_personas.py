from lxml import html
import nltk
import pycountry
import requests
import pickle
import csv
import pandas as pd
from collections import defaultdict
import re
import time
import os
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from datetime import date

import numpy as np
from scipy.io.wavfile import write
import pygame

import time
from selenium.webdriver.common.by import By
import selenium
from unidecode import unidecode

from pygame import mixer
mixer.init()
sound=mixer.Sound("bell.wav")
sound2=mixer.Sound("bell2.wav")

def window_bounds(driver):
    win_upper_bound = driver.execute_script('return window.pageYOffset')
    win_left_bound = driver.execute_script('return window.pageXOffset')
    win_width = driver.execute_script('return document.documentElement.clientWidth')
    win_height = driver.execute_script('return document.documentElement.clientHeight')
    win_right_bound = win_left_bound + win_width
    win_lower_bound = win_upper_bound + win_height
    return win_left_bound, win_right_bound, win_upper_bound, win_lower_bound

def element_completely_viewable(driver, elem, win_left_bound, win_right_bound, win_upper_bound , win_lower_bound ):
    elem_left_bound = elem.location.get('x')
    elem_top_bound = elem.location.get('y')
    elem_width = elem.size.get('width')
    elem_height = elem.size.get('height')
    elem_right_bound = elem_left_bound + elem_width
    elem_lower_bound = elem_top_bound + elem_height
    #
    return all((win_left_bound <= elem_left_bound,
                win_right_bound >= elem_right_bound,
                win_upper_bound <= elem_top_bound,
                win_lower_bound >= elem_lower_bound)
              )


# Set up the Firefox profile with the desired proxy settings
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "localhost")
profile.set_preference("network.proxy.socks_port", 2000)

driver = webdriver.Firefox(firefox_profile=profile)

url="https://www.scopus.com/authid/detail.uri?authorId={}".format(26538012200)

driver.get(url)

apellido, nombre = driver.find_elements(By.XPATH,"//section/div/div/h1")[0].text.split(", ")
print(apellido, ",", nombre)


tree = html.fromstring(driver.page_source)


driver.close()

