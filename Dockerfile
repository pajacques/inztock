docker FROM python:3.10.8-bullseye

WORKDIR /FinTechExplained_Python_Docker

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENV FLASK_APP=App.py
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]