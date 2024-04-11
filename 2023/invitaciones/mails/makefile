activate: venv-undetected_chromedrive
	source venv-undetected_chromedrive/bin/activate

venv-undetected_chromedrive:
	python3 -m venv venv-undetected_chromedrive
	pip install undetected-chromedriver
	pip install lxml nltk pycountry requests pandas datetime  numpy scipy selenium unidecode pygame

update_chrome:
	sudo apt-get update
	sudo apt-get --only-upgrade install google-chrome-stable
