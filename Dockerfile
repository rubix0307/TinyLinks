FROM python:3-alpine

# Install system dependencies
RUN apk add --no-cache gcc musl-dev linux-headers

EXPOSE 8000

WORKDIR .

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--reload"]
