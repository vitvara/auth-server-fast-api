FROM python

COPY ./src /app/src
COPY ./requirement.txt /app

WORKDIR /app

RUN pip3 install -r requirement.txt

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host=0.0.0.0", "--reload"]