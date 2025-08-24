FROM python

WORKDIR /backend

COPY . /backend

# RUN cd /backend
RUN python -m ensurepip
RUN pip install poetry
RUN poetry lock
RUN poetry install --no-root

EXPOSE 5000

CMD ["poetry", "run", "python", "app.py"]