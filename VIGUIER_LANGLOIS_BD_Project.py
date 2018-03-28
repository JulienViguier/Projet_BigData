def get_jobs(city, money, tech):
    if tech == 'c#':
        tech = 'c%23'
    elif tech == 'c++':
        tech = 'c%2B%2B'
    url_test = 'https://stackoverflow.com/jobs/feed?l='+str(city)+'&u=Km&d=20&s='+str(money)+'&c=EUR&tl='+str(tech)
    print(url_test)
    url = urllib.request.urlopen(url_test)
    return url
                                 
def get_weather(city):
    url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city +'&mode=json&units=metric&APPID=786b264284a5fd8ff885525aea085ba0')
    data = json.loads(url.read().decode('utf-8'))
    url.close()
    return data

def create_tree(xml_file):
    parsed_xml = et.parse(xml_file).getroot()
    category_list = []
    link_list = []
    name_list = []
    title_list = []
    desc_list = []
    pubdate_list = []
    location_list = []
    global category, link, name, title, desc, pubdate, location, num_node, num
    
    for node in parsed_xml:
        namespace_r = {'os': 'http://a9.com/-/spec/opensearch/1.1/'}
        num_node = node.find('os:totalResults', namespace_r)
        num = get_node(num_node)
        
        for x in node.findall('item'):
            namespace = {'a10': 'http://www.w3.org/2005/Atom'}
            link = x.find('link')
            name = x.find('a10:author/a10:name', namespace)
            category = x.findall('category')
            title = x.find('title')
            desc = x.find('description')
            pubdate = x.find('pubDate')
            location = x.find('{http://stackoverflow.com/jobs/}location')
            
        for i in range(0, len(category)):  
            category_list.append(get_node(category[i]))
        link_list.append(get_node(link))
        name_list.append(get_node(name))
        title_list.append(get_node(title))
        desc_list.append(get_node(desc))
        pubdate_list.append(get_node(pubdate))
        location_list.append(get_node(location))
    if(int(num) > 0):
        print('Techno utilisees: '+str(category_list))
        print('Entreprise: '+str(name_list))
        print('Intitule: '+str(title_list))
        print('Description: '+str(link_list))
        print('Date de publication: '+str(pubdate_list))
        print('Lieu: '+str(location_list))
    else:
        print('Aucun resultat disponible pour cette ville/technologie')
    
    
def get_node(n):
    if(n is not None):
        return n.text
    
def orgnz_weather_data(data):
    n_data = dict(
        city = data.get('name'),
        country = data.get('sys').get('country'),
        main_temp = data.get('main').get('temp'),
        main_press = data.get('main').get('pressure'),
        main_humidity = data.get('main').get('humidity'),
        wind = data.get('wind').get('speed'),
        clouds = data.get('clouds').get('all'),
        desc = data.get('weather')
    )
    return n_data
                
def print_weather_data(n_data):
    print('*********************************')
    print('Ville: {}'.format(n_data['city']))
    print('Pays: {}'.format(n_data['country']))
    print('Temperature actuelle: {}'.format(n_data['main_temp'])+'\xb0'+'C')
    print('Pression atmospherique: {}'.format(n_data['main_press'])+'hpa')
    print('Humidite: {}'.format(n_data['main_humidity'])+'%')
    print('Vitesse du vent: {}'.format(n_data['wind']))
    print('Nuage: {}'.format(n_data['clouds'])+'%')
    print('Description: {}'.format(n_data['desc']))
    
import urllib.request
import json, requests, xml
import xml.etree.ElementTree as et

global s
fav_techs = []
cities = ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Reims', 'Lille']
techs = ['javascript', 'sql', 'java', 'c#', 'python', 'php', 'c++', 'c', 'typescript', 'ruby', 'swift']
for z in range(0, 11):
    print(techs[z])
print("\n")
for x in range(0, 3):
    while True:
        fav_techs.insert(x, input('Saisir votre language prefere parmi ceux listes: '))
        if fav_techs[x] not in techs:
            print("Ce langage de programmation n'est pas disponible, reessayez. ")
            print(fav_techs[x])
            continue
        else:
            break

s = int(input('Salaire minimum (/an): '))
for c in cities:
    print_weather_data(orgnz_weather_data(get_weather(c)))
    for d in fav_techs:
        create_tree(get_jobs(c, s, d))
