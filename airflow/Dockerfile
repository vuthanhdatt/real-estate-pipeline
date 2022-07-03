FROM apache/airflow:2.2.3

ENV AIRFLOW_HOME=/opt/airflow
ENV PYTHONPATH "${PYTHONPATH}:${AIRFLOW_HOME}"

USER root
RUN apt-get update -qq && apt-get install vim -qqq


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /opt/airflow/data
RUN chmod 777 /opt/airflow/data

WORKDIR $AIRFLOW_HOME


USER $AIRFLOW_UID