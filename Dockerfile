FROM python:3.9.6

RUN pip install pipenv
WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --dev --system --deploy

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000