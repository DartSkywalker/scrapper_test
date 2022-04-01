import bs4.element
import xlsxwriter
from spiders.fastcomet_spider import FastcometSpider
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.signalmanager import dispatcher


def save_urls(spider_results):
    urls_list = []
    for dict_data in spider_results:
        for key, value in dict_data.items():
            urls_list.append(value)

    # Save urls_list to file
    with open('urls.txt', 'w') as f:
        for item in urls_list:
            f.write("%s\n" % item)


def crawl_website():
    results = []

    def crawler_results(signal, sender, item, response, spider):
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_scraped)

    process = CrawlerProcess(get_project_settings())
    process.crawl(FastcometSpider)
    process.start()

    save_urls(results)


def extract_data_from_url():
    # Get all urls from urls.txt to list
    with open('urls.txt', 'r') as f:
        urls_list = f.readlines()
    urls_list = [x.strip() for x in urls_list]
    url_len = len(urls_list)

    data_list = []

    # Get data from each url
    for i, url in enumerate(urls_list):
        print(f"Processing {i+1}/{url_len}")

        # Get title of the url using bs4
        import requests
        from bs4 import BeautifulSoup
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        try:
            title = soup.find('title').text
        except AttributeError:
            title = ""

        # Get H1 tag of the url using bs4
        try:
            h1 = soup.find_all('h1')
            for tag in h1:
                if "Web Hosting Deals" not in tag.text:
                    h1 = tag.text
            if isinstance(h1, bs4.element.ResultSet):
                h1 = "Web Hosting Deals"

        except AttributeError:
            h1 = ''

        data_list.append([url, title, h1])
        # Export result to csv file in format - Page Url, Page Title, H1 tag text
        # with open('data.csv', 'a') as f:
        #     try:
        #         # f.write("%s,%s,%s\n" % (url, title, h1))
        #         if "," in h1:
        #             f.write(f'{url},{title},"{h1}"\n')
        #         else:
        #             f.write(f'{url},{title},{h1}\n')
        #     except UnicodeEncodeError:
        #         continue

    with xlsxwriter.Workbook('data.xlsx') as workbook:
        worksheet = workbook.add_worksheet()

        for row_num, data in enumerate(data_list):
            worksheet.write_row(row_num, 0, data)

    print("Data successfully extracted and saved to data_old.csv")


def main():
    crawl_website()
    extract_data_from_url()


if __name__ == '__main__':
    main()
