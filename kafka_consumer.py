from kafka import KafkaConsumer
import json


class kafka_consumer(object):
    kafka_server = []
    group_id = ''

    def __init__(self, kafka_server=['10.91.125.32:9092'], group_id='test'):
        self.kafka_server = kafka_server
        self.group_id = group_id

    def read(self, topic):
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=self.kafka_server,
            group_id=self.group_id
        )
        print("read {} message".format(topic))
        for message in consumer:
            print("receive, key: {}, value: {}".format(
                json.loads(message.key.decode()),
                json.loads(message.value.decode())
                )
            )


if __name__ == '__main__':
    kafka = kafka_consumer()
    kafka.read('dispatch_bus_test')
