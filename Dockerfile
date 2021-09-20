#!/bin/bash
FROM python:3.9
COPY . ./domain_api
WORKDIR /domain_api
RUN pip install -r requirements.txt
CMD python domain_api.py