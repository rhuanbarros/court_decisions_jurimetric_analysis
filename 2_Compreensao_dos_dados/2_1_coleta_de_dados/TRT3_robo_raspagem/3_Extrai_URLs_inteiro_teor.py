import pandas as pd
import time
import traceback
import urllib.request
from time import sleep

#df = pd.read_excel( 'TRT3_df_urn_selecionadas.xls', encoding='utf-8' )
df = pd.read_csv( 'TRT3_df_urn_selecionadas_amostra_2017_2018_2019_2.csv', encoding='utf-8' )
print( df.info() )

df_urls = pd.DataFrame(columns=['URL', 'URL_INTEIRO_TEOR'])
df_urls_nao_baixadas = pd.DataFrame(columns=['URL', 'URL_INTEIRO_TEOR'])

start = time.time()

cont=1
for url in df.iloc[:, 0]:
    print(cont)
    cont=cont+1
    try:
        fp = urllib.request.urlopen( url )
        mybytes = fp.read()
        html = mybytes.decode("utf8")
        fp.close()
        publicacao_original_pos = html.find( "Publicação Original" )
        if publicacao_original_pos == -1:
            print( "Nao achou 'publicao original'" )
        else:
            link_inicio_pos = html.find( "href=\"", publicacao_original_pos ) + len( "href=\"" )
            if link_inicio_pos == -1:
                print( "Nao achou 'link_inicio_pos'" )
            else:
                link_fim_pos = html.find( "\"", link_inicio_pos )
                if link_fim_pos == -1:
                    print( "Nao achou 'link_fim_pos'" )
                else:
                    url_inteiro_teor = html[ link_inicio_pos:link_fim_pos ]
                    print( url_inteiro_teor )

        df_urls.loc[len(df_urls)] = [url, url_inteiro_teor]
        #print( [url, url_inteiro_teor] )

        if cont % 100 == 0:
            print( "salvo: "+str( cont ) )
            #df_urls.to_csv( "urls_inteiro_teor\\TRT3_df_urls_inteiro_teor_"+str( cont )+".csv", encoding='utf-8', index=False ) #windows
            df_urls.to_csv( ".//urls_inteiro_teor//TRT3_df_urls_inteiro_teor_"+str( cont )+".csv", encoding='utf-8', index=False ) #linux
            df_urls = df_urls.iloc[0:0] #limpa dataframe

            #df_urls_nao_baixadas.to_csv( "urls_inteiro_teor\\TRT3_df_urls_inteiro_teor_nao_baixadas_"+str( cont )+".csv", encoding='utf-8', index=False )
            df_urls_nao_baixadas = df_urls.iloc[0:0] #limpa dataframe
        
        #sleep(randint(10,100))
        sleep( 1 )
    except:
        print("Ocorreu uma falha")
        traceback.print_exc()
        df_urls_nao_baixadas.loc[len(df_urls)] = [url, url_inteiro_teor]

print( df_urls.info() )
print( df_urls.head() )
print( df_urls_nao_baixadas.info() )

#df_urls.to_csv( "urls_inteiro_teor\\TRT3_df_urls_inteiro_teor_"+str( cont )+".csv", encoding='utf-8', index=False ) #windows
df_urls.to_csv( ".//urls_inteiro_teor//TRT3_df_urls_inteiro_teor_"+str( cont )+".csv", encoding='utf-8', index=False ) #linux

#df_urls_nao_baixadas.to_csv( "urls_inteiro_teor\\TRT3_df_urls_inteiro_teor_nao_baixadas_"+str( cont )+".csv", encoding='utf-8', index=False ) #windows
#df_urls_nao_baixadas.to_csv( ".//urls_inteiro_teor//TRT3_df_urls_inteiro_teor_nao_baixadas_"+str( cont )+".csv", encoding='utf-8', index=False ) #linux


end = time.time()
hours, rem = divmod(end-start, 3600)
minutes, seconds = divmod(rem, 60)
print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))