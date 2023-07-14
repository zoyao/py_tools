FROM python:3.9.17
VOLUME /tmp
ADD . /app/
RUN pip install -r /app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn
                    ##测试环境配置，正式环境保持注释 end
ENTRYPOINT ["python","/app/main.py"]