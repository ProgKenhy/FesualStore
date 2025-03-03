#!/bin/bash
# prod.sh - запуск в продакшн-режиме
docker-compose -f docker-compose.prod.yml up -d
echo "Сервер запущен в продакшн-режиме"
