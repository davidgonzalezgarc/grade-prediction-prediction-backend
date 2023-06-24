FROM python:3.9
WORKDIR /home/app
COPY requirements.txt /home/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /home/app/requirements.txt
COPY rest /home/app/rest
COPY db.py /home/app/db.py
COPY main.py /home/app/main.py
COPY model.py /home/app/model.py
COPY predict.py /home/app/predict.py
COPY storage.py /home/app/storage.py
EXPOSE 8000
ENTRYPOINT ["uvicorn", "main:app", "--host=0.0.0.0", "--port=8000"]