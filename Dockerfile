FROM pytorch/pytorch
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app/
ARG port=80
EXPOSE $port
ENV app_port $port
CMD uvicorn main:app --host 0.0.0.0 --port $app_port