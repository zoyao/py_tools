FROM python:3.9.5
VOLUME /tmp
ADD target/runningbus-generate-server.jar /runningbus-generate-server.jar
#测试环境配置，正式环境保持注释 end
ENTRYPOINT ["java","-Djava.security.egd=file:/dev/./urandom","-jar","/runningbus-generate-server.jar"]