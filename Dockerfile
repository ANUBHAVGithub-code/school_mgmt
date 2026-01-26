# use an official python image 
FROM python:3.10-slim 

# prevent python from writing .pyc files 
ENV PYTHONDONTWRITEBYTECODE=1

# prevent python output buffrening
#Forces Python to print logs immediately
#Without this, Django logs may appear late or not at all in Docker logs
ENV PYTHONUNBUFFERED=1

# setup working directory inside docker container
#Creates /app inside the container (if not present)
#All following commands run inside /app
WORKDIR /app   

# install dependencies 
#this runs once during build time
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt 


# copy project files
COPY . .

# expose django development port
EXPOSE 8000

# run django development server
CMD ["python", "manage.py","runserver","0.0.0.0:8000"]

#full life cycle
# FROM -> RUN : BUILD TIME
#CMD : RUN TIME