import scrapy
import logging
import pandas as pd
import io
from itertools import islice

class Trt4InteiroTeorSpider(scrapy.Spider):
    name = "trt4_inteiro_teor"
    links_csv = "https://app.scrapinghub.com/api/items.csv?project=388838&spider=trt4&include_headers=1&fields=link&apikey=59335219782042129d04074d949f907b"
    site = 'https://www.trt4.jus.br/pesquisas/'

    def start_requests(self):
        yield scrapy.Request( url=self.links_csv, callback=self.parse_csv )

    def parse_csv(self, response):
        df = pd.read_csv( io.BytesIO( response.body ) )
        #for row in islice( df.itertuples(), 5 ):
        for row in df.itertuples():
            link = getattr(row, 'link')
            link_completo = self.site+str(link)
            logging.debug( link_completo )
            yield scrapy.Request( url=link_completo, callback=self.parse_inteiro_teor, meta={ 'link': link } )

    def parse_inteiro_teor(self, response):
        item = {
            'link': response.meta['link'],
            'html': response.body.decode(response.encoding)            
        }
        yield item