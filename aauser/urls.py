from django.urls import path, register_converter, include
from . import views

from admin_d. converters import ObjectIdConverter

register_converter(ObjectIdConverter, 'ObjectId')




urlpatterns = [
    path('', views.home, name="home"),
    path('collection/<slug:slug>/', views.view_collection, name='view_collection'),
    path('catelog/<slug:slug>/', views.view_catlog, name='view_catlog'),
    path('product/<slug:url_key>/', views.product_detail, name='product'),
    path("checkout/", views.checkout, name="checkout"),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('otp_verify/', views.otp_verify, name='otp_verify'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('forgot_otp_verify/', views.forgot_otp_verify, name='forgot_otp_verify'),
    # path("place-order/<str:order_id>/", views.place_order_page, name="place_order"),
    path('order-success/', views.order_success, name='order_success'),
    path("orders/<ObjectId:post_id>/", views.order_detail, name="order_detail"),
    path("orders/", views.orders, name="orders"),
    
    path("profile/", views.profile, name="profile"),
    path("add-address/", views.add_address, name="add_address"),
    
    
    path("contact/", views.contact, name="contact"),
    path("about/", views.about, name="about"),
    path("shipping/", views.shipping, name="shipping"),
    path('refund/', views.refund, name="refund"),
    path('terms-of-service/', views.terms, name="terms"),
]