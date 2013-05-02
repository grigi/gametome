from django.shortcuts import render
from pure_pagination import Paginator, EmptyPage
from django.conf import settings
from .models import *

RESULTS_PER_PAGE = getattr(settings, 'RESULTS_PER_PAGE', 20)

# Create your views here.

def index(request):
    ct = ContentType.objects.get(model='news')
    news_list = News.objects.filter(content_type=ct).order_by('-created_date').select_related('reporter').prefetch_related('comments', 'related_to__a', 'related_to__a__content_type', 'related_from__b', 'related_from__b__content_type')
    
    paginator = Paginator(news_list, RESULTS_PER_PAGE)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        news_list = paginator.page(page)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)
        
    return render(request, 'index.html', {
        'news_list': news_list,
    })

def news(request, news_id):
    news = News.objects.filter(pk=news_id).select_related('reporter').prefetch_related('comments','comments__reporter', 'related_to', 'related_to__a', 'related_to__a__content_type', 'related_from', 'related_from__b', 'related_from__b__content_type')
    return render(request, 'news_item.html', {
        'news': news[0],
    })

def games(request):
    games_list = Game.objects.all().order_by('-created_date').select_related('reporter','album','company').prefetch_related('comments')

    paginator = Paginator(games_list, RESULTS_PER_PAGE)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        games_list = paginator.page(page)
    except EmptyPage:
        games_list = paginator.page(paginator.num_pages)
    
    return render(request, 'games.html', {
        'games_list': games_list,
    })

def game(request, game_id):
    game = Game.objects.filter(pk=game_id).select_related('reporter').prefetch_related('comments','comments__reporter', 'related_to__a', 'related_to__a__content_type', 'related_from__b', 'related_from__b__content_type')
    return render(request, 'game_item.html', {
        'game': game[0],
    })

def companies(request):
    ct = ContentType.objects.get(model='company')
    comp_list = Company.objects.filter(content_type=ct).order_by('-created_date').select_related('reporter').prefetch_related('comments','games')

    paginator = Paginator(comp_list, RESULTS_PER_PAGE)
    try:
        page = int(request.GET.get('page', 1))
    except ValueError:
        page = 1
    try:
        comp_list = paginator.page(page)
    except EmptyPage:
        comp_list = paginator.page(paginator.num_pages)
    
    return render(request, 'companies.html', {
        'comp_list': comp_list,
    })

def company(request, comp_id):
    comp = Company.objects.filter(pk=comp_id).select_related('reporter').prefetch_related('comments','comments__reporter', 'games__reporter')
    return render(request, 'company_item.html', {
        'comp': comp[0]
    })
