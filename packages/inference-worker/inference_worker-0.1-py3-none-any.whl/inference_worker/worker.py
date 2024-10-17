import pika, json
from handler import Handler
from input import Input
from multiprocessing import Process

class Worker:
    def __init__(self, *, host, vhost, username, password, exchange, queueName):
        self.host = host
        self.credentials = pika.PlainCredentials(username, password)
        self.connection = None
        self.channel = None
        self.vhost = vhost
        self.queueName = queueName
        self.exchange = exchange
        self.handler = Handler()


    def connect(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                virtual_host=self.vhost,
                credentials=self.credentials
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queueName, durable=True)
        self.channel.queue_bind(exchange=self.exchange, queue=self.queueName)

    def process_message(self, ch, method, properties, body):
        print(f"Received message: {body.decode()}")
        try:
            message = json.loads(body.decode())
            operationId = message.get('operationId')
            baseUrl = message.get('baseUrl')
            inputFilesPath = message.get('inputFilesPath')
            modelArtifactsPath = message.get('modelArtifactsPath')
            arguments = message.get('arguments', {})

            input = Input(
                operationId=operationId,
                baseUrl=baseUrl,
                inputFilesPath=inputFilesPath,
                modelArtifactsPath=modelArtifactsPath,
                arguments=arguments
            )

            process = Process(target=self.handler.handle, args=(input,))
            process.start()
            
            while process.is_alive():
                self.connection.process_data_events(time_limit=1)

            process.join()
        except Exception as e:
            print('Problem occurs')
            print(e)
        
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        self.channel.basic_qos(prefetch_count=1)  # Process one message at a time
        self.channel.basic_consume(queue=self.queueName, on_message_callback=self.process_message)
        print("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()


if __name__ == "__main__":
    worker = Worker()
    try:
        worker.connect()
        worker.start_consuming()
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt, shutting down...")
    finally:
        worker.close()