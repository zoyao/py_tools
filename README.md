# py_tools
python tools

## requirements
### use
```
pip install -r requirements.txt
```
### generate
```
# install
pip install pipreqs
# generate
pipreqs . --encoding=utf8 --force
```

### check_tool
```docker
docker run -d --name check -e TZ=Asia/Shanghai -v /app/py_tools_config/logs:/app/logs -v /app/py_tools_config/resources:/app/resources check:0.1
```