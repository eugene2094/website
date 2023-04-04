from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Category
from django.db.models import Q
from .forms import PostForm
import datetime
from django.contrib.auth.decorators import login_required


def get_categories():
    all = Category.objects.all()
    count = all.count()
    half = count / 2 + count % 2
    first_half = all[:half]
    second_half = all[half:]
    return {'cat1': first_half, "cat2": second_half}


# Create your views here.
def index(request):
    # posts = Post.objects.filter(title__contains="django")
    # posts = Post.objects.filter(published_date__year="2022")
    # posts = Post.objects.filter(category__name='news')
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)  # Show 25 contacts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    context.update(get_categories())
    return render(request, "newsBlog/index.html", context)


def post(request, id=None):
    posts = get_object_or_404(Post, pk=id)
    context = {'post': posts}
    context.update(get_categories())
    return render(request, 'newsBlog/post.html', context)


def category(request, id=None):
    c = get_object_or_404(Category, pk=id)
    posts = Post.objects.filter(category=c).order_by("-published_date")
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'newsBlog/index.html', context)


def search(request):
    query = request.POST.get('query')
    posts = Post.objects.filter(Q(content__icontains=query) | Q(title__icontains=query))
    context = {'posts': posts}
    context.update(get_categories())
    return render(request, 'newsBlog/index.html', context)


@login_required
def create(request):
    if request.method == 'POST':
        form = PostForm(data=request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.published_date = datetime.datetime.now()
            post.user = request.user
            post.save()
            form.save_m2m()
        return redirect('index')
    form = PostForm()
    context = {'form': form}
    context.update(get_categories())
    return render(request, 'newsBlog/create.html', context)
