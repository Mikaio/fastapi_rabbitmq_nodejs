# Steps

## Python
### Install/Update [Pipenv](https://pipenv.pypa.io/en/latest/)
```pip install --user pipenv```

```pip install --user --upgrade pipenv```

### Install dependencies
```pipenv install```

```python -m pipenv install```

### Run
```pipenv run uvicorn main:app --reload```

```python -m pipenv run uvicorn main:app --reload```


## Node.js
### Install dependencies
```yarn install```

### Install [PM2](https://pm2.keymetrics.io/docs/usage/quick-start/) (Optional)
```npm install pm2 -g```

### Run
```yarn start```
or
```pm2 start ecosystem.config.js && pm2 logs```

## [RabbitMQ](https://www.rabbitmq.com/download.html) (Docker)
```docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management```
