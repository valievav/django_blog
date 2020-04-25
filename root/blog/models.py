from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# custom manager (useful shortcut if some db operations are performed often)
# Post.objects.filter(status='published') == Post.published.all()
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    objects = models.Manager()  # default manager (1st manager declared in a model is default one)
    published = PublishedManager()  # custom manager (shortcut to exclude status='published' in a query)


    STATUS_CHOICES = (('draft', 'Draft'),
                      ('published', 'Published'))
    # model fields
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')  # will generate unique slag for date
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)  # sets date to now (used for creation)
    updated = models.DateTimeField(auto_now=True)  # sets to date now (used for last modified, updates field on save())
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ('-publish',)

    def get_absolute_url(self):  # will be used to link to specific post
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])

    def __str__(self):
        return self.title
