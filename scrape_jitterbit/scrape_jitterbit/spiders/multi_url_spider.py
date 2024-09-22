from scrapy import Spider

url_list = []

with open("alldocslinks.txt","r") as filestream:
    for line in filestream:
        url_list.extend(line.split(","))

class MultiUrlSpider(Spider):
    name = "multi_url_spider"

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
