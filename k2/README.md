Configure Keycloak:
-------------------
(1)Create Client
- client id: krakend-api-gateway
- protocol: openid-connect
- root url: http://localhost:8402

(2)Configure Client
- access type: confidential
- go to Credentials and copy the Secret

(3)Create Role
- role Name: pingtest-parent

(4)Create User
- username: test
- email verified: checked

(5)Configure user
- password: test
- temporary: unchecked
- assign 'pingtest-parent' role