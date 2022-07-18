# # этап production (production-stage)
# FROM nginx:stable-alpine as production-stage
# COPY --from=build-stage /app/dist /usr/share/nginx/html
# EXPOSE 80
# CMD /usr/sbin/nginx -g "daemon off;"

# этап сборки (build stage)
FROM node:lts-alpine AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
RUN chown -R node /app/node_modules
COPY . .
RUN npm run build
RUN ls

FROM nginx:1.19-alpine AS production-stage

COPY nginx.conf /

# COPY --from=build-stage /app/dist /opt/site
COPY --from=build-stage /app/dist /usr/share/nginx/html
# COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80