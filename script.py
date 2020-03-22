import requests
from parsel import Selector
import datetime
import csv
import os

date_part = datetime.datetime.now().strftime('%d %b %Y %H_%M_%S')
output_csv_name = f'Output_{date_part}.csv'
input_file_name = 'scraper_input.csv'
img_folder = f'images_{date_part}'
try:
    os.makedirs(img_folder)
except:
    pass
row = ['Product SKU', 'Product Name', 'Product Brand',
       'Product Price', 'Image URLs seperated by Semicolon']
with open(output_csv_name, 'a', newline='') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(row)


def download_image(img_url, path_to_store):
    if img_url:
        r = requests.get(img_url)
        with open(path_to_store, 'wb') as img:
            img.write(r.content)


def scrape_product(product_url):
    print(f"Scraping {product_url}")
    r = requests.get(product_url)
    sel = Selector(r.text)
    product_sku = sel.xpath(
        '//div[@class="productSKU"]/dd[@class="productView-info-value"]/text()').extract_first()
    product_name = sel.xpath(
        '//div[@data-event-type="product"]/@data-name').extract_first()
    product_brand = sel.xpath(
        '//div[@data-event-type="product"]/@data-product-brand').extract_first()
    product_price = sel.xpath(
        '//div[@data-event-type="product"]/@data-product-price').extract_first()
    product_images = sel.xpath(
        '//li[contains(@class,"productView-thumbnail")]/a/@data-image-gallery-new-image-url').extract()
    for n, product_image in enumerate(product_images, start=1):
        download_image(product_image, f'{img_folder}/{product_sku}-{n}.jpg')
    product_images_str = ';'.join(product_images)
    return [product_sku, product_name, product_brand, product_price, product_images_str]


def get_all_product_url(search_url):
    all_products_url = []
    r = requests.get(search_url)
    while True:
        sel = Selector(r.text)
        all_products_url += sel.xpath(
            '//li[@class="product"]/article/div/div/h4/a/@href').extract()
        next_page_url = sel.xpath(
            '//li[contains(@class,"pagination-item--next")]/a/@href').extract_first()
        if next_page_url:
            r = requests.get(next_page_url)
            print(
                f"Products URLs Found:{len(all_products_url)} and moving to next page...")
        else:
            print(f"Total Products Found:{len(all_products_url)}")
            return all_products_url

with open(input_file_name, 'r') as infile:
    reader = csv.reader(infile)
    urls_to_scrape= [row[0] for row in list(reader)]

for search_url in urls_to_scrape[1:]:
    if not search_url:
        print('Might be a empty line skipping it...')
        continue
    all_products_url = get_all_product_url(search_url)
    print(f'Search URL: {search_url}')
    for product_url in all_products_url:
        row = scrape_product(product_url)
        with open(output_csv_name, 'a', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(row)
        print("Scraped and added to CSV...")
    with open('url_scraped.csv', 'a', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerow([search_url])
