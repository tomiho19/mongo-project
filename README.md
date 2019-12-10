# Facebook v2
* mongo start
```shell script
docker-compose up
```
* backend
```shell script
cd backend
python3.6 -m venv venv
source venv/bin/activate
cat requirements.txt | xargs -n 1 venv/bin/pip3 install
cd src
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
* frontend
```shell script
cd frontend
npm i
npm start
```
