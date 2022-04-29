FROM python

WORKDIR /mainfile

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY ./messageboard ./messageboard

CMD ["python", "./messageboard/app.py"]