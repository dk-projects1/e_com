from django.urls import path, register_converter, include
from . import views
from . converters import ObjectIdConverter

register_converter(ObjectIdConverter, 'ObjectId')


urlpatterns = [
    path('', views.admin_login, name="admin"),
    path('logout/', views.logout, name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('collection_list', views.collection_list, name="collection_list"),
    path('new_collection', views.new_collection, name='new_collection'),
    path('edit_collection/<ObjectId:post_id>/', views.collection_edit, name='edit_collection'),
    path('delete_collections/<ObjectId:post_id>/', views.delete_collections, name='delete_collections'),
    path('category', views.categories, name="category"),
    path('new_category', views.new_category, name='new_category'),
    path('edit_category/<ObjectId:post_id>/', views.edit_category, name='edit_category'),
    path('delete_category/<ObjectId:post_id>/', views.delete_category, name='delete_category'),
    path('product_list/', views.product_list, name='product_list'),
    path('new_product', views.new_product, name="new_product"),
    path('edit_product/<ObjectId:post_id>/', views.product_edit, name='edit_product'),
    path('delete_product/<ObjectId:post_id>/', views.delete_product, name='delete_product'),
    path('coupon_list/', views.coupon_list, name='coupon_list'),
    path('new_coupon', views.new_coupon, name="new_coupon"),
    path('edit_coupon/<ObjectId:post_id>/', views.edit_coupon, name='edit_coupon'),
    path('delete_coupon/<ObjectId:post_id>/', views.delete_coupon, name='delete_coupon'),
    path('pages', views.paages, name="paages"),
    path('new_layout', views.new_layout, name="new_layout"),
    path('delete_layout/<ObjectId:post_id>/', views.delete_layout, name='delete_layout'),
    path('edit_layout/<ObjectId:post_id>/', views.edit_layout, name='edit_layout'),
    path('show_credentials', views.show_credentials, name="show_credentials"),
    path('edit_credentials/<ObjectId:post_id>/', views.edit_credentials, name='edit_credentials'),
    path('edit_footer/<ObjectId:post_id>/', views.edit_footer, name='edit_footer'),
]

