import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class CrawlerSpider(CrawlSpider):
    name = "no-scraper"
    allowed_domains = [
        'coruna.gal'
    ]
    start_urls = [
        "https://www.coruna.gal/serviciossociales/es/servicios/tramites/detalle-tramites/tarjeta-para-estacionamiento-en-lugares-reservados-para-personas-con-diversidad-funcional/contenido/1144274928772?argIdioma=es"
    ]

    rules = [
        Rule(LinkExtractor(allow='/servicios/tramites/'), callback='parse_item', follow=True),
    ]

    def parse_item(self, response):
        try:
            parking_places = response.css('.mas_informacion ul li')
            for place in parking_places:

                text = place.xpath('string()').extract_first().strip()
                text = text.replace(' ', ' ')

                maps_url = place.css('a::attr(href)').get()

                # Expresiones regulares
                cantidad_regex = r'(\d+)\s*(prazas)'
                info_regex = r'\(([^()]*?)(?<!prazas)\)'
                nombre_regex = r'^[^()]*'

                # Buscamos los patrones en el texto
                quantity_match = re.search(cantidad_regex, text)
                info_match = re.search(info_regex, text)
                name_match = re.search(nombre_regex, text)

                if quantity_match:
                    try:
                        quantity = int(quantity_match.group(1))
                    except Exception:
                        quantity = 1
                else:
                    quantity = 1

                if info_match:
                    info = info_match.group(1).capitalize()
                else:
                    info = None

                if name_match:
                    name = name_match.group(0).strip().capitalize()
                else:
                    name = None

                if maps_url and maps_url.startswith("https://maps.google"):
                    yield {
                        "name": name,
                        "info": info,
                        "quantity": quantity,
                        "maps_url": maps_url
                    }

        except Exception:
            pass
