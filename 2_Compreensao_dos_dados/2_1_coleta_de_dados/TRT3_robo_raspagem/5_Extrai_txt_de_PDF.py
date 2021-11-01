#%%
import subprocess
import os

pasta = "pdfs"

for nome_arquivo in os.listdir( pasta ):

    linha_de_comando = "pdftotext.exe pdfs\\"+nome_arquivo+" txt\\"+nome_arquivo[0:-3]+"txt"
    result = subprocess.run( linha_de_comando )

# %%
