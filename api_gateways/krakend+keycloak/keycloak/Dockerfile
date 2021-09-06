FROM quay.io/keycloak/keycloak:latest
COPY /ssh_configuration /opt/jboss/keycloak/standalone/configuration
COPY /users /opt/jboss/keycloak/standalone/configuration
COPY /realms /opt/jboss/keycloak/standalone/realms/