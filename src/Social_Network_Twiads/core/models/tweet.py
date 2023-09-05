from django.db import models

from .base_model import BaseModel


class Tweet(BaseModel):
    """User message"""

    content = models.CharField(max_length=400, null=False)
    likes_count = models.PositiveIntegerField(default=0)
    retweets_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)

    parent_tweet = models.ForeignKey(to="self", on_delete=models.CASCADE, null=True, related_name="comments")
    author = models.ForeignKey(to="User", on_delete=models.CASCADE, related_name="tweets")

    tags = models.ManyToManyField(to="Tag", symmetrical=False, related_name="tweets", db_table="tag_tweets", blank=True)

    class Meta:
        db_table = "tweets"
