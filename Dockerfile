#==============================================================================================
FROM continuumio/anaconda3:2022.10

RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  build-essential=12.9 \
  && \
  apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/software
COPY . .
RUN pip install .
WORKDIR /data

ENTRYPOINT [ "prodigy_cryst" ]
#==============================================================================================
