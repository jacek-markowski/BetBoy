#!usr/bin/env python
import urllib2
import re

with open('links.txt','r') as files:
    links = files.readlines()

for url in links:
    source = urllib2.urlopen(url).read()
    url_split = url.split('/')
    print url_split[:]
    re_patternA ='<a href="/soccer/%s/(?P<link>.*?/).*?>'%url_split[-2]
    print re_patternA
    check = re.compile(re_patternA, re.DOTALL)
    search = check.findall(source)
    with open('betexplorer/%s' %url_split[-2], 'w') as league:
        for i in range(1, len(search[:-1])):
            path = search[i].split('/')
            name_league = url_split[-2] + '_'+path[-2]
            line = name_league +' '+url[:-1]+search[i]+'\n'
            if (not 'cup' in path[-2]) and (not 'trophy' in path[-2]):
                league.write(line)
