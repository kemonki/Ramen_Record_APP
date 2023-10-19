from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from django import forms

from users.models import User


class Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """
    
    name = models.CharField(
       verbose_name='ラーメン店',
       max_length=20,
       blank=True,
       null=True,
    )
    
    name1 = models.CharField(
       verbose_name='メニュー名称',
       max_length=20,
       blank=True,
       null=True,
    )

    name2 = models.CharField(
        verbose_name='都道府県',
        max_length=20,
        blank=True,
        null=True,
    )
    
    name3 = models.CharField(
        verbose_name='市区町村',
        max_length=20,
        blank=True,
        null=True,
    )
    
    
    ramen_taste = (
        ('醤油', '醤油'),
        ('塩', '塩'),
        ('豚骨', '豚骨'),
        ('味噌', '味噌'),
        ('鯛', '鯛'),
        ('鶏白湯', '鶏白湯'),
        ('つけ麺', 'つけ麺'),
        ('担々麺', '担々麺'),
        ('油そば', '油そば'),
       
    )

    # サンプル項目1 ラーメンの味
    sample_1 = models.TextField(
        verbose_name='味',
        choices=ramen_taste,
        blank=True,
        null=True,
    )
    
    
    # サンプル項目2 満足度合い
    sample_satisfaction = models.IntegerField(
        verbose_name='満足度評価',
        blank=True,
        null=True,
    )

   # サンプル項目3 こってり度合い 
    sample_3 = models.IntegerField(
        verbose_name='こってり度評価',
        blank=True,
        null=True,
    )

    # サンプル項目4 辛さ度合い　(削除)
    sample_4 = models.IntegerField(
        verbose_name='からさ評価',
        blank=True,
        null=True,
    )
    
    #サンプル項目　麺の太さ
    ramen_hutosa = (
        (1, '極細麺(1.1mm)'),
        (2, '細麺(1.15mm)'),
        (3, '中細麺(1.25mm)'),
        (4, '中太麺(1.4mm)'),
        (5, '太麺(1.7〜1.875mm)'),
        (6, '極太麺(2.2〜2.5mm)'),
    )
    
    sample_menhutosa = models.IntegerField(
        verbose_name='麺の太さ',
        choices=ramen_hutosa,
        blank=True,
        null=True,
    )
    
    # サンプル項目5 値段評価
    sample_5 = models.IntegerField(
        verbose_name='値段評価',
        blank=True,
        null=True,
    )
    
    #サンプル項目5.1 値段
    sample_cost = models.CharField(
        verbose_name='値段',
        max_length=10,
        blank=True,
        null=True,
    )
    
    # サンプル項目6 アクセス
    sample_6 = models.IntegerField(
        verbose_name='アクセス評価',
        blank=True,
        null=True,
    )

    #サンプル項目 URL
    sample_url = models.URLField(
        verbose_name='ホームページ',
        max_length=100,
        blank=True,
        null=True,
    )
    
    #サンプル項目8 感想
    memo = models.TextField(
        verbose_name='コメント欄',
        max_length=300,
        blank=True,
        null=True,
    )
    
    #サンプル項目9 来店日付
    date = models.DateField(blank=True, null=True)
    
    #サンプル項目10 画像
    image = models.ImageField(
        upload_to = '',
        verbose_name='添付画像',
        null=True,
        blank=True,
    )
    

    
    # 以下、管理項目

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CreatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
        editable=False,
    )


    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.name

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'サイト'
        verbose_name_plural = 'サイト'
