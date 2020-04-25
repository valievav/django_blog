from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.conf import settings
from .models import Post
from .forms import EmailPostForm


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


def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id,
                             status='published')
    sent = False
    if request.method == 'POST':  # user submitted form
        form = EmailPostForm(request.POST)  # prepare form with data
        if form.is_valid():
            cd = form.cleaned_data  # dict with valid fields
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you to read '{post.title}'"
            message = f"Read post '{post.title}' at {post_url}\n\n" \
                      f"{cd['name']}\'s comments: {cd['comments']}\n\n" \
                      f"{cd['name']}\'s email: {cd['email']}"

            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['email_to']])
            sent = True  # for template to display success message
    else:
        form = EmailPostForm()  # display empty form

    return render(request, 'blog/post/share.html', {'post': post,
                                                    'form': form,
                                                    'sent': sent})
