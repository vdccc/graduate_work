FROM alpine
EXPOSE 80
WORKDIR /usr/src/app
RUN apk add --no-cache \
        uwsgi-python3 \
        python3 \
        poetry
COPY pyproject.toml pyproject.toml
RUN python -m venv "/venv"
ENV VIRTUAL_ENV "/venv"
ENV PATH "$VIRTUAL_ENV:${PATH}"
RUN poetry install
COPY graduate_work graduate_work
COPY tracker tracker
COPY wsgi.ini wsgi.ini
CMD [ "uwsgi", "--ini", "wsgi.ini" ] 
