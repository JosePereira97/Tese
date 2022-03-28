FROM python:3.7

RUN mkdir /Assembly_MG
WORKDIR /Assembly_MG
ADD . /Assembly_MG/
#install dependecies
RUN pip install flask

EXPOSE 5001

CMD ["python3", "Assembly_MG.py"]