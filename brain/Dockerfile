FROM python:3.9

WORKDIR /

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir --upgrade -r /requirements.txt

COPY ./ /

RUN prisma generate
# RUN prisma db push

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
