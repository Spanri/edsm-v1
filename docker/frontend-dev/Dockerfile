FROM node:lts-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install

RUN chown -R node /app/node_modules

EXPOSE 8080

CMD ["npm", "run", "serve"]