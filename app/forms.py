from django import forms
from django.contrib.admin.widgets import AdminDateWidget
from .models import Item
import crispy_forms.helper as crispy_helper
from crispy_forms.layout import Submit


class ItemForm(forms.ModelForm):
    """
    モデルフォーム構成クラス
    ・公式 モデルからフォームを作成する
    https://docs.djangoproject.com/ja/2.1/topics/forms/modelforms/
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = crispy_helper.FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        
    class Meta:
         model = Item
         exclude = []

        

    

        # 以下のフィールド以外が入力フォームに表示される
        # AutoField
        # auto_now=True
        # auto_now_add=Ture
        # editable=False
