#!/bin/bash
ln -s /usr/local/vufind/config/vufind/httpd-vufind.conf /etc/apache2/conf-enabled/vufind.conf
chown -R www-data:www-data /usr/local/vufind
chown -R www-data:www-data /usr/local/vufind/local/cache
chown -R www-data:www-data /usr/local/vufind/local/config
mkdir /usr/local/vufind/local/cache/cli
chmod 777 /usr/local/vufind/local/cache/cli
rm -rf /var/www/html
cd /var/www
ln -s /usr/local/vufind/public html
chown -R www-data:www-data /var/www/html
exec /usr/local/bin/apache2-foreground
