FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

COPY app /code/app/
WORKDIR /code/

CMD sh -c "/wait && uvicorn app.main:app --proxy-headers --host 0.0.0.0 --port 80"
