from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from core.models import Tweet

if TYPE_CHECKING:
    from django.http import HttpRequest


@login_required
@require_http_methods(["GET"])
def top_tags_controller(request: HttpRequest) -> HttpResponse:
    user = request.user
    country = user.country.name if user.country else None
    trending_tags = Tweet.objects.filter(author__country__name=country).values('tags__name').annotate(tag_count=Count('tags')).order_by('-tag_count')[:10]

    context = {
        'trending_tags': trending_tags,
    }
    return render(request, 'trending_in_your_country.html', context)
