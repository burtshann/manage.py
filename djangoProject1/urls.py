print("views.py loaded")
"""
URL configuration for djangoProject1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
# from django.urls import path
# from myapp import views
# from django.urls import path
# from myapp import views
# from django.urls import path
# from myapp import views
# from django.urls import path
# from myapp.views import index, get_high_freq_data ,download_video  #
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from myapp.views import index, get_high_freq_data, download_video, get_max_danmaku,run_pygame_game

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('index/', views.index, name='index'),
    # path() 的常用参数包括以下几项：
    # route（路径）：定义 URL 中的路径，支持静态部分和动态部分（可变参数）。
    # view（视图函数）：指定当用户访问该 URL 时应调用的视图函数。
    # kwargs（可选的关键字参数）：可以给视图函数传递额外的参数。
    # name（可选的名称）：为该路径命名，以便在模板中反向生成 URL。
    # 配置访问主页的 URL 路径
# ]


# urlpatterns = [
#     path('', views.index, name='index'),
#     path('high_freq_data/', views.get_high_freq_data, name='high_freq_data'),
# ]


# urlpatterns = [
#     path('', views.index, name='index'),  # 首页
#     path('high-freq-data/', views.get_high_freq_data, name='get_high_freq_data'),  # 高频词数据 API
# ]


# urlpatterns = [
#     path('high_freq_data/', views.get_high_freq_data, name='high_freq_data'),
#     path('', views.index, name='index'),
# ]


urlpatterns = [
    path('', index, name='index'),  # 首页
    path('get_high_freq_data/', get_high_freq_data, name='get_high_freq_data'),  # 高频词数据
    path('download_video/', download_video, name='download_video'),
    path('get_max_danmaku/', get_max_danmaku, name='get_max_danmaku'),
]
if settings.DEBUG:
    urlpatterns += static(settings.DOWNLOAD_URL, document_root=settings.DOWNLOAD_ROOT)