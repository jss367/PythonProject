import collections
import matplotlib.pyplot as plt
import bs4
import requests
import datetime
from datetime import *
import operator

url_list=['https://en.wikipedia.org/w/index.php?title=Keisha_Lance_Bottoms&action=history','https://en.wikipedia.org/w/index.php?title=Elizabeth_Warren&action=history','https://en.wikipedia.org/w/index.php?title=Val_Demings&action=history','https://en.wikipedia.org/w/index.php?title=Kamala_Harris&action=history','https://en.wikipedia.org/w/index.php?title=Michelle_Lujan_Grisham&action=history','https://en.wikipedia.org/w/index.php?title=Susan_Rice&action=history']
allcandidate={}
candidate=[]
cnt=[]
present = datetime.now()
past7 = present-timedelta(days=7)
datemask = "%Y-%m-%d"

def each_candidate(url): 
    #define a sub-function to extract name 
    def get_name(text):
        a=''
        for i in range(0,len(text)):
            if text[i]==':':
                break
            else:
                a+=text[i]
                i+=i
        return a
    
    #define a sub-function to find how many time the page has been editted in the recent week
    def one_week(r):
        new_r=[]
        r_recent=[]
        
        for i in range(0,len(r)):
            R[i]=r[i].strip()
            x=str(datetime.strptime(R[i],'%d %B %Y'))
            new_r.append(x[:10])
          
        #among the list of newly formatted date, find the recent one week 
        for i in range(0,len(new_r)):
            if datetime.strptime(new_r[i], datemask)>=past7:
                r_recent.append(new_r[i])
            elif datetime.strptime(new_r[i], datemask)<past7:
                break
                     
        return r_recent               

    #loop through main page to find all candidate wikipedia page, and print out its editting frequency   
    result=requests.get(url)
    result_soup=bs4.BeautifulSoup(result.text,"html.parser")
    a=result_soup.select('.mw-changeslist-date')
    R= []
   
    #loop through all items in the mw-changelist-date class and append dates into a new list R, R contain all edit dates 
    for i in range(0,len(a)):
        a1=a[i].text
        b1=a1[-15:].rsplit(',', 1)[-1]
        i+=i
        R.append(b1)
 
    r=one_week(R)
  
    #extract candidate name 
    text=result_soup.select('title')[0].getText()
    name=get_name(text)
    
    occurrences = collections.Counter(R)
    
    print(name)
    print(f"The total times is {len(one_week(R))} \n")
    plt.figure(figsize=(30,3))
    plt.title(f'{name} - Editing frequency ')
    plt.bar(occurrences.keys(),occurrences.values(),align='edge',width=0.3)

    candidate.append(name)
    cnt.append(len(one_week(R)))

print("Please see below the list of democratic VP candidates for the 2020 election, and the total editing times of their Wikipedia page in the most recent one week.\n")    
for url in url_list:
    each_candidate(url)
      
allcandidate=dict(zip(candidate,cnt))  
max_key = max(allcandidate, key=allcandidate.get)
print(f"\nThe current's time is {present}\n")
print(f"Based on the total editing times for each candidate's Wikipedia page in the most recent week, I would like to predict that the next democratic VP is {max_key}\n")
print("Below is a chart showing the editing frequency for the most recent 50 edits for each candidate. ")
