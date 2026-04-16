import main
import urllib.request
import xml.etree.ElementTree as ET

feed = main.LIVE_NEWS_FEEDS[0]
req = urllib.request.Request(feed["url"], headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, timeout=8) as response:
    xml_data = response.read()

root = ET.fromstring(xml_data)
items = root.findall('./channel/item')

for item in items[:2]:
    t1 = item.find('title')
    t2 = item.find('{http://www.w3.org/2005/Atom}title')
    title_el = t1 if t1 is not None else t2
    
    l1 = item.find('link')
    l2 = item.find('{http://www.w3.org/2005/Atom}link')
    link_el = l1 if l1 is not None else l2
    
    title = title_el.text if title_el is not None and title_el.text else "Unknown Title"
    link = link_el.text if link_el is not None and link_el.text else (link_el.get("href", "") if link_el is not None else "")
    
    print("Title:", title)
    print("Link:", link)
