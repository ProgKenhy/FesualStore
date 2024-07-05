# -*- coding: utf-8 -*-

import multiprocessing
import os
from distutils.util import strtobool

bind = f"0.0.0.0:{os.getenv('PORT', '8000')}"
accesslog = "-"
access_log_format = "%(h)s %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s' in %(D)sµs"  # noqa: E501

workers = int(os.getenv("WEB_CONCURRENCY", multiprocessing.cpu_count() * 2))
threads = int(os.getenv("PYTHON_MAX_THREADS", 1))

reload = bool(strtobool(os.getenv("WEB_RELOAD", "false")))

# certfile = "/var/certbot/conf/live/fesualstore.ru-0003/fullchain.pem"  # pay ATTENTION here 0003 !
# keyfile = "/var/certbot/conf/live/fesualstore.ru-0003/privkey.pem"  # pay ATTENTION here 0003 !
