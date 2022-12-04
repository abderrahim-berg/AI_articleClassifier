from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
from multiprocessing import Pool,Manager
import unidecode 
from itertools import repeat



tags=['computer vision','natural language processing','evolutionary computation','robotics','speech recognition','expert systems','neural networks']
driver_location=(r"C:\\Program Files (x86)\\chromedriver.exe")



def extract_tag_data(tag,dataset_dictionary,lst):
    driver= webdriver.Chrome(driver_location)
    driver.get("https://hal.archives-ouvertes.fr/search/index?q="+tag)
    for _ in range (20):
        articles=driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr/td[2]/div[@class='media']/div[@class='media-body']/strong/a")
        for i in range(len(articles)-1):
            driver.find_elements(By.XPATH, "//table[@class='table table-hover']/tbody/tr/td[2]/div[@class='media']/div[@class='media-body']/strong/a")[i].click()
            dataset_dictionary['tag']=tag
            dataset_dictionary['article_title']= unidecode.unidecode(driver.find_element(By.XPATH,'//h1[@class="title"]').text)
            dataset_dictionary['abstract']= unidecode.unidecode(driver.find_element(By.XPATH,'//div[@class="abstract" or @class="content-en"]/div[1]').text)
            dataset_dictionary['authors']=(",".join([element.text for element in (driver.find_elements(By.XPATH,'//div[@class="authors"]/span'))]))
            dataset_dictionary['structs']=(",".join([element.text for element in (driver.find_elements(By.XPATH,'//div[@class="authors"]/div[@class="structs"]/div[@class="struct"]/a'))]))
            lst.append(dataset_dictionary)
            driver.back()
        driver.find_element(By.XPATH,'//table[@class="table table-hover"]/tfoot/tr[1]/th[2]/ul/li/a/span[@class="glyphicon glyphicon-step-forward"]').click()
    driver.quit()
    return(lst)
         
    
    
    

if __name__ == '__main__':
    manager = Manager()
    dataset_dictionary=manager.dict()
    dataset_dictionary = {
    'article_title':[],
    'authors':[],
    'abstract':[],
    'structs':[],
    'tag':[]
    }
    lst=manager.list()
    pool= Pool(4)
    pool.starmap(extract_tag_data, zip(tags,repeat(dataset_dictionary),repeat(lst)))
    pool.close()
    df = pd.DataFrame.from_records(lst)
    df.to_excel(r"C:\\Users\\dell\\Desktop\\data collection\\myDataset.xlsx",  sheet_name='Sheet1')
    print(lst)
    
