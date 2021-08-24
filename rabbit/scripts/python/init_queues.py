import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=15673))
channel = connection.channel()

# First declare exchanges (contact points)
channel.exchange_declare(exchange='Command_Exchange', exchange_type='fanout', durable=True)
channel.exchange_declare(exchange='Log_Exchange', exchange_type='topic', durable=True)
# Then declare queues (message stores)
channel.queue_declare(queue='commands', durable=True)
channel.queue_declare(queue='commands_backout', durable=True)
channel.queue_declare(queue='system_log', durable=True)
channel.queue_declare(queue='user_log', durable=True)

# Register queues with relevant exchanges ("Here I am. I'm interested in messages from you.")
channel.queue_bind(exchange='Command_Exchange', queue='commands')
channel.queue_bind(exchange='Command_Exchange', queue='system_log')
channel.queue_bind(exchange='Log_Exchange', queue='user_log', routing_key='user.event')
channel.queue_bind(exchange='Log_Exchange', queue='system_log', routing_key='system.event')
connection.close()