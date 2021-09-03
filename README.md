Docker-compose file fors quick start of composite Docker projects.

- Keycloak + Postgresql   : Authentication services
- RabbitMQ + Postgresql   : Messaging services
- Krakend                 : Gateway service 
- K2 (Krakend + Keycloak) : Secured Gateway service

Used ports:

12305	Keycloak admin/auth
12306	Keycloak admin/auth (SSL)
-----------------------------------
12310	Tyk	
12311	pingtest 
-----------------------------------
12320	Kong 	
12321	Kong (SSL)
12322	Kong admin	
12323	Kong admin (SSL)
12324	Konga dashboard
12329	pingtest 
-----------------------------------
12330	Krakend	
12339	pingtest 
-----------------------------------
12370	KT: Tyk	
12375	KT: Keycloak admin/auth 
12376	KT: Keycloak admin/auth (SSL)
12378	KT: Backend
12379	KT: Frontend
-----------------------------------
12380	KK: Kong	
12381	KK: Kong	(SSL)
12382	KK: Kong	admin
12383	KK: Kong	admin (SSL)
12384	KK: Konga dashboard
12385	KK: Keycloak admin/auth 
12386	KK: Keycloak admin/auth (SSL)
12388	KK: Backend
12389	KK: Frontend
-----------------------------------
12390	K2: Krakend	
12395	K2: Keycloak admin/auth 
12396	K2: Keycloak admin/auth (SSL)
12398	K2: Backend
12399	K2: Frontend
-----------------------------------
15672	Rabbit admin console
15673	Rabbit exchanges/queues
-----------------------------------


