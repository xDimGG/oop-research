from pyquery import PyQuery as pq
import urllib

def scrape(url):
	d = pq(url=url)
	el = d('dt:contains("Direct Known Subclasses:")')
	if len(el) == 0:
		return []

	for e in el.next().children():
		e = pq(e)
		path = e.attr('href')
		yield e.text()
		yield from scrape(urllib.parse.urljoin(url, path))

print(list(scrape('https://docs.oracle.com/javase/8/docs/api/java/lang/Exception.html')))
