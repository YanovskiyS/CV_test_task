# Stage 1: Build React
FROM node:20-alpine AS build
WORKDIR /app

# Скопировать package.json + lockfile из подпапки
COPY frontend/package*.json ./

# Установить зависимости
RUN npm install

# Скопировать исходники из подпапки
COPY frontend/. .

# Собрать приложение (создаст /app/build)
RUN npm run build

# Stage 2: Serve via Nginx
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]