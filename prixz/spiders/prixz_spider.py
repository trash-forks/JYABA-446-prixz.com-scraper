from pyexpat import model
import scrapy
import datetime


#scrapy.spiders.SitemapSpider
class PrixzSpider(scrapy.spiders.SitemapSpider):
    name = 'prixz'
    sitemap_urls = ['https://prixz.com/sitemap_index.xml']
    sitemap_rule = [
        ('/c/', 'parse'),
    ]
    #start_urls = ['https://prixz.com/c/farmacia/alta-especialidad/antivirales-alta-especialidad/atazanavir-sago-300mg-capsula-30/']

    def parse(self, response):
        title = response.xpath("//h1[contains(@class,'product_title')]/text()").extract_first()
        stock = response.xpath("//div[contains(@class,'stock_disponible')]/b/text()").extract_first()
        price = response.xpath("//div[@class='summary entry-summary']//span[contains(@class,'woocommerce-Price-amount')]/bdi/text()").extract_first()
        sale_price =  response.xpath("//div[@class='summary entry-summary']//ins/span[contains(@class,'woocommerce-Price-amount')]/bdi/text()").extract_first()
        shipment_cost = response.xpath("//svg[contains(@class,'ui-pdp-icon--truck')]/parent::figure/following-sibling::div/p/text()").extract_first()
        sku = response.xpath('//span[@class="sku"]/text()').extract_first()
        presenticion = response.xpath('//p[contains(text(),"Presentación")]/parent::td/following-sibling::td/p/text()').extract_first()
        image_url =  response.xpath("//a[contains(@class,'woocommerce-main-image')]/@href").extract_first()
        description = response.xpath("//div[@id='description']//text()").extract()
        clean_description = " ".join([d.strip() for d in description if d.strip()])
        characteristics = response.xpath("//div[@id='product-info-table']//text()").extract()
        clean_characteristics = " ".join([c.strip() for c in characteristics if c.strip()])
        breadcum_list = response.xpath("//nav/a/text()").extract()[1:-1]
        categories_dict = {breadcum_list.index(c):c for c in breadcum_list}
        item = dict()
        item['Date'] = datetime.datetime.now().strftime("%d/%m/%Y")
        item['Canal'] = 'Prixz'
        item['Category'] = categories_dict.get(0, '')
        item['Subcategory'] = categories_dict.get(1, '')
        item['Subcategory2'] = categories_dict.get(2, '')
        item['Subcategory3'] = ''
        item['Marca'] = breadcum_list[-1]
        item['Modelo'] = presenticion
        item['SKU'] = response.xpath("//input[contains(@name,'_sku')]/@value").extract_first()
        item['UPC'] = sku
        item['Item'] = title
        item['Item Characteristics'] = f'{clean_description} {clean_characteristics}'
        item['URL SKU'] = response.url
        item['Image'] = image_url
        item['Price'] = price
        item['Sale Price'] = sale_price
        item['Shipment Cost'] = shipment_cost
        item['Sales Flag'] = ''
        item['Store ID'] = ''
        item['Store Name'] = ''
        item['Store Address'] = ''
        item['Stock'] = stock
        item['UPC WM'] = sku[0:-1].zfill(16)
        item['Final Price'] = min(price, sale_price) if price and sale_price else price
        yield item







    
        
