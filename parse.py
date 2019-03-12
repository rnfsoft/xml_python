import xml.etree.ElementTree as ET

tree= ET.parse('movies.xml')
root = tree.getroot()

print (root.tag) # collection
print (root.attrib) # {}

for child in root:
    print(child.tag, child.attrib) # genre {'category': 'Action'}

print([elem.tag for elem in root.iter()]) # ['collection', 'genre', 'decade', 'movie', 'format', 'year', 'rating', 'description', 'movie',

for movie in root.iter('movie'):
    print (movie.attrib) # {'favorite': 'True', 'title': 'Indiana Jones: The raiders of the lost Ark'} <- <movie favorite="True" title="Indiana Jones: The raiders of the lost Ark"> 

for description in root.iter('description'):
    print(description.text) # Marty McFly <- <description>Marty McFly</description>

for movie in root.findall("./genre/decade/movie/[year='1992']"):
    print(movie.attrib) # {'favorite': 'True', 'title': 'Batman Returns'} <- <movie favorite="False" title="Reservoir Dogs">

for movie in root.findall("./genre/decade/movie/format/[@multiple='Yes']"): # @ (attribute) = 'Yes'
    print(movie.attrib) # {'multiple': 'Yes'}

for movie in root.findall("./genre/decade/movie/format/[@multiple='Yes']..."): # ... = parent element of the current element
    print(movie.attrib) # {'favorite': 'True', 'title': 'THE KARATE KID'}

b2tf = root.find("./genre/decade/movie/[@title='Back 2 the Future']") # both working./genre/decade/movie[@title='Back 2 the Future']
print (b2tf.attrib) # {'favorite': 'False', 'title': 'Back 2 the Future'}
b2tf.attrib["title"] = "Back to the Future"
print(b2tf.attrib) # {'favorite': 'False', 'title': 'Back to the Future'}
tree.write("movies_cleanup.xml")
tree = ET.parse('movies_cleanup.xml')
root = tree.getroot()
for movie in root.iter("movie"):
    print(movie.attrib) # {'favorite': 'False', 'title': 'Back to the Future'}

for form in root.findall("./genre/decade/movie/format"):
    print(form.attrib, form.text) # {'multiple': 'Yes'} DVD,Online

import re
for form in root.findall("./genre/decade/movie/format"):
    match = re.search(',', form.text) # search for the commas
    if match:
        form.set('multiple', 'Yes')
    else:
        form.set('multiple', 'No')
tree.write("movies_cleanup.xml")
tree = ET.parse('movies_cleanup.xml')
root = tree.getroot()
for form in root.findall("./genre/decade/movie/format"):
    print(form.attrib, form.text) # {'multiple': 'Yes'} dvd, digital

for decade in root.findall("./genre/decade"):
    print (decade.attrib) # {'years': '1980s'}
    for year in decade.findall("./movie/year"):
        print (year.text) # 1986

for movie in root.findall("./genre/decade/movie/[year='2000']"):
    print (movie.attrib) # {'favorite': 'False', 'title': 'X-Men'}

action = root.find("./genre[@category='Action']")
new_dec = ET.SubElement(action, 'decade')
new_dec.attrib["years"] = '2000s' # <decade years="2000s" />
xmen = root.find("./genre/decade/movie[@title='X-Men']")
dec2000s = root.find("./genre[@category='Action']/decade[@years='2000s']")
dec2000s.append(xmen) # adding xmen to 2000s
dec1990s = root.find("./genre[@category='Action']/decade[@years='1990s']")
dec1990s.remove(xmen) # removing xmen from 1990s
tree.write("movies_cleanup.xml")

print(ET.tostring(root, encoding='utf8').decode('utf8'))