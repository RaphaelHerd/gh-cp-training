FROM composer:latest

WORKDIR /home/app

COPY composer.json /home/app/
COPY index.php /home/app/
COPY bin/ /home/app/bin/
COPY commands/ /home/app/commands/
COPY config/ /home/app/config/
COPY controllers/ /home/app/controllers/
COPY views/ /home/app/views/

RUN composer install --no-dev --optimize-autoloader

EXPOSE 8000

CMD ["php", "-S", "0.0.0.0:8000", "-t", "/home/app"]
