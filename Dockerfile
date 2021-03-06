FROM python:3.9.5
COPY . /app
WORKDIR /app
RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE 8000
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8000"]
