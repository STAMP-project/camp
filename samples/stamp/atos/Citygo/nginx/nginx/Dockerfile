FROM nginx:latest

COPY nginx.tmpl /etc/nginx/nginx.tmpl

CMD /bin/sh -c "envsubst </etc/nginx/nginx.tmpl > /etc/nginx/nginx.conf & nginx -g 'daemon off;' || cat /etc/nginx/nginx.conf"
