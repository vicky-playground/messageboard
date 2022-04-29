FROM python

WORKDIR /main

COPY requirement.txt .

RUN pip install -r requirement.txt

COPY ./messageboard ./messageboard

CMD ["python", "./messageboard/app.py"]