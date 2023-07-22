FROM debian:bullseye-slim

RUN apt-get update
RUN apt-get install python3 python3-pip apache2 libmariadb-dev-compat libmariadb-dev libapache2-mod-wsgi-py3 \
    apache2-dev nano build-essential fish libreoffice -y

# Configure timezone
ENV TZ=America/Mexico_City
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN mkdir -p ~/.local/share/fonts

COPY ./fonts/Montserrat-Bold.otf ~/.local/share/fonts/
COPY ./fonts/Montserrat-Bold.otf ~/.local/share/fonts/

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

RUN python3 -m pip install --upgrade pip

EXPOSE 80

CMD ["fish"]