from django.urls import path
from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.post_list, name='post_list'),  # function-based post_list view
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),  # function-based post_list view WITH tags
    # path('', views.PostListView.as_view(), name='post_list'),  # class-based post_list view (w/o tags url view)
    path('<int:year>/<int:month>/<int:day>/<slug:post>', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
]
