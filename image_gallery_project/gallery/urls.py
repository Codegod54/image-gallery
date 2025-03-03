from django.urls import path
from . import views

urlpatterns = [
    # Public views
    path('', views.gallery_view, name='gallery'),
    path('image/<int:image_id>/', views.image_detail, name='image_detail'),
    path('download/<int:image_id>/', views.download_image, name='download_image'),

    # Admin views
    path('login/', views.admin_login, name='admin_login'),
    path('logout/', views.admin_logout, name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_image, name='upload'),
    path('edit/<int:image_id>/', views.edit_image, name='edit_image'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),
]
