FROM python:3.11
ENV PYTHONUNBUFFERED=1
COPY ./requirements.txt /bot/requirements.txt
COPY /bot /bot
WORKDIR /bot
RUN pip install --no-cache-dir --upgrade -r /bot/requirements.txt