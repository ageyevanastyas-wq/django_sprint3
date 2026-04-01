from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone # Используем это вместо datetime.now()
from django.contrib.auth.decorators import login_required

from .models import Post, Category, User
from .forms import PostForm, CommentForm

# Пункт 4 и 11: переименовали posts() и добавили timezone.now()
def get_published_posts():
    """Вспомогательная функция для получения опубликованных постов."""
    return Post.objects.select_related(
        'category',
        'location',
        'author'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )

def index(request):
    """Главная страница с пагинацией (по 10 постов)."""
    post_list = get_published_posts()
    # Пункт 7: Внедряем пагинацию
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/index.html', {'page_obj': page_obj})

def post_detail(request, post_id):
    """Страница одного поста с комментариями."""
    # Пункт 8: Используем post_id вместо id
    post = get_object_or_404(Post, pk=post_id)
    
    # Пункт 5: Проверка, что неопубликованный пост видит только автор
    if not post.is_published or post.pub_date > timezone.now() or not post.category.is_published:
        if post.author != request.user:
            from django.http import Http404
            raise Http404("Пост не найден или у вас нет прав на просмотр.")

    comments = post.comments.all() # Загружаем комментарии
    form = CommentForm()
    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog/detail.html', context)

def category_posts(request, category_slug):
    """Публикации конкретной категории с пагинацией."""
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    post_list = get_published_posts().filter(category=category)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category.html', {
        'category': category,
        'page_obj': page_obj
    })

# Пункт 6: Добавляем профиль пользователя
def profile(request, username):
    author = get_object_or_404(User, username=username)
    post_list = Post.objects.filter(author=author)
    
    # Если зашел не автор профиля — фильтруем только опубликованное
    if request.user != author:
        post_list = post_list.filter(
            is_published=True,
            pub_date__lte=timezone.now(),
            category__is_published=True
        )
        
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/profile.html', {
        'profile': author,
        'page_obj': page_obj
    })
