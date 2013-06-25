from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from haystack import indexes
from gtdb import models

class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.News

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        ct = ContentType.objects.get(model='news')
        return self.get_model().objects.filter(content_type=ct, updated_date__lte=now())

class GameIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.Game

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(updated_date__lte=now())

class CompanyIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return models.Company

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        ct = ContentType.objects.get(model='company')
        return self.get_model().objects.filter(content_type=ct, updated_date__lte=now())
