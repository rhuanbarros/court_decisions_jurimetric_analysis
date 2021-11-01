#%%
import pandas as pd
import os
from time import sleep

import urllib.request
import requests
import traceback

#%%
trt4_df_inteiro_teor = pd.DataFrame(columns=[ 'INTEIRO_TEOR' ])

arquivo = "E:\\OneDrive\\Documentos\\pesquisa_codigos_2020\\pesquisa_jurimetria_polaridade_final\\2_Compreensao_dos_dados\\2_1_coleta_de_dados\\Datasets_coletados\\TRT4\\1_trt4_inteiro_teor_janeiro_abril_2019.csv"
df = pd.read_csv( arquivo, encoding='utf-8' ) #windows
df.info()

#%%
pd.set_option('display.max_colwidth', 1000)
html = str( df.head(1)["html"] )
print( html.replace( "\n", "" ) )


#%%
from bs4 import BeautifulSoup
from bs4.element import Comment

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def text_from_html(body):
    print( "foi" )
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    retorno = u" ".join(t.strip() for t in visible_texts)
    return retorno.replace( "\n", "" )

print( text_from_html( html ) )

#%%
inteiro_teor = df['html'].map( text_from_html )
len( inteiro_teor )

#%%
df[ "inteiro_teor" ] = inteiro_teor        
df=df.drop('html',1)
df.info()

#%%
df.to_csv( "TRT4_inteiro_teor_2017_2018_2019_amostra.csv", encoding='utf-8', index=False )

# %%
