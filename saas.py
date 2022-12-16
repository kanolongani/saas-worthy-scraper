import requests
from bs4 import BeautifulSoup
import pandas as pd


def getCategoryData(url_cat,pages):

    data_arr=[]
    cats_name = url_cat.split("/")[-1]
    print(cats_name)


    for page in range(1,pages+1):
        
        url=url_cat+"?page="+str(page)

        data = requests.get(url)
        soup =BeautifulSoup(data.content,'html.parser')
        kano=soup.find_all("div",class_="fndr-row saas_list")


        for x in kano:
            
            data_arr.append(informationScraper(x))

        print(data_arr)

    dataframe = pd.DataFrame(data_arr)
    dataframe.to_csv(cats_name+".csv",index=False)




def cleanText(raw_text):
    clean_text = raw_text.replace(",","").replace("(","").replace(")","")
    clean_text = clean_text.replace("Ratings","")
    clean_text = clean_text.strip()

    return clean_text


def informationScraper(single_division):
    information_json = {}
    information_json["Title"] = cleanText(single_division.find("h2").text)
    information_json["Rating Count"] = cleanText(single_division.find("span",class_="rat-count").text)

    return information_json

main_url="https://www.saasworthy.com"
res = requests.get(main_url)
soup =BeautifulSoup(res.content,'html.parser')
kano=soup.find("div",class_="allcatgry_wrp")

all_urls=kano.find_all("a")

for u in all_urls[:10]:
    print(main_url+u["href"])
    getCategoryData(url_cat=main_url+u["href"],pages=3)
    


