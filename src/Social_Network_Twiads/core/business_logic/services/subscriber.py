from __future__ import annotations

from typing import TYPE_CHECKING

from core.models import User

if TYPE_CHECKING:
    from core.business_logic.dto import SubscriberDTO


def subscribe_and_unsubscribe(data: SubscriberDTO) -> None:
    user = User.objects.get(username=data.username)
    subscriber_user = User.objects.get(username=data.subscriber_username)
    if subscriber_user not in user.subscriber.all():
        user.subscriber.add(subscriber_user)
        user.subscribers_count += 1
        subscriber_user.subscriptions_count +=1
        user.save()
        subscriber_user.save()
    else:
        user.subscriber.remove(subscriber_user)
        user.subscribers_count -= 1
        subscriber_user.subscriptions_count -=1
        user.save()
        subscriber_user.save()
    return None