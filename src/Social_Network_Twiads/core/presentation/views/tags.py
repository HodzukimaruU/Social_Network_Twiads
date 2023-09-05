from __future__ import annotations

from typing import TYPE_CHECKING

from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from core.models import Tweet

from django.http import HttpResponse

if TYPE_CHECKING:
    from django.http import HttpRequest

@login_required
@require_http_methods(["GET"])
def tags_views_controller(request: HttpRequest) -> HttpResponse:
    tags = request.GET.get('tags')
    tweets = Tweet.objects.filter(tags__name__icontains=tags) if tags else None
    
    if tweets:
        sort_by = request.GET.get('sort_by', 'Newest')
        if sort_by == 'Newest':
            tweets = tweets.order_by('-created_at')
        elif sort_by == 'Likes':
            tweets = tweets.order_by('-likes_count')
        
        paginator = Paginator(tweets, 2)
        page_number = request.GET.get('page', 1)
        page = paginator.get_page(page_number)
        
        context = {
            'tweets': page,
            'tags': tags,
        }
        return render(request, 'tags.html', context)
    
    context = {
        'tweets': None,
        'tags': tags,
    }
    return render(request, 'tags.html', context)
