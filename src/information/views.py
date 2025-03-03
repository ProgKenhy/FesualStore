from django.shortcuts import render


def delivery(request):
    return render(request, 'information/delivery.html', {'title': 'Доставка'})


def payment(request):
    return render(request, 'information/payment.html', {'title': 'Оплата'})


def contacts(request):
    return render(request, 'information/contacts.html', {'title': 'Контакты'})


def team(request):
    return render(request, 'information/team.html', {'title': 'Наша команда'})


def faq(request):
    return render(request, 'information/faq.html', {'title': 'Частые вопросы'})


def history(request):
    return render(request, 'information/company-history.html', {'title': 'История компании'})


def public_offer(request):
    return render(request, 'information/public-offer.html', {'title': 'Публичная оферта'})
