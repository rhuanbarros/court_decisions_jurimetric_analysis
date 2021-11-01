import scrapy
import logging
import datetime
from datetime import timedelta

class Trt4Spider(scrapy.Spider):
    name = "trt4"
    pagina_inicial = 'https://www.trt4.jus.br/pesquisas/acordaos'
    pagina_resultados = "https://www.trt4.jus.br/pesquisas/acordaos?0-1.IBehaviorListener.0-painel_filtro-form_acordaos-submit_button"
    
    def start_requests(self):
        data_inicial_obj = None
        data_final_obj = datetime.datetime.strptime("19/11/2019", '%d/%m/%Y') #tem que ser essa data para que feche a sequencia correta no loop

        limite_obj = datetime.datetime.strptime("31/12/2019", '%d/%m/%Y')

        for i in range(23):
            data_inicial_obj = data_final_obj + timedelta(days=1)
            data_final_obj = data_final_obj + timedelta(days=15)

            if( data_final_obj < limite_obj ):
                data_inicial = data_inicial_obj.strftime("%d/%m/%Y")
                data_final = data_final_obj.strftime("%d/%m/%Y")
                logging.debug( data_inicial +" - "+ data_final )


                for j in range( 6, 23 ):
                    logging.debug("++++++++++++++++++++++++++++++++++++++++++++++++++")
                    logging.debug(j)
                    logging.debug("++++++++++++++++++++++++++++++++++++++++++++++++++")
                    tipo_orgao_julgador = j
                    pagina=self.pagina_inicial+"/"+str(i)
                    yield scrapy.Request( url=pagina, callback=self.parse, dont_filter=True,
                        meta={'cookiejar': i, 'data_inicial': data_inicial, 'data_final': data_final, 'tipo_orgao_julgador': str( tipo_orgao_julgador ) } )

                yield scrapy.Request( url=pagina, callback=self.parse, dont_filter=True,
                        meta={'cookiejar': i, 'data_inicial': data_inicial, 'data_final': data_final, 'tipo_orgao_julgador': '1789876'} )
                yield scrapy.Request( url=pagina, callback=self.parse, dont_filter=True,
                        meta={'cookiejar': i, 'data_inicial': data_inicial, 'data_final': data_final, 'tipo_orgao_julgador': '1789877'} )

    def parse(self, response):
        data_inicial = response.meta['data_inicial']
        data_final = response.meta['data_final']
        tipo_orgao_julgador = response.meta['tipo_orgao_julgador']

        logging.debug("===========================================================================")
        logging.debug( data_inicial )
        logging.debug( data_final )
        logging.debug( tipo_orgao_julgador )
        logging.debug("===========================================================================")

        data = {
            "id1_hf_0":"",
            "todas_palavras=":"",
            "texto":"",
            "sem_palavras":"",
            "trecho_exato":"",
            "texto_ementa":"",
            "processo":"",
            "tipo_documento":"0",
            "tipo_classe_acordao":"",
            "tipo_orgao_julgador": tipo_orgao_julgador,
            "fonte":"",
            "tipo_redator":"option0",
            "tipo_redator":"option0",
            "data_inicial": data_inicial,
            "data_final":data_final,
            "submit_button":"1"
        }

        yield scrapy.FormRequest(url=self.pagina_resultados, formdata=data, dont_filter=True,
            callback=self.parse_acordaos, method='POST', meta={'cookiejar': response.meta['cookiejar']})
        
    def parse_acordaos(self, response):

        #salva arquivo
        #filename = 'lista_%s.html' % self.quantidade
        #self.quantidade = self.quantidade+1
        #with open(filename, 'wb') as f:
            #f.write(response.body)
        #self.log('Saved file %s' % filename)
        
        for decisao in response.css('li.list-group-item'):
            item = {
                'link': decisao.css('p > a::attr(href)').extract_first()
            }
            yield item

        next_link = response.css('ul.pagination li')[-2]
        next_page_url = next_link.css('a::attr(href)').extract_first()

        #fazer um codigo que rastreia onde deu o erro.
        #anotar em qual data e orgao e quem sabe a pagina.

        #codigo para testes. para copiar apenas a primeira pagina.
        #next_page_url = False

        if next_page_url:
            next_page_url = response.urljoin(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_acordaos, dont_filter=True,
                     meta={'cookiejar': response.meta['cookiejar']} )