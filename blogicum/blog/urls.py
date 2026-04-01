from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    
    # Работа с постами (CRUD)
    # Пункт 8: Используем post_id вместо id
    path('posts/<int:post_id>/', views.post_detail, name='post_detail'),
    path('posts/create/', views.post_create, name='post_create'),
    path('posts/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    
    # Комментарии
    path('posts/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    
    # Категории
    path(
        'category/<slug:category_slug>/',
        views.category_posts,
        name='category_posts'
    ),
    
    # Профиль пользователя (Пункт 6)
    path('profile/<str:username>/', views.profile, name='profile'),
    # Также можно добавить редактирование профиля, если это есть в задании
    path('edit_profile/', views.edit_profile, name='edit_profile'),
]
