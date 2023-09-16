FROM python:3.11

# Allow docker to cache installed dependencies between builds
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /beginnerai

# Mount the application code to the image
COPY . /beginnerai
WORKDIR /beginnerai

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

EXPOSE 8000

# Run the application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]