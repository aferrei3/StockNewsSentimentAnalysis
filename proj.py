# Import libraries
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
from textblob import TextBlob
from InvestopediaApi import ita
from tkinter import *
import tkinter as tk




class TickerSent:
    def __init__(self):
        self.ticker = ''
        self.sentiment = 0.0






CAP_ALPHA = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

URL_0 = 'https://seekingalpha.com/market-news/top-news'

URL_1 = 'https://seekingalpha.com/market-news/all'

URL_2 = 'https://seekingalpha.com/market-news/energy'

URL_3 = 'https://seekingalpha.com/market-news/healthcare'

URL_4 = 'https://seekingalpha.com/market-news/on-the-move'







def findHyperLinks(url):

    hyper_link_list = getHtmlElements(url,'a')
    
    return hyper_link_list

def findTickersInHyperLinks(hyper_link_list):

    tickers_in_site = list()

    listed_tickers = getTickers()

    for i in listed_tickers:
        if i in hyper_link_list:
            tickers_in_site.append(i)

    return tickers_in_site




def getTickers():
    all_listed = open("tickers.txt", "r+")
    all_tickers = all_listed.readlines()
    ticker_list = list()
    for i in all_tickers:
        x = i.rstrip('\n')

        ticker_list.append(x)
    
    all_listed.close()

    return ticker_list



def getHtmlElements(url,data_type_as_str):

        # Set the URL you want to webscrape from
    #url = 'https://seekingalpha.com/market-news/top-news'

    # Connect to the URL
    response = requests.get(url)

    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")
    link_list = list()
    
    for i in range(len(soup.findAll(data_type_as_str))): #'a' tags are for links
        one_a_tag = soup.findAll(data_type_as_str)[i]
        link_list.append(one_a_tag.text) 
       # print(one_a_tag)

    return link_list

def getText(text_list,url):


    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    new_text = soup.text
    li_list = new_text.split('|')

    news_list = list()
    
    #print(new_list)
    for i in li_list:
        i_index = li_list.index(i)
        #print(i_index)
        if 'Comments' in i:
            print(i)
            print('\n')
            news_list.append(i)
        else:
            print('', end = '')
        

    return news_list



def getSentiment(news_list,url):

    hyper_link_tickers = findTickersInHyperLinks(url)

    ticker_list = getTickers()



    hyper_link_tickers = findHyperLinks(url)

    ticker_sentiment_dict = dict()

    for i in news_list:
        li_element = TextBlob(i)

        for sentence in li_element.sentences:
            if 'ETF' not in sentence:
                for j in ticker_list:
                    if j in sentence:
                        if j in hyper_link_tickers:
                            if len(j) > 1:

                                if j in ticker_sentiment_dict:
                                    x = ticker_sentiment_dict[j]
                                    x += sentence.sentiment.polarity
                                    ticker_sentiment_dict[j] = x
                                else:
                                    ticker_sentiment_dict[j] = sentence.sentiment.polarity



            

    return ticker_sentiment_dict


##################################ROBINHOOD#######################################







        

def loadListSentiment(url):



    news_list = getHtmlElements(url,'li')
    '''
    for i in news_list:
        print(i)
        print('\n')
        '''

    sentiment_ticker_dict = getSentiment(news_list,url)
    #print(sentiment_ticker_dict)
    return sentiment_ticker_dict

    











class Application(tk.Frame,TickerSent):


    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        


        

    def create_widgets(self):

        self.List1 = tk.Text(root, height=2, width=30)
        self.List1.pack()
        self.List1.config(width=100, height=200)
        self.List1.insert(tk.END, "This program will tell you the sentiment of seeking alph\
a(a popular market news site) on a particular   stock \
based on whats on their website. The   sentiment of any given \
news article for a stock will range from negative  one to positive one. If a stock occurs\
 more than once the sentiment will  be added to the previous sentiment. \
 The module used \
 to derive sentiment from any given article is TextBlob which derives from the natural\
 language tool kit a python library which facilitates working with a language in\
     programming through the use of machine learning. In order to use this      press the \
remove button\
 then press any of the News buttons to bring up the sentiment for \
 all stocks on that given page on\
 seeking alpha.\
 In order to close the window press the red quit button or\
 the X in the top right      corner. Generally the better the sentiment the better  the\
 stock is doing. However the natural language tool kit was did not use\
 stock news as its   training model. A future improvement to this would include\
 training a     machine learning model on stock news rather than tweets which is\
 what the natural language toolkit was trained on, and is better suited for. Keep in\
 mind this is not accurate by any means at prediciting or assessing a stocks performance\
 and is mainly a prototype which could be improved on. Also  note that time between\
 pressing the button and executing the function will take a second or two since\
 webscraping the webpage takes a bit of time.")


        self.top_news = tk.Button(self)
        self.top_news["text"] = "Seeking Alpha\nTop Market News"

        self.top_news["command"] = self.Link1
        self.top_news.pack(side="left")

        self.all_news = tk.Button(self)
        self.all_news["text"] = "Seeking Alpha\nAll Market News"

        self.all_news["command"] = self.Link2
        self.all_news.pack(side="left")


        self.energy_news = tk.Button(self)
        self.energy_news["text"] = "Seeking Alpha\nEnergy News"

        self.energy_news["command"] = self.Link3
        self.energy_news.pack(side="left")


        self.health_news = tk.Button(self)
        self.health_news["text"] = "Seeking Alpha\nHealthcare News"

        self.health_news["command"] = self.Link4
        self.health_news.pack(side="left")


        self.move_news = tk.Button(self)
        self.move_news["text"] = "Seeking Alpha\nOn the Move "

        self.move_news["command"] = self.Link5
        self.move_news.pack(side="left")


        # self.remove = tk.Button(self)
        # self.remove["text"] = "Remove List"

        # self.remove["command"] = self.remove_list
        # self.remove.pack(side="left")





        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")
        #self.data = loadListSentiment(URL_0)

        # self.x = self.data

        # # self.w = Label(self, text = self.x)
        # # self.w.pack(side='left')
        # self.List1 = Listbox(self.master)
        # # self.List1.insert(1,'ppppp')
        # self.List1.pack()
        # for key in self.x:
        #     self.List1.insert(END, '{}: {}'.format(key, self.x[key]))

    def remove_list(self):
        # self.List1.delete(0,tk.END)
        self.List1.pack_forget()    

    def Link1(self):
        self.remove_list()
        self.data = loadListSentiment(URL_0)
        self.x = self.data

        # self.w = Label(self, text = self.x)
        # self.w.pack(side='left')
        self.List1 = Listbox(self.master)
        self.List1.config(width=100, height=200)
        # self.List1.insert(1,'ppppp')
        self.List1.pack()

        for key in self.x:
            self.List1.insert(END, '{}: {}'.format(key, self.x[key]))

    def Link2(self):
        self.remove_list()
        self.data = loadListSentiment(URL_1)
        self.x = self.data

        # self.w = Label(self, text = self.x)
        # self.w.pack(side='left')
        self.List1 = Listbox(self.master)
        self.List1.config(width=100, height=200)
        # self.List1.insert(1,'ppppp')
        self.List1.pack()
        for key in self.x:
            self.List1.insert(END, '{}: {}'.format(key, self.x[key]))

    def Link3(self):
        self.remove_list()
        self.data = loadListSentiment(URL_2)
        self.x = self.data

        # self.w = Label(self, text = self.x)
        # self.w.pack(side='left')
        self.List1 = Listbox(self.master)
        self.List1.config(width=100, height=200)
        # self.List1.insert(1,'ppppp')
        self.List1.pack()
        for key in self.x:
            self.List1.insert(END, '{}: {}'.format(key, self.x[key]))


    def Link4(self):
        self.remove_list()
        self.data = loadListSentiment(URL_3)
        self.x = self.data

        # self.w = Label(self, text = self.x)
        # self.w.pack(side='left')
        self.List1 = Listbox(self.master)
        self.List1.config(width=100, height=200)
        # self.List1.insert(1,'ppppp')
        self.List1.pack()
        for key in self.x:
            self.List1.insert(END, '{}: {}'.format(key, self.x[key]))



    def Link5(self):
        self.remove_list()
        self.data = loadListSentiment(URL_4)
        self.x = self.data

        # self.w = Label(self, text = self.x)
        # self.w.pack(side='left')
        self.List1 = Listbox(self.master)
        self.List1.config(width=100, height=200)
        # self.List1.insert(1,'ppppp')
        self.List1.pack()
        for key in self.x:
            self.List1.insert(END, '{}: {}'.format(key, self.x[key]))

    



root = tk.Tk()
root.geometry("600x500")
app = Application(master=root)
app.mainloop()







#APP-3433-MLXX



