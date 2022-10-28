from lxml import html
import requests
import csv
import pandas as pd
from collections import defaultdict
import re
import time
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.action_chains import ActionChains

import time
from selenium.webdriver.common.by import By
import selenium
from unidecode import unidecode

driver = webdriver.Firefox()

url= "https://www.linkedin.com/search/results/people/?geoUrn=[%22100446943%22]&keywords=bayesian&origin=FACETED_SEARCH&page=1&sid=yFh"

url_ar = "https://www.linkedin.com/search/results/people/?keywords=bayesian&origin=FACETED_SEARCH&schoolFilter=%5B%22900758%22%2C%2215091522%22%2C%22566506%22%2C%22402027%22%2C%221190954%22%2C%22341722%22%2C%226999890%22%2C%22123724%22%2C%2215141765%22%2C%22338240%22%2C%221099951%22%2C%221212758%22%2C%221732640%22%2C%2253629%22%2C%22573021%22%2C%2261238%22%2C%22728787%22%5D&sid=-LN"

url_ur = "https://www.linkedin.com/search/results/people/?keywords=bayesian&origin=FACETED_SEARCH&schoolFilter=%5B%2238258%22%2C%2243361%22%2C%22578031%22%5D&sid=2kF"


driver.get(url)
tree = html.fromstring(driver.page_source)
