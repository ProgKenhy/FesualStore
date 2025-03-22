from django.conf import settings

def allowed_hosts(request):
    return {
        'ALLOWED_HOSTS': settings.ALLOWED_HOSTS,
    }

def metrika_id(request):
    return {
        'YANDEX_METRICA_ID': settings.YANDEX_METRICA_ID,
    }
