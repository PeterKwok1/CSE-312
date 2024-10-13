FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install -y ffmpeg
COPY . .
EXPOSE 8080
CMD [ "python", "-u", "./server.py" ]