FROM python:3.9.17
WORKDIR /app
VOLUME /tmp
ADD . /app/
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
ENTRYPOINT ["python","/app/main.py"]