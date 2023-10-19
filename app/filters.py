import django_filters
from django.db import models

from .models import Item


class OrderingFilter(django_filters.filters.OrderingFilter):
    """日本語対応"""
    descending_fmt = '%s （降順）'

class ItemFilterSet(django_filters.FilterSet):
    """
     django-filter 構成クラス
    https://django-filter.readthedocs.io/en/latest/ref/filterset.html
    """


    class Meta:
        model = Item
        # 一部フィールドを除きモデルクラスの定義を全て引用する
        exclude = ['sample_3','sample_cost','sample_url','memo','date','image','created_by','created_at','updated_by','updated_at',]
        # 文字列検索のデフォルトを部分一致に変更
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.TextField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.ImageField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
