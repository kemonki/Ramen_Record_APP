from crispy_forms.helper import FormHelper
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
from .filters import ItemFilterSet
from .forms import ItemForm
from .models import Item
from django.shortcuts import render

#Geocoding API を使用する際のモジュール設定
from django.http import JsonResponse
import googlemaps
from django.shortcuts import render

# 現在地より800m圏内のラーメン店舗情報を表示する
def geocode_address_view(request):
    return render(request, 'geocode_template.html')

# アプリケーションのルーティング設定
def render_search_view(request):
    return render(request, 'search_form.html')

def search_results_view(request):
    return render(request, 'search_results.html')



# 未ログインのユーザーにアクセスを許可する場合は、LoginRequiredMixinを継承から外してください。
#
# LoginRequiredMixin：未ログインのユーザーをログイン画面に誘導するMixin
# 参考：https://docs.djangoproject.com/ja/2.1/topics/auth/default/#the-loginrequired-mixin

class ItemFilterView(LoginRequiredMixin, FilterView):
    """
    ビュー：一覧表示画面
    以下のパッケージを使用
    ・django-filter 一覧画面(ListView)に検索機能を追加
    https://django-filter.readthedocs.io/en/master/
    """
    model = Item
    
    # django-filter 設定
    filterset_class = ItemFilterSet
    # django-filter ver2.0対応 クエリ未設定時に全件表示する設定
    strict = False

    # 1ページの表示
    paginate_by = 10

    

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """

        # 一覧画面内の遷移(GETクエリがある)ならクエリを保存する
        if request.GET:
            request.session['query'] = request.GET
        # 詳細画面・登録画面からの遷移(GETクエリはない)ならクエリを復元する
        else:
            request.GET = request.GET.copy()
            if 'query' in request.session.keys():
                for key in request.session['query'].keys():
                    request.GET[key] = request.session['query'][key]

        return super().get(request, **kwargs)

    def get_queryset(self):
        q_word = self.request.GET.get('query')

        if q_word:
           object_list = Item.objects.filter(
             Q(name__icontains = q_word) | Q(name2__icontains = q_word) |
             Q(name3__icontains = q_word) | Q(sample_1__icontains = q_word))
        else:
           object_list = Item.objects.all()
        return object_list


    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """

        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset_class(self.request.GET, queryset=self.get_queryset())
        return context

class ItemDetailView(LoginRequiredMixin, DetailView):
    """
    ビュー：詳細画面
    """
    model = Item

    def get_context_data(self, **kwargs):
        """
        表示データの設定
        """
        # 表示データの追加はここで 例：
        # kwargs['sample'] = 'sample'
        return super().get_context_data(**kwargs)


class ItemCreateView(LoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        登録処理
        """
        item = form.save(commit=False)
        item.created_by = self.request.user
        item.created_at = timezone.now()
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    """
    ビュー：更新画面
    """
    model = Item
    form_class = ItemForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        """
        更新処理
        """
        item = form.save(commit=False)
        item.updated_by = self.request.user
        item.updated_at = timezone.now()
        item.save()

        return HttpResponseRedirect(self.success_url)


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    """
    ビュー：削除画面
    """
    model = Item
    success_url = reverse_lazy('index')

    def delete(self, request, *args, **kwargs):
        """
        削除処理
        """
        item = self.get_object()
        item.delete()

        return HttpResponseRedirect(self.success_url)
    

#Geocoding APIの住所を地理座標に変換するための関数
    
def geocode_address(request):
    if request.method == 'GET':
        address = request.GET.get('address', '')
        api_key = os.environ.get('GOOGLE_MAPS_API_KEY')
        if api_key:
            gmaps = googlemaps.Client(key=api_key)
            geocode_result = gmaps.geocode(address)
            if geocode_result:
                lat_lng = geocode_result[0]['geometry']['location']
                return JsonResponse({'latitude': lat_lng['lat'], 'longitude': lat_lng['lng']})
            else:
                return JsonResponse({'error': 'Invalid address'})
        else:
            return JsonResponse({'error': 'API key not found'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


