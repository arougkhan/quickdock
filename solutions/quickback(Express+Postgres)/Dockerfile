FROM node:16

#RUN apt-get clean  && apt-get -y update

WORKDIR /usr/src/app

## Copy and install dependencies
COPY ./src/node/package*.json /usr/src/app/
RUN npm install

COPY ./src/node /usr/src/app
RUN npm run build

RUN groupadd -g 500 app && useradd -u 1001 -g app app
RUN chmod -R 766 /usr/src/app/*
RUN chown -R app:app /usr/src/app/*
USER app

EXPOSE 5001
CMD [ "node", "build/server.js" ]

