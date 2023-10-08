import scrapy
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
import re

class NHSSpider(Spider):
    name = 'nhsscraper'
    start_urls = ['https://www.nhs.uk/conditions/']

    def parse(self, response):
        # Find all links without a class attribute
        links = response.xpath('//a[not(@class)]/@href').getall()

        # Loop through the links and follow them to extract content
        for link in links:
            yield response.follow(link, callback=self.parse_content)

    def clean(self, txt):
        txt = txt.replace("\n", "").replace(" ", " ")
        txt = re.sub(r'\s+', ' ', txt)
        return txt
    def parse_content(self, response):
        # Extract content from #maincontent
        sections = response.css('#maincontent section')
        # content = re.sub(r'[\n\s]+', '\n', main_content_text)

        # Extract the title of the page
        title = response.css('title::text').get()

        # Remove all non-text characters from the title and sanitize it
        sanitized_title = re.sub(r'[^\w\s]', '', title).replace('\n', '')

        # Append ".txt" at the end of the sanitized title
        filename = f"./content/{sanitized_title}.txt"

        data = ""
        for section in sections:
            h2 = section.css("h2:first-child")
            if h2:
                txt = h2.css('::text').get()
                txt = self.clean(txt)
                if txt == "Further information":
                    continue
                data += txt + "\n"
            txt = "".join(section.css("*:not(h2) *::text").getall())
            txt = self.clean(txt)
            data += txt + "\n"

        # Save the content to a .txt file
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(data)

if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(NHSSpider)
    process.start()
