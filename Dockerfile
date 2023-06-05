FROM archlinux:latest

RUN pacman -Syu --noconfirm
RUN pacman -S apache python python-pip mysql gcc \
    git openssh neovim fish --noconfirm

# Application environment
WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip3 install -r /app/requirements.txt

EXPOSE 80

CMD ["fish"]
