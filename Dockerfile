FROM python:3.6-slim-stretch

RUN apt-get update \
    && apt-get install -y \
    apt-utils \
    build-essential \
    git \
    wget \
    curl \
    unzip

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt \
    && python3 -m spacy download pt_core_news_sm \
    && curl -fsSL https://deb.nodesource.com/setup_16.x | bash - \
    && apt-get install -y nodejs \
    && jupyter labextension install jupyterlab-plotly

WORKDIR /app

ENTRYPOINT bash
#ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--no-browser", "--allow-root"]
#jupyter notebook --ip=0.0.0.0 --no-browser --allow-root
#jupyter lab --ip=0.0.0.0 --no-browser --allow-root