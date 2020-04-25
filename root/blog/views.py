from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .models import Post


# class-based view
class PostListView(ListView):
    queryset = Post.published.all()  # get only published posts
    context_object_name = 'posts'
    paginate_by = 5
    template_name = 'blog/post/list.html'


# function-based view of the above class
def post_list(request):
    object_list = Post.published.all()  # get only published posts
    paginator = Paginator(object_list, 5)  # 5 posts per page
    page = request.GET.get('page')  # current page number that's requested

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # if current page number is not int, return 1st page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # if current page number > number of results, return last page

    return render(request,
                  'blog/post/list.html',
                  {'page': page,
                   'posts': posts})


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'blog/post/detail.html',
                  {'post': post})
