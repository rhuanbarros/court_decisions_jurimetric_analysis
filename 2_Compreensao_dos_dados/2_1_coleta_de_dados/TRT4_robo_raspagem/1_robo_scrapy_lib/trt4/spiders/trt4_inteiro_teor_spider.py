import scrapy
import logging
import pandas as pd
import io
from itertools import islice

import csv
import pkgutil
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO 
from io import BytesIO


class Trt4InteiroTeorSpider(scrapy.Spider):
    name = "trt4_inteiro_teor"
    site = 'https://www.trt4.jus.br/pesquisas/'

    def start_requests(self):
        data  = pkgutil.get_data("trt4", "resources/TRT4_df_url_2017_2018_2019_amostra.csv")
        csvio = StringIO( data.decode( encoding='UTF-8',errors='ignore' ) )

        raw = csv.reader( csvio )
        for row in raw:
            #print( "===================================================" )
            linha = row[0].strip()
            #print( linha )
            print( "===================================================" )
            link_completo = self.site+str(linha)
            logging.debug( link_completo )
            yield scrapy.Request( url=link_completo, callback=self.parse_inteiro_teor, meta={ 'link': linha } )

    def parse_inteiro_teor(self, response):
        item = {
            'link': response.meta['link'],
            'html': response.body.decode(response.encoding)            
        }
        yield item