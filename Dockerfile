FROM ubuntu:14.04

#TODO: Install dependencies and PIP
RUN apt-get update && apt-get install -y \
    python-dev \
    python-pip

RUN pip install --upgrade pip

#TODO: Install numpy, scipy, scikit-learn, pandas, keras, TF
RUN pip install bottle 
#TODO: Copy a local python file into a folder - "DLCode"

RUN mkdir -p /MLOps/logs
COPY mlops /MLOps

#TODO: Specify "DLCode" as the working directory
WORKDIR MLOps

EXPOSE 8080

CMD python wordcountAPI.py