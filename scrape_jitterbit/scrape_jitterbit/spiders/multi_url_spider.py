from scrapy import Spider
import os



class MultiUrlSpider(Spider):
    name = "multi_url_spider"
    
    url_list = []
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    
    file_path = os.path.join(current_dir,"links.txt")
    
    with open(file_path,"r") as filestream:
        for line in filestream:
            url_list.extend(line.split(","))

    # List of URLs you want to scrape
    start_urls = url_list

    def parse(self, response):
        # Extract the text content from the page
        page_text = response.xpath("//body//text()").getall()
        cleaned_text = ''.join(page_text).strip()

        # Save or process the extracted data
        yield {
            'url': response.url,
            'text': cleaned_text
        }
