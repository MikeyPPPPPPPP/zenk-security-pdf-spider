from bs4 import BeautifulSoup
#from requests.utils import quote
import requests
import json

ROOTURL = "https://repo.zenk-security.com/"

MASTSER = {}

class web_spider:
    """This class will download the files from a website"""
    def __init__(self):
        self.path_gone_through = []



    def requester(self, url: str) -> str:
        """this is a seprete function that will allow us to add headers and proxys when we need to"""
        req = requests.get(url)#, headers={'User-Agent':"fasd"})
        return req.text


    def get_hrefs(self, url: str) -> list[str]:
        """this will scrap a page for hrefs"""
        urls = []
        soup = BeautifulSoup(self.requester(url), "lxml")
        for uri in soup.find_all('a', href=True):
            urls.append(uri['href'])
        return urls


    def process_urls(self, urls: list) -> list[str]:
        """this will return a list of urlencode urls in a list"""
        return ['https://repo.zenk-security.com/?dir='+x for x in [x[5:] for x in urls if '?dir=.' in x] if ROOTURL not in x]

    def not_a_file_uri(self, url: str) -> str:
        #url = ''
        if not url.startswith('https://repo.zenk-security.com/'):
            #print('\t\t\t\t\t'+ROOTURL+url)
            return ROOTURL+url
        return url

    def recursion(self, url: list[str]) -> list[str]:
        """This will use recursion to get a urls"""
        urls = []
        soup = BeautifulSoup(self.requester(url), "lxml")
        for uri in soup.find_all('a', href=True):
            if uri['href'].split('/')[-1].endswith('.pdf'):# this will print if there is a .pdf in the url
                urls.append(url[0:31] + url[38:] + '/' + uri['href'].split('/')[-1])#quote(uri['href'].split('/')[-1]))
                pass

            elif '.' in uri['href'][-6:]:
                pass

            elif uri['href'].split('/')[-1].endswith('.pdf') == False:
                if self.not_a_file_uri(uri['href']) not in self.path_gone_through:

                    #print('atemptting recursion')
                    self.path_gone_through.append(self.not_a_file_uri(uri['href']))

                    self.recursion(self.not_a_file_uri(uri['href']))
                else:
                    pass
        
        if url not in MASTSER:
            MASTSER[url] = urls

        return urls



t = web_spider()
s = t.get_hrefs(ROOTURL)
s = t.process_urls(s)

for x in s:
    t.recursion(x)


with open("sample.json", "w") as outfile:
    json.dump(MASTSER, outfile, indent=4)