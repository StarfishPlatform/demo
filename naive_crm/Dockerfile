FROM python:3

EXPOSE 5000

ENV FLASK_APP "./server.py"
ENV TEMPLATES_AUTO_RELOAD "False"
ENV STARFISH_API_URL "http://api.starfish-blockchain.com:3000"

WORKDIR "/app"
COPY ./requirements.txt /app
RUN pip install -r requirements.txt

COPY ./ /app/

ENTRYPOINT ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
