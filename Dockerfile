FROM python:3.6
ENV PYTHONUNBUFFERED=1
WORKDIR /catering_service
COPY . /catering_service
RUN pip3 install --upgrade pip
RUN pip3 install wheel
RUN pip3 install -r requirements.txt
