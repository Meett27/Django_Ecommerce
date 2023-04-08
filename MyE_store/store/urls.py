from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name= 'store'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('shope_by_brand/', views.Product_categories.as_view(), name = 'category'),
    path('product/<slug>/', views.ProductDetails.as_view(), name= 'item'),
    path('product_by_category/<int:cat_id>/', views.Products_by_categories.as_view(), name= 'product_by_category'),
    path('cart/', views.cart, name= 'cart'),
    path('profile_page/', views.ProfileDetails.as_view(), name= 'profile'),
    path('update_profile_page/', views.UpdateUserProfile.as_view(), name= 'update_profile'),
    path('update_cart_items/', views.update_cart_items, name= 'update_cart_items'), 
]
urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)