#%%
import pandas as pd
import os
import urllib.request
import requests
import traceback
from time import sleep
import requests

#%%
def extrai_html( link ):
    try:
        print( link )
        response = requests.get( link )
        html = response.text
        sleep( 1 )

        return html
    except:
        print("Ocorreu uma falha")
        traceback.print_exc()

#link = "https://as1.trt3.jus.br/juris/acordao.htm?idAcordao=pje20598726&amp;hash=fab5bf0bab5f395d51317c9fa8dc3f1e"
#extrai_html( link )

#%%
def extrai_pdf( link ):
    try:    
        print( link )
        response = requests.get( link )
        name = link.split( "=" )[-1] +".pdf"
        with open( "pdfs\\"+name, "wb" ) as f:
            f.write(response.content)
        sleep( 1 )
    except:
        print("Ocorreu uma falha")
        traceback.print_exc()

#link = "http://as1.trt3.jus.br/consulta/redireciona.htm?pIdAcordao=1274175&acesso=46590c114e1fdb5088375e0fda96a5c4"
#extrai_pdf( link )


#%%
trt3_df_html = pd.DataFrame(columns=[ 'HTML' ])

pasta = "urls_inteiro_teor"
#nome_arquivo = "TRT3_df_urls_inteiro_teor_"

for nome_arquivo in os.listdir( pasta ):
    if nome_arquivo.find( "TRT3_df_urls_inteiro_teor_nao_baixadas_" ) == -1:
        print( nome_arquivo )
        #df = pd.read_csv( pasta+"\\"+nome_arquivo, encoding='utf-8' ) #windows
        df = pd.read_csv( pasta+"//"+nome_arquivo, encoding='utf-8' ) #linux
        df.info()
        df[ "URL_INTEIRO_TEOR" ] = df[ "URL_INTEIRO_TEOR" ].str.replace("&amp;", "&") #arruma um detalhe no link que veio incorreto
        
        #processa apenas os que sao PDF
        #print( "\nprocessando PDFs" )
        #df[ df['URL_INTEIRO_TEOR'].str.contains( "redireciona.htm" ) ]['URL_INTEIRO_TEOR'].map( extrai_pdf )
        
        #processa apenas os que sao HTML
        print( "\nprocessando HTMLs" )
        html = df[ df['URL_INTEIRO_TEOR'].str.contains( "acordao.htm" ) ]['URL_INTEIRO_TEOR'].map( extrai_html )
        trt3_df_html[ "HTML" ] = html        
        #trt3_df_html.to_csv( "html\\TRT3_df_html_"+nome_arquivo+".csv", encoding='utf-8', index=False )
        trt3_df_html.to_csv( ".//inteiro_teor//TRT3_inteiro_teor_"+nome_arquivo+".csv", encoding='utf-8', index=False )