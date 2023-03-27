from django.urls import path
from . import views


app_name='ecommerce_app'

urlpatterns = [
    path('',views.allProdCat,name='allProdCat'),
    path('logout/',views.logout,name= "logout"),
    path('register/',views.register,name="register"),
    path('login/',views.login_page,name="login"),

    path('favviewpage', views.favviewpage, name="favviewpage"),
    path('add_favorite/<str:product_id>/', views.add_favorite, name='add_favorite'),
    path('remove_fav/<int:product_id>', views.remove_fav, name="remove_fav"),

    path('<slug:c_slug>/',views.allProdCat,name='product_by_category'),
    path('<slug:c_slug>/<slug:product_slug>/',views.proDetail,name='prodCatdetail')
]