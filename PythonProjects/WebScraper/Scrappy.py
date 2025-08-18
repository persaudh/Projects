import requests
from bs4 import BeautifulSoup, ResultSet
import pprint


#element = soup.select(".score")
# for score in element:
#     scoreText = score.get_text()
#     scoreValue = int(scoreText.split()[0])
#     if(scoreValue > 100):
#         id = score["id"].split("score_")[1]
#         print(score,id)

#print(element[0])




def sort_stories_by_vote(hn_list):
    return sorted(hn_list, key= lambda k:k["votes"],reverse=True)

def create_custom_hn(links,subtext):
    hn = []
    for index, item in enumerate(links):
        vote = subtext[index].select(".score")
        if(len(vote)):
            score = vote[0].get_text().split()[0]
            scoreValue = int(score)
            if scoreValue > 100:
                title = links[index].getText()
                href = links[index].select("a")[0].get('href',None)
                hn.append({"title":title,"link":href,"votes":scoreValue})

    return sort_stories_by_vote(hn)

links = ResultSet(None)
subtext = ResultSet(None)
for i in range (1,5):
    res = requests.get(f"https://news.ycombinator.com/news?p={i}")
    soup = BeautifulSoup(res.text, "html.parser")

    links = links + soup.select(".titleline")
    subtext = subtext + soup.select(".subtext")

pprint.pprint(create_custom_hn(links=links,subtext=subtext))