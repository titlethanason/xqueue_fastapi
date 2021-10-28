FROM python:3.9
WORKDIR /xqueue_fastapi
COPY ./requirements.txt /xqueue_fastapi/requirements.txt
RUN pip install uvicorn
RUN pip install --no-cache-dir --upgrade -r /xqueue_fastapi/requirements.txt
COPY . /xqueue_fastapi/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]