import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.basic_publish(exchange='Command_Exchange',
                      routing_key='user.command',
                      properties=pika.BasicProperties(content_type='text/plain'),
                      body='{\"command\" = \"Secure\", \"target\" = \"All UR Base\"}"')
connection.close()