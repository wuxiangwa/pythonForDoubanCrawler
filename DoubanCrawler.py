import requests
import expanddouban
from bs4 import BeautifulSoup
from operator import itemgetter, attrgetter

"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
def getMovieUrl(category, location):
    url = 'https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影'
    url = url + ',' + category + ',' + location
    return url

"""
return locations.
"""
locations = [
'大陆', '美国', '香港', '台湾', '日本' , '韩国', '英国', '法国', '德国', '意大利', '西班牙', '印度', '泰国', '俄罗斯', '伊朗', '加拿大', '澳大利亚', '爱尔兰', '瑞典', '巴西', '丹麦'
]

"""
电影类的构造函数
"""
class Movie:
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link

    def getMovieDetail(self):
        return {
            'name': self.name,
            'rate': self.rate,
            'location': self.location,
            'category': self.category,
            'info_link': self.info_link,
            'cover_link': self.cover_link
        }



"""
return a list of Movie objects with the given category and location.
"""

def getMovies(category, location):
    url = getMovieUrl(category, location)
    html = expanddouban.getHtml(url, True)
    soup = BeautifulSoup(html, "html.parser")

    content_div = soup.find(id="app").find(class_="list-wp")
    list = []
    for element in content_div.find_all("a", recursive=False):

        category = category
        location = location
        info_link = element.get('href')
        cover_link = element.div.span.img.get('src')
        name = element.p.find(class_="title").text
        rate = element.p.find(class_="rate").text

        m = Movie(name, rate, location, category, info_link, cover_link).getMovieDetail()
        list.append(m)

    return list

movies_all = {
    '剧情': {
        'number': 0,
        'list': []
    },
    '科幻': {
        'number': 0,
        'list': []
    },
    '悬疑': {
        'number': 0,
        'list': []
    }

}

for category in ['剧情','科幻', '悬疑']:
    for location in locations:
        print(location, category)
        list = getMovies(category, location)
        if category == '剧情':
            movies_all[category]['list'].append((location,len(list)))
            movies_all[category]['number'] += len(list)
        elif category == '科幻':
            movies_all[category]['list'].append((location,len(list)))
            movies_all[category]['number'] += len(list)
        elif category == '悬疑':
            movies_all[category]['list'].append((location,len(list)))
            movies_all[category]['number'] += len(list)

        with open('movies.csv','a') as f:
            for item in list:
                f.write("{},{},{},{},{},{}".format(item['name'], item['rate'], item['location'], item['category'], item['info_link'], item['cover_link']) + '\n')


with open('output.txt','a') as f:
    for key in movies_all:
        if len(movies_all[key]['list']) >= 3:
            list = movies_all[key]['list']
            number = movies_all[key]['number']
            topThree = sorted(list, key=itemgetter(1))[-1:-4:-1]

            percentage1 = round(int(topThree[0][1])/int(number)*100, 2)
            percentage2 = round(int(topThree[1][1])/int(number)*100, 2)
            percentage3 = round(int(topThree[2][1])/int(number)*100, 2)

            f.write('{}类电影中排名前三的地区为{}、{}、{},分别占此类电影总数的百分比为{}%、{}%、{}%\n'.format(
                key,
                topThree[0][0],
                topThree[1][0],
                topThree[2][0],
                percentage1,
                percentage2,
                percentage3
            ))
