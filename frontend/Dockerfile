# Multi-stage: local dev (Vite), production asset build, static nginx runtime.

# ---------- dev ----------
FROM node:22.11-alpine AS dev
WORKDIR /app
RUN apk add --no-cache wget
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]

# ---------- build ----------
FROM node:22.11-alpine AS build
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# ---------- production ----------
FROM nginx:1.27-alpine AS production
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist /usr/share/nginx/html
RUN chown -R nginx:nginx /usr/share/nginx/html \
  && mkdir -p /tmp/client_body /tmp/proxy /tmp/fastcgi /tmp/uwsgi /tmp/scgi \
  && chown -R nginx:nginx /tmp/client_body /tmp/proxy /tmp/fastcgi /tmp/uwsgi /tmp/scgi /var/cache/nginx
USER nginx
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
