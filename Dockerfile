#FROM -> usado para baixar uma imagem já criada, caso eu queria criar uma imagem do zero, eu uso o FROM scratch
FROM ubuntu:latest

#RUN -> usado para rodar comandos no terminal antes de criar a imagem
RUN apt-get update 
RUN apt-get install -y \
    apache2 \
    python3 \
    python3-pip \
    python3.12-venv

#WORKDIR -> usado para mudar o diretório de trabalho
WORKDIR /app

COPY . .

RUN python3 -m venv venv
#RUN [ "/bin/bash", "-c", "source venv/bin/activate"]

#CMD -> usado para rodar comandos no terminal depois de criar a imagem apenas quando o container for iniciado

#ENTRYPOINT -> usado para rodar comandos no terminal depois de criar a imagem apenas quando o container for iniciado
#EXPOSE -> usado para expor uma porta do container (documentação)
EXPOSE 8000

#ativar o venv, instalar as dependências e rodar o servidor
CMD [ "/bin/bash", "-c", "source venv/bin/activate && pip install -r requirements.txt && python manage.py runserver 0.0.0.0:8000"]