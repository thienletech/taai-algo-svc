FROM python:3.8-slim-buster as build-stage

RUN echo "deb http://deb.debian.org/debian buster main" >> /etc/apt/sources.list && \
    echo "deb-src http://deb.debian.org/debian buster main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list && \
    echo "deb-src http://security.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list
RUN apt update && \
    apt install -y libpq-dev gcc cmake

WORKDIR /app
COPY . /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install pyinstaller

RUN pyinstaller -w -F \
	--add-data "templates:templates" \
	--add-data "static:static" \
	--hidden-import='pkg_resources.py2_warn' \
	--noconfirm \
	src/server.py

FROM python:3.8-slim-buster as prod-stage

RUN echo "deb http://deb.debian.org/debian buster main" >> /etc/apt/sources.list && \
    echo "deb-src http://deb.debian.org/debian buster main" >> /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list && \
    echo "deb-src http://security.debian.org/debian-security buster/updates main" >> /etc/apt/sources.list
RUN apt update && \
    apt install -y libpq-dev

WORKDIR /app
COPY --from=build-stage /app/dist/server /app/server

ENV LOG_LEVEL=${LOG_LEVEL}
ENV APP_DIR=${APP_DIR}
ENV APP_HOST=${APP_HOST}
ENV APP_HOST=${APP_PORT}
ENV APP_ROOT=${APP_ROOT}
ENV DB_POSTGRES_USER=${DB_POSTGRES_USER}
ENV DB_POSTGRES_PW=${DB_POSTGRES_PW}
ENV DB_POSTGRES_HOST=${DB_POSTGRES_HOST}
ENV DB_POSTGRES_PORT=${DB_POSTGRES_PORT}
ENV DB_POSTGRES_DB=${DB_POSTGRES_DB}
ENV OPENAI_API_KEY=${OPENAI_API_KEY}

CMD ["/app/server"]
# ENTRYPOINT ["/bin/sh"]
