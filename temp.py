
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())
PATH = "/Users/ziyasarican/Desktop/comments.csv"

def loadPage():
    import time

    driver.get("https://www.trendyol.com/xiomar/mi-20-000-mah-tasinabilir-sarj-cihazi-power-bank-p-166905041/yorumlar?boutiqueId=61&merchantId=667299")    # Web scrapper for infinite scrolling page 
    screen_height = driver.execute_script("return window.screen.height;")   # get the screen height of the web
    
    i = 1
    
    while True:
        # scroll one screen height each time
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
        i += 1
        time.sleep(0.25)
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
findCommentSize()

def getData2Csv():
    import pandas as pd
    
    commentList = []
    starList = []
    
    # search in comments line
    # size should be commentSize*2
    for i in range(1,findCommentSize()*2+1,2):  
        print("i: ",i)                      
        commentTemp = driver.find_element('xpath',f'//*[@id="rating-and-review-app"]/div/div[2]/div/div[2]/div[3]/div[4]/div[{i}]/div[1]/div/p').text
        commentList.append(commentTemp)
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
    
    #create dict
    dict = {'COMMENTS':commentList,'STARS':starList}
    df = pd.DataFrame(dict)
    df.to_csv('/Users/ziyasarican/Desktop/comments.csv', index=False, encoding='utf-8')
    print(df)
    
getData2Csv()

 

       



# Translate Turkish Comments
def translateComments():
    from googletrans import Translator
    import pandas as pd
    import time
    translator = Translator()
    
    df = pd.read_csv('/Users/ziyasarican/Desktop/comments.csv')
    englishList = []
    for i in range (0,len(df)):
        translateTemp = (translator.translate(df.loc[i]['COMMENTS'],src="tr",dest="en").text).lower()
        print(translateTemp)
        englishList.append(translateTemp)
        time.sleep(0.5)
    
    df["English Comments"] = englishList
    df.to_csv('/Users/ziyasarican/Desktop/comments.csv', encoding='utf-8')
    print(df)   
translateComments()

# Apply Vader Model to English Comments
def vaderModel():
    import pandas as pd
    import nltk
    nltk.download("vader_lexicon")
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sia= SentimentIntensityAnalyzer()
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    polarityList = []
    vaderModelStatusList = []
    for i in range (0,len(df)):
        polarityTemp = sia.polarity_scores(df.loc[i]['English Comments']).get("compound")
        polarityList.append(polarityTemp)
    
        if (polarityTemp > 0):
            vaderModelStatusList.append("Positive")
        elif (polarityTemp < 0 ):
            vaderModelStatusList.append("Negative")
        else:
            vaderModelStatusList.append("Neutral")
        
        
    df["Comments Polarity"] = polarityList
    df["Vader Model Status"] = vaderModelStatusList
    df.to_csv('/Users/ziyasarican/Desktop/comments.csv', encoding='utf-8')
vaderModel()




def compareVaderAndStars():
    import pandas as pd
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    vaderResultList = []
    
    
    for i in range(0,len(df)):
        if (df.loc[i]['STARS'] > 3 ):
            if (df.loc[i]['Vader Model Status'] == "Positive"):
                vaderResultList.append("True")
            else:
                vaderResultList.append("False")
        elif(df.loc[i]['STARS'] < 3 ):
            if (df.loc[i]['Vader Model Status'] == "Negative"):
                vaderResultList.append("True")
            else:
                vaderResultList.append("False")
        else:
            if (df.loc[i]['Vader Model Status'] == "Neutral"):
                vaderResultList.append("True")
            else:
                vaderResultList.append("False")
       
    df["Vader Result"] = vaderResultList
    df.to_csv('/Users/ziyasarican/Desktop/comments.csv', index=False, encoding='utf-8')        
compareVaderAndStars()        


def plotStars():
    
    import pandas as pd
    import matplotlib.pyplot as plt

    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    
    
    ax = df["STARS"].value_counts().sort_index().plot(kind="bar", title="Count of Reviews by Stars",figsize=(10,5)) 
    ax.set_xlabel("Review Stars")
    ax.set_ylabel("Number of Review")
    plt.show()
# plotStars()

def plotVaderResult():
    import pandas as pd
    import matplotlib.pyplot as plt   
    df = pd.read_csv("comments.csv")
    
    ax = df["Vader Result"].value_counts()
    labels = "False", "True"
    sizes = [ax[0],ax[1]]
    
    plt.pie(sizes,labels=labels,autopct='%1.1f%%')
    plt.title("Vader Result")
    plt.figsize = 10,5 
plotVaderResult()


def robertaModel():
    import pandas as pd
    from transformers import AutoTokenizer
    from transformers import AutoModelForSequenceClassification
    from scipy.special import softmax
    from transformers import pipeline

    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv"),

    
    polarityList = []
    robertaModelStatusList = []
    for i in range(len(df)):
      encoded_text = tokenizer(df.loc[i]['English Comments'], return_tensors="pt")
      output = model(**encoded_text)
      score = output[0][0].detach().numpy()
      score = softmax(score)
      polarityList.append(score)
    
      if(score[0] > score[1] and score[0] > score[2]):
        robertaModelStatusList.append("Negative")
      elif(score[1] > score[0] and score[1] > score[2]):
        robertaModelStatusList.append("Neutral")
      else:
        robertaModelStatusList.append("Positive")
      
    df["Roberta Model Polarity"] = polarityList
    df["Roberta Model Status"] = robertaModelStatusList
    df.to_csv('comments.csv', encoding='utf-8')
robertaModel()


def compareRobertaAndStars():
    import pandas as pd
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    robertaResultList = []
    
    
    for i in range(0,len(df)):
        print(i)
        if (df.loc[i]['STARS'] > 3 ):
            if (df.loc[i]['Roberta Model Status'] == "Positive"):
                robertaResultList.append("True")
            else:
                robertaResultList.append("False")
        elif(df.loc[i]['STARS'] < 3 ):
            if (df.loc[i]['Roberta Model Status'] == "Negative"):
                robertaResultList.append("True")
            else:
                robertaResultList.append("False")
        else:
            if (df.loc[i]['Roberta Model Status'] == "Neutral"):
                robertaResultList.append("True")
            else:
                robertaResultList.append("False")
       
    df["Roberta Result"] = robertaResultList
    df.to_csv('/Users/ziyasarican/Desktop/comments.csv', index=False, encoding='utf-8') 
    
compareRobertaAndStars()




def plotRobertaResult():
    import pandas as pd
    import matplotlib.pyplot as plt   
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    ax = df["Roberta Result"].value_counts()
    print(ax)
    labels = "False", "True"
    sizes = [ax[0],ax[1]]
    
    plt.pie(sizes,labels=labels,autopct='%1.1f%%')
    plt.title("Roberta Result")
    plt.figsize = 10,5 
plotRobertaResult()

def translateComments2():
    from deep_translator import GoogleTranslator
    from googletrans import Translator
    import pandas as pd
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    englishList = []
    
    for i in range (0,len(df)):
        translateTemp = (GoogleTranslator(src="tr",dest="en").translate(df.loc[i]['COMMENTS'])).lower()
        englishList.append(translateTemp)
        print(translateTemp)
    print(englishList)   
    df["English Comments 2"] = englishList
    df.to_csv('/Users/ziyasarican/Desktop/comments.csv',index=False, encoding='utf-8')
    
translateComments2()



def vaderModel2():
    import pandas as pd
    import nltk
    nltk.download("vader_lexicon")
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sia= SentimentIntensityAnalyzer()
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    polarityList = []
    vaderModelStatusList = []
    for i in range (0,len(df)):
        polarityTemp = sia.polarity_scores(df.loc[i]['English Comments 2']).get("compound")
        polarityList.append(polarityTemp)
    
        if (polarityTemp > 0):
            vaderModelStatusList.append("Positive")
        elif (polarityTemp < 0 ):
            vaderModelStatusList.append("Negative")
        else:
            vaderModelStatusList.append("Neutral")
        
        
    df["Comments Polarity 2"] = polarityList
    df["Vader Model Status 2"] = vaderModelStatusList
    df.to_csv('/Users/ziyasarican/Desktop/comments.csv', index=False, encoding='utf-8')
vaderModel2()


def compareVaderAndStars2():
    import pandas as pd
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    vaderResultList = []
    
    
    for i in range(0,len(df)):
        if (df.loc[i]['STARS'] > 3 ):
            if (df.loc[i]['Vader Model Status 2'] == "Positive"):
                vaderResultList.append("True")
            else:
                vaderResultList.append("False")
        elif(df.loc[i]['STARS'] < 3 ):
            if (df.loc[i]['Vader Model Status 2'] == "Negative"):
                vaderResultList.append("True")
            else:
                vaderResultList.append("False")
        else:
            if (df.loc[i]['Vader Model Status 2'] == "Neutral"):
                vaderResultList.append("True")
            else:
                vaderResultList.append("False")
       
    df["Vader Result 2"] = vaderResultList
    df.to_csv('/Users/ziyasarican/Desktop/comments.csv',index=False, encoding='utf-8')        
compareVaderAndStars2()  


def plotVaderResult2():
    import pandas as pd
    import matplotlib.pyplot as plt   
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    ax = df["Vader Result 2"].value_counts()
    labels = "False", "True"
    sizes = [ax[0],ax[1]]
    
    plt.pie(sizes,labels=labels,autopct='%1.1f%%')
    plt.title("Vader Result 2")
    plt.figsize = 10,5 
plotVaderResult2()  

def robertaModel2():
    import pandas as pd
    from transformers import AutoTokenizer
    from transformers import AutoModelForSequenceClassification
    from scipy.special import softmax
    from transformers import pipeline

    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv"),

    
    polarityList = []
    robertaModelStatusList = []
    for i in range(len(df)):
      encoded_text = tokenizer(df.loc[i]['English Comments 2'], return_tensors="pt")
      output = model(**encoded_text)
      score = output[0][0].detach().numpy()
      score = softmax(score)
      polarityList.append(score)
    
      if(score[0] > score[1] and score[0] > score[2]):
        robertaModelStatusList.append("Negative")
      elif(score[1] > score[0] and score[1] > score[2]):
        robertaModelStatusList.append("Neutral")
      else:
        robertaModelStatusList.append("Positive")
      
    df["Roberta Model Polarity 2"] = polarityList
    df["Roberta Model Status 2"] = robertaModelStatusList
    df.to_csv('comments.csv', index=False, encoding='utf-8')
robertaModel2()

def compareRobertaAndStars2():
    import pandas as pd
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    robertaResultList = []
    
    
    for i in range(0,len(df)):
        print(i)
        if (df.loc[i]['STARS'] > 3 ):
            if (df.loc[i]['Roberta Model Status 2'] == "Positive"):
                robertaResultList.append("True")
            else:
                robertaResultList.append("False")
        elif(df.loc[i]['STARS'] < 3 ):
            if (df.loc[i]['Roberta Model Status 2'] == "Negative"):
                robertaResultList.append("True")
            else:
                robertaResultList.append("False")
        else:
            if (df.loc[i]['Roberta Model Status 2'] == "Neutral"):
                robertaResultList.append("True")
            else:
                robertaResultList.append("False")
       
    df["Roberta Result 2"] = robertaResultList
    df.to_csv('/Users/ziyasarican/Desktop/comments.csv', index=False, encoding='utf-8') 
compareRobertaAndStars2()


def plotRobertaResult2():
    import pandas as pd
    import matplotlib.pyplot as plt   
    
    df = pd.read_csv("/Users/ziyasarican/Desktop/comments.csv")
    
    ax = df["Roberta Result 2"].value_counts()
    labels = "False", "True"
    sizes = [ax[0],ax[1]]
    
    plt.pie(sizes,labels=labels,autopct='%1.1f%%')
    plt.title("Roberta Result 2")
    plt.figsize = 10,5 
plotRobertaResult2()


def falseResult2Csv():
    import pandas as pd
    
    df = pd.read_csv(PATH)
    
    result = df[(df["Roberta Result 2"] == 0)][["COMMENTS","STARS","English Comments 2","Roberta Model Polarity 2"]]
    result.to_csv('/Users/ziyasarican/Desktop/falseStatus-.csv', index=False, encoding='utf-8') 
    print(result)
falseResult2Csv()