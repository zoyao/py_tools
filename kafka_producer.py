from kafka import KafkaProducer
from kafka.errors import kafka_errors
import traceback
import json


class kafka_producer(object):
    kafka_server = []

    def __init__(self, kafka_server=['10.91.125.32:9092']):
        self.kafka_server = kafka_server

    def send(self, topic, msg):
        # 假设生产的消息为键值对（不是一定要键值对），且序列化方式为json
        producer = KafkaProducer(
            bootstrap_servers=self.kafka_server,
            key_serializer=lambda k: json.dumps(k).encode(),
            value_serializer=lambda v: json.dumps(v).encode())
        future = producer.send(
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
    kafka.send('dispatch_bus_test', message)
