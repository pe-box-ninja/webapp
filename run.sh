#!/bash/sh
# sh ./run.sh

docker-compose up -d

kill -9 $(lsof -ti:3000)
flask --debug run --port 3000 --host 127.0.0.1
