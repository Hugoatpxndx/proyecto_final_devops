FROM alpine:latest AS builder
WORKDIR /app
RUN echo "<h1>Proyecto Final DevOps</h1><p>Mi contenedor funciona y es escalable.</p>" > index.html

FROM nginx:alpine
COPY --from=builder /app/index.html /usr/share/nginx/html/index.html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
