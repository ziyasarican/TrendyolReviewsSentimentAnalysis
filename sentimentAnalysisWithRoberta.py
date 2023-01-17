#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 13:56:02 2022

@author: ziyasarican
"""

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

def loadPage():
    import time

    driver.get("https://www.trendyol.com/polygold/carbonn-led-aydinlatmali-mouse-seti-oyuncu-gamer-set-p-36385875/yorumlar?boutiqueId=612449&merchantId=439703")    # Web scrapper for infinite scrolling page 
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    
    i = 1
    
    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(1)
        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")  
        # Break the loop when the height we need to scroll to is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break
    
    
loadPage()

def findCommentSize():
    commentTemp = driver.find_element('xpath','//*[@id="rating-and-review-app"]/div/div[2]/div/div[2]/div[1]/div/div[2]/span[2]').text
    commentTemp = commentTemp.split(' ')
    commentSize = int(commentTemp[0])
    return commentSize


def getData2Csv():
    import pandas as pd
    import time

    #connect website    
    
    commentList = []
    starList = []
    
    # search in comments line
    # size should be commentSize*2 because each div elements count double
    
    unsuccessfulData = 0
    for i in range(1,findCommentSize()*2+1,2):  
        try:                     
            commentTemp = driver.find_element('xpath',f'//*[@id="rating-and-review-app"]/div/div[2]/div/div[2]/div[3]/div[4]/div[{i}]/div[1]/div/p').text
            commentList.append(commentTemp)
            print(commentTemp)
            a=0
            
            #search in stars
            for j in range(1,6):
                starTemp = driver.find_element('xpath',f'//*[@id="rating-and-review-app"]/div/div[2]/div/div[2]/div[3]/div[4]/div[{i}]/div[1]/div/span/div/div[{j}]/div[2]' ).get_attribute('style')
                #separate stars HTML tags
                starTemp = starTemp.split(';')
                starTemp = starTemp[0].split(': ')
                if starTemp[1] == '100%':
                    a=a+1
            starList.append(a)
        
        # different xpath,
        except:
            unsuccessfulData += 1
            pass
    
    #create dict
    dict = {'COMMENTS':commentList,'STARS':starList}
    df = pd.DataFrame(dict)
    df.to_csv('/Users/ziyasarican/Desktop/comments2.csv', index=False, encoding='utf-8')
    print(df)
    
getData2Csv()



def translateComments():
    from deep_translator import GoogleTranslator
    from googletrans import Translator
    import pandas as pd
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments2.csv")
    
    englishList = []
    
    
    # translateTemp = GoogleTranslator(src="tr",dest="en").translate(df.loc[101]['COMMENTS'])
    # print(translateTemp)
    
    for i in range (0,len(df)):
        try: 
            translateTemp = (GoogleTranslator(src="tr",dest="en").translate(df.loc[i]['COMMENTS'])).lower()
            englishList.append(translateTemp)
            print(i, " ", translateTemp)
        except:
            englishList.append(df.loc[101]['COMMENTS'])
    print(englishList)   
    df["English Comments"] = englishList
    df.to_csv('/Users/ziyasarican/Desktop/comments2.csv',index=False, encoding='utf-8')
    
translateComments()



def robertaModel():
    import pandas as pd
    from transformers import AutoTokenizer
    from transformers import AutoModelForSequenceClassification
    from scipy.special import softmax
    from transformers import pipeline

    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments2.csv")

    polarityList = []
    robertaModelStatusList = []
    for i in range(len(df)):
            
          encoded_text = tokenizer(df.loc[i]['English Comments'], return_tensors="pt")
          output = model(**encoded_text)
          score = output[0][0].detach().numpy()
          score = softmax(score)
          polarityList.append(score)
      
    df["Roberta Model Polarity"] = polarityList
        
    df.to_csv('comments2.csv', index=False, encoding='utf-8')
    
robertaModel()


def robertaModelResult():
    import pandas as pd
    import numpy as np 
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments2.csv")
    
    removeChar = "[]"
    
    statusList = []
    count = 0
    for i in range(len(df)):
        score = df.loc[i]['Roberta Model Polarity']
        for remove in removeChar:
            score = score.replace(remove,"")
        
        score = np.fromstring(score, dtype=float, sep=" ")
        
# Score should be far from 5x to others
# Score should be very close each other so I used 'non'
        if (score[0] > 0.80):
            statusList.append("Negative")
        elif (score[1] > 0.80):
            statusList.append("Neutral")
        elif (score[2] > 0.80):
            statusList.append("Positive")
        elif (score[0] < 0.20):
            statusList.append("Non Negative")
        elif (score[2] < 0.20):
            statusList.append("Non Positive")
        else:
            count += 1
            statusList.append("Cannot Find")
         
    df["Roberta Model Status"] = statusList
    df.to_csv('/Users/ziyasarican/Desktop/comments2.csv', index=False, encoding='utf-8')

robertaModelResult()  

def compareRobertaAndStars():
    import pandas as pd
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments2.csv")
    
    robertaResultList = []
    
    
    for i in range(len(df)):
        
        status = df.loc[i]['Roberta Model Status']
        star = df.loc[i]['STARS']
        
        if (status == "Cannot Find"):
            robertaResultList.append("False")
        elif ((status == "Positive") or (status == "Non Negative")):
            if(star >= 3):
                robertaResultList.append("True")
            else:
                robertaResultList.append("False")
        elif ((status == "Negative") or (status == "Non Positive")):
            if(star <= 3):
                robertaResultList.append("True")
            else:
                robertaResultList.append("False")
        else:
            if (star == 3):
                robertaResultList.append("True")
            else:
                robertaResultList.append("False")
        
    df["Roberta Result"] = robertaResultList
    df.to_csv('/Users/ziyasarican/Desktop/comments2.csv', index=False, encoding='utf-8') 
    
compareRobertaAndStars()

def plotRobertaResult():
    import pandas as pd
    import matplotlib.pyplot as plt   
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments2.csv")
    
    ax = df["Roberta Result"].value_counts()
    labels = "False", "True"
    sizes = [ax[0],ax[1]]
    
    plt.pie(sizes,labels=labels,autopct='%1.1f%%')
    plt.title("Roberta Result")
    plt.figsize = 10,5 
plotRobertaResult()


def falseResult2Csv():
    import pandas as pd
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments2.csv")
    
    result = df[(df["Roberta Result"] == 0)][["COMMENTS","STARS","English Comments","Roberta Model Polarity","Roberta Model Status"]]
    result.to_csv('/Users/ziyasarican/Desktop/falseStatus2-.csv', index=False, encoding='utf-8') 
falseResult2Csv()
