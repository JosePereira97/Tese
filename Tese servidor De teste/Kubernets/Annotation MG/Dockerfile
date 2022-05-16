FROM python:3.7

#create a directory
RUN mkdir /annotation_mg
WORKDIR /annotation_mg
ADD . /annotation_mg/
#will installs all packages necessarys
RUN pip install flask 

EXPOSE 5000

CMD ["python3", "Annotation_MG.py"]