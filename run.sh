#!/bash/sh
# sh ./run.sh

docker-compose up -d

kill -9 $(lsof -ti:5200)
flask --debug run --port 5200 --host 127.0.0.1
