from django.db.models import Q
from django.http import HttpRequest, JsonResponse
from django_api import models


def search_f(request: HttpRequest) -> JsonResponse:

    # todo Извлечение параметра для поиска из запроса
    text = request.GET.get("text", "")

    # todo Извлечение из базы данных только одобренных объявлений
    # # 1
    # ads = models.Ad.objects.all()
    # # 2
    # ads = ads.filter(flag_good=True)
    # # 3
    # ads = ads.filter(Q(title__icontains=text) | Q(description__icontains=text))

    # todo Извлечение из базы данных только одобренных объявлений
    ads = models.Ad.objects.filter(Q(title__icontains=text) | Q(description__icontains=text), flag_good=True)

    # todo Превращение объектов в JSON (Сериализация)
    data = [
        {"id": ad.id, "title": ad.title, "price": ad.price, "date_created": ad.created}
        for ad in ads
    ]

    # todo Возврат данных
    return JsonResponse(data=data, safe=False)


def ads_f(request: HttpRequest) -> JsonResponse:
    # todo Извлечение из базы данных только одобренных объявлений
    ads = models.Ad.objects.filter(flag_good=True)

    # todo Превращение объектов в JSON (Сериализация)
    data = [
        {"id": ad.id, "title": ad.title, "price": ad.price, "date_created": ad.created}
        for ad in ads
    ]

    # todo Возврат данных
    return JsonResponse(data=data, safe=False)
