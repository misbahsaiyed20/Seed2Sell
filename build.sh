#!/bin/bash

mkdir -p static/media
cp -r media/* static/media/

python manage.py collectstatic --noinput