import browser
import lxml.html
from prettytable import PrettyTable
 
# Open some site, let's pick a random one, the first that pops in mind:
# assign depth, how many pages do you want to scrape...
# get the news time, and title
 
x = PrettyTable(["News", "time", "stock"])
 
for i in range(5):
 
        i = str(i + 1)
        r = browser.open('http://newsletter.hotstocked.com/newsletters/index/page-' + i)
        doc = lxml.html.parse(r).getroot()
 
        listItem = doc.cssselect(".nl-single-title")
        for item in listItem:
                 title = item.cssselect("a")[0].text_content().strip()
                 date = item.cssselect(".nl-single-date")[0].text_content()
                 x.add_row([title, date, '---']);
print x
