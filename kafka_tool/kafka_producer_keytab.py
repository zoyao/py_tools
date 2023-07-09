from kafka import KafkaProducer
from kafka.errors import kafka_errors
import traceback
import json
import os


class kafka_producer(object):
    producer = {}

    def __init__(self, kafka_server=['test.plain.com:9092'], username='bus4_dispatch', password='vQMYGDzUB4NdLrj7AjaT'):
        # # 配置地址映射，127.0.0.1为示例
        # with open('/etc/hosts', 'r') as hosts:
        #     if 'bigdata' not in hosts.read():
        #         os.system('echo "127.0.0.1 kafka-point-01\n127.0.0.1 kafka-point-02\n127.0.0.1 kafka-point-03" >> /etc/hosts')
        #
        # # kafka鉴权文件软链接到/etc目录
        # cur_dir = os.path.dirname(os.path.abspath(__file__))  # 自定义该目录
        # os.system('ln -fs %s/krb5.conf /etc/krb5.conf' % cur_dir)
        # os.system('ln -fs %s/kafka.keytab /etc/kafka.keytab' % cur_dir)
        # os.system('ln -fs %s/jaas.conf /etc/jaas.conf' % cur_dir)

        # 生成kafka认证密钥，配置系统环境变量
        os.system('kinit -kt /etc/kafka.keytab kafka/bigdata-test-01@TDH')
        os.environ['KAFKA_OPTS'] = '-Djava.security.auth.login.config=/etc/jaas.conf -Djava.security.krb5.conf=/etc/krb5.conf'

        # 假设生产的消息为键值对（不是一定要键值对），且序列化方式为json
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_server,
            key_serializer=lambda k: json.dumps(k).encode(),
            value_serializer=lambda v: json.dumps(v).encode(),
            sasl_mechanism='PLAIN',
            security_protocol='SASL_PLAINTEXT',
            sasl_plain_username=username,
            sasl_plain_password=password)

    def send(self, topic, msg):
        future = self.producer.send(
                topic,
                # key='count_num',  # 同一个key值，会被送至同一个分区
                value=eval(msg),
                # partition=1
        )  # 向分区1发送消息
        print("send {} message {}".format(topic, msg))
        try:
            future.get(timeout=10)  # 监控是否发送成功
        except kafka_errors:  # 发送失败抛出kafka_errors
            traceback.format_exc()


if __name__ == '__main__':
    message = '{"downlink_trantime":"211117140121","obuid":"912549","operator":"zddd","order_number":1,' \
              '"package_type":"1e","prompt_duration":10,"prompt_status":1,"route_code":"07730","seqno":123456,' \
              '"task_type":"00","reply_sn":948362012} '
    kafka = kafka_producer()
    kafka.send('dispatch_bus_app_ver4', message)
