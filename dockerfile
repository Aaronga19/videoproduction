FROM python:3.13.1-bookworm⁠

ENV PYTHONUNBUFFERED 1
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . $APP_HOME

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt
# RUN DOCKER_CLIENT_TIMEOUT=1200
# RUN COMPOSE_HTTP_TIMEOUT=1200
RUN python3 -m pip install bcrypt


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]