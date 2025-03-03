from django.shortcuts import render


def delivery(request):
    return render(request, 'information/delivery.html')


def payment(request):
    return render(request, 'information/payment.html')


def contacts(request):
    return render(request, 'information/contacts.html')


def team(request):
    return render(request, 'information/team.html')


def faq(request):
    return render(request, 'information/faq.html')


def history(request):
    return render(request, 'information/company-history.html')


def public_offer(request):
    return render(request, 'information/public-offer.html')
