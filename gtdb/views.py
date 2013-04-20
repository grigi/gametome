from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from .models import *

RESULTS_PER_PAGE = getattr(settings, 'RESULTS_PER_PAGE', 20)

# Create your views here.

def index(request):
    ct = ContentType.objects.get(model='news')
    news_list = News.objects.filter(content_type=ct).order_by('-created_date').prefetch_related('comments')
    
    paginator = Paginator(news_list, RESULTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        news_list = paginator.page(1)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)
        
    return render(request, 'index.html', {
        'news_list': news_list,
    })

def news(request, news_id):
    return render(request, 'news_item.html', {
        'news': News.objects.get(pk=news_id)
    })

def games(request):
    games_list = Game.objects.all().order_by('-created_date').prefetch_related('comments')

    paginator = Paginator(games_list, RESULTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        games_list = paginator.page(page)
    except PageNotAnInteger:
        games_list = paginator.page(1)
    except EmptyPage:
        games_list = paginator.page(paginator.num_pages)
    
    return render(request, 'games.html', {
        'games_list': games_list,
    })

def game(request, game_id):
    return render(request, 'game_item.html', {
        'game': Game.objects.get(pk=game_id)
    })

def companies(request):
    ct = ContentType.objects.get(model='company')
    comp_list = Company.objects.filter(content_type=ct).order_by('-created_date').prefetch_related('comments')

    paginator = Paginator(comp_list, RESULTS_PER_PAGE)
    page = request.GET.get('page')
    try:
        comp_list = paginator.page(page)
    except PageNotAnInteger:
        comp_list = paginator.page(1)
    except EmptyPage:
        comp_list = paginator.page(paginator.num_pages)
    
    return render(request, 'companies.html', {
        'comp_list': comp_list,
    })

def company(request, comp_id):
    return render(request, 'company_item.html', {
        'comp': Company.objects.get(pk=comp_id)
    })
