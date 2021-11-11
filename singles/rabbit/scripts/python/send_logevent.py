import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_publish(exchange='Log_Exchange',
                      routing_key='system.event',
                      properties=pika.BasicProperties(content_type='text/plain'),
                      body='System is running slowly...')
connection.close()