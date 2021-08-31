Docker-compose file fors quick start of composite Docker projects.

- Keycloak + Postgresql   : Authentication services
- RabbitMQ + Postgresql   : Messaging services
- Krakend                 : Gateway service 
- K2 (Krakend + Keycloak) : Secured Gateway service

Used ports:

12345	Keycloak admin/auth service
12346	Postgresql (Keycloak)
-----------------------------------
12380	Krakend	
12381	pingtest (Krakend)
-----------------------------------
12390	K2: Krakend	
12391	K2: pingtest (Krakend)
12395	K2: Keycloak admin/auth service
12396	K2: Postgresql (Keycloak)
-----------------------------------
15672	Rabbit admin console
15673	Rabbit exchanges/queues
-----------------------------------


