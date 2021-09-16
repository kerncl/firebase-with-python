from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import pandas as pd
import validators
import sys
import re
import logging
import os


### Global Variable ###
klse_url = 'https://www.klsescreener.com/v2/'


### Initialize Logger ###
def initialize_logger():
    """
    Initialize the logger for the flow
    Returns:
        None
    """
    format = '%(asctime)4s [%(levelname)s]: %(message)s'
    logging.basicConfig(format=format, level=logging.INFO, datefmt='%d/%m/%y-%H:%M:%S', filename=os.path.join(os.getcwd(), 'stock_list.log'))
    logging.FileHandler(filename='stock_list.log', mode='w')


def web_access():
    """
    Access to the klse page and extract out the stock list
    Returns:
        data (html): return the html format string
    """
    ### Dynamic Website ###
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-erros')
    options.add_argument('--test-type')
    driver = webdriver.Chrome(executable_path=r'C:\bat\chromedriver_win32\chromedriver.exe', chrome_options=options)
    driver.get(klse_url)
    xpath_submit = "//input[@id='submit' and @value='Screen']"
    submit_button = driver.find_element_by_xpath(xpath=xpath_submit)
    submit_button.click()
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "table-responsive")))
    except:
        logging.error(f'Error: {EC}')
        logging.error('Web loading too slow ..... out of time.... exiting code')
        sys.exit(1)
    data = driver.page_source
    driver.close()

    ### Static Website ###
    # req = Request(url=klse_url, headers={'user-agent':'my-app'})
    # data = urlopen(req)
    return data


def web_scrapping_stock(data):
    """
    Perform web scrapping, extract out useful information from klse website and save it into pickle file and csv file
    Args:
        data (html): webpage source

    Returns:
        None
    """
    ### Web Scraping ###
    html = BeautifulSoup(data, 'lxml')
    stock_tb_list = html.find(name='tbody').findAll(name='tr')
    code_list = []
    name_list = []
    company_list = []
    sector_list = []
    market_list = []
    EPS_list = []
    ROE_list = []
    YoY_list = []
    QoQ_list = []
    ConQ_list = []
    TopQ_list = []
    RYoY_list = []
    RQoQ_list = []
    RConQ_list = []
    RTopQ_list = []
    price_list = []

    for index, stock_data in enumerate(stock_tb_list):
        # print(stock_data)
        YoY = QoQ = ConQ = TopQ = RYoY = RQoQ = RConQ = RTopQ = 'No'
        company_info = stock_data.find(name='td')
        pattern = re.compile('[\w\d\-\.&]+')
        match = re.match(pattern, company_info.text)
        stock_name = match.group()
        company_full_name = company_info.attrs.get('title')
        stock_code = stock_data.find(attrs={'title': 'Code'}).text
        EPS = stock_data.find(attrs={'title': 'EPS'}).text
        ROE = stock_data.find(attrs={'title':'ROE'}).text
        price = stock_data.findAll(name='td')[3].text
        try:
            sector, market = stock_data.findAll(name='td')[2].text.split(',')
        except:
            sector = 'None'
            market = 'None'
        indicators = [indicator.text for indicator in stock_data.findAll(name='span')]
        if 'YoY' in indicators:
            YoY = 'Yes'
        if 'QoQ' in indicators:
            QoQ = 'Yes'
        if 'ConQ' in indicators:
            ConQ = 'Yes'
        if 'TopQ' in indicators:
            TopQ = 'Yes'
        if 'RYoY' in indicators:
            RYoY = 'Yes'
        if 'RQoQ' in indicators:
            RQoQ = 'Yes'
        if 'RConQ' in indicators:
            RConQ = 'Yes'
        if 'RTopQ' in indicators:
            RTopQ = 'Yes'
        code_list.append(stock_code)
        name_list.append(stock_name)
        company_list.append(company_full_name)
        sector_list.append(sector)
        market_list.append(market.strip())
        price_list.append(price)
        EPS_list.append(EPS)
        ROE_list.append(ROE)
        YoY_list.append(YoY)
        QoQ_list.append(QoQ)
        ConQ_list.append(ConQ)
        TopQ_list.append(TopQ)
        RYoY_list.append(RYoY)
        RQoQ_list.append(RQoQ)
        RConQ_list.append(RConQ)
        RTopQ_list.append(RTopQ)
        logging.info(f'({index+1})\t{company_full_name}:\t{stock_name} ({stock_code})\t{sector}\t{market}')

    ### Export into Pandas ###
    stock_df = pd.DataFrame({'Code': code_list,
                             'Stock': name_list,
                             'Company': company_list,
                             'Sector': sector_list,
                             'Market': market_list,
                             'Price': price_list,
                             'EPS': EPS_list,
                             'ROE': ROE_list,
                             'YoY': YoY_list,
                             'QoQ': QoQ_list,
                             'ConQ': ConQ_list,
                             'TopQ': TopQ_list,
                             'RYoY': RYoY_list,
                             'RQoQ': RQoQ_list,
                             'RConQ': RConQ_list,
                             'RTopQ': RTopQ_list})
    csv_file = f'stock_list_{datetime.today().date()}.csv'
    pickle_file = f'stock_list_{datetime.today().date()}.pkx'
    stock_df.to_csv(os.path.join(os.getcwd(), csv_file), index=False)
    stock_df.to_pickle(os.path.join(os.getcwd(), pickle_file))
# print(stock_df)


def web_scrapping_news(code):
    """
    Web scrapping on news based on the stock code given
    Args:
        code (str): stock code

    Returns:
        (list): return list of news link
    """
    klse_news_url = f'{klse_url}/news/stock/{code}'
    try:
        req = Request(url=klse_news_url, headers={'user-agent': 'my-app'})
        data = urlopen(req)
    except Exception as error:
        logging.critical(f'{error}, Unable to access webpage')
        print(f'Webpage unable to access, error message {error}')
        exit(1)
    html = BeautifulSoup(data, 'lxml')
    link_html_list = html.findAll(name='h2', attrs={'class': 'figcaption'})
    link_list = [f"https://www.klsescreener.com{link_html.find(name='a').attrs['href']}" for link_html in link_html_list if validators.url(f"https://www.klsescreener.com{link_html.find(name='a').attrs['href']})")]
    # print(link_list)
    return link_list


def text_processing(links):
    news = {}
    for i, link in enumerate(links):
        content = {'header': '', 'date': '', 'paragraph': ''}
        try:
            req = Request(url=link, headers={'user-agent': 'my-app'})
            data = urlopen(req)
        except Exception as error:
            logging.critical(f'{error}, Unable to access webpage')
        html = BeautifulSoup(data, 'lxml')
        header = html.find(attrs={'class': 'news-container'}).find(name='h2').text
        if re.search("[\u4e00-\u9FFF]", header):
            continue
        header = html.title.text.rstrip().strip()
        date = html.find(name='span', attrs={'class': 'col-sm-5 text-muted'}).text
        page_contents = html.find(name='div', attrs={'class': 'content text-justify'}).findAll(text=True)
        paragraph = ' '.join(page_content.replace(u'\xa0',' ').rstrip().strip() for page_content in page_contents)
        content['header'] = header
        content['date'] = date
        content['paragrpah'] = paragraph
    return news


def sentiment_analysis(news):
    vader = SentimentIntensityAnalyzer()
    for index, content in news.items():
        header = content['header']
        paragrpah = content['paragraph']
        date = content['date']

        header_score = vader.polarity_scores(header)
        paragrpah_score = vader.polarity_scores(paragrpah)
        words = word_tokenize(paragrpah)
        stopword = stopwords.words('english')
        words = [word for word in words if word.isalpha() if word not in stopword]
        fdist = FreqDist(words)
        keywords = fdist.most_common(10)


    return 0


if __name__ == '__main__':
    initialize_logger()
    # data = web_access()
    # web_scrapping_stock(data)
    links = web_scrapping_news('0185')
    news = text_processing(links)
    logging.info('Finish')