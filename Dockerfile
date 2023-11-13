#FROM python:3.9-slim-bookworm
FROM python:3.8
#FROM apache/airflow:2.7.3
USER root
RUN mkdir /app
COPY . /app/
WORKDIR /app/
RUN pip3 install -r requirements.txt
ENV AIRFLOW_HOME="/app/airflow"
ENV AIRFLOW__CORE__DAGBAG_IMPORT_TIMEOUT=1000
ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
RUN airflow db init
RUN airflow users create -e prakhar.kumar5@gmail.com -f Prakhar -l Baba -p admin -r Admin -u admin
RUN chmod 777 start.sh
RUN apt update -y && apt install awscli -y
ENTRYPOINT [ "/bin/sh" ]
CMD ["start.sh"]