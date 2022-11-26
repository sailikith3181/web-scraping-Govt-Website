from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
#from bs4 import BeautifulSoup
url='https://data.gov.in/catalogs?page=1'
def get_driver():
  chrome_options=Options()
  chrome_options.add_argument('--no-sandbox')
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--disable-dev-hsm-usage')
  driver = webdriver.Chrome(options=chrome_options)
  return driver
  
base_url='https://data.gov.in/catalogs?page='
def urls(base_url):
  total_list=[]
  for i in range(1,25,1):
    total_url=base_url+str(i)
    total_list.append (total_url)
  return total_list
def catalog(div_tag):
  a_tag=div_tag.find_element(By.TAG_NAME,'a')
  title=a_tag.text
  findlink=a_tag.get_attribute('href')
  text_=(div_tag.find_element(By.CLASS_NAME,'card-text').text)
  sub_tag=div_tag.find_elements(By.CLASS_NAME,'list-group-item')
  database=[]
  for i in range(len(sub_tag)):
    database.append(sub_tag[i].text)
  return{
    'Title':title,
    'description':text_,
    'Links':findlink,
    "data and API'S":database[0],
    'Updates':database[1],
    #'Views and downloads':database[2]
  }
def all_repos(driver):
  div_tag=driver.find_elements(By.CLASS_NAME,"catalog_grid_box")
  total_repos=[catalog(tag)for tag in div_tag]
  return total_repos
def full_info(base_url):
  list_=[]
  all_links=urls(base_url)
  for link in all_links:
    driver=get_driver()
    driver.get(link)
    new_list=all_repos(driver)
    list_.extend(new_list)
  return list_


if __name__=="__main__":
  base_url='https://data.gov.in/catalogs?page='
  print('creating driver and getting the url')
  lists=full_info(base_url)
  #print(lists)
  #print(urls(base_url))
  df= pd.DataFrame.from_records(lists)
  df.to_csv('govtdata.csv',index=None)