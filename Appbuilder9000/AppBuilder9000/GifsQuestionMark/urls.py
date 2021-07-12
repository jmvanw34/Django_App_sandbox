# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='GifsQuestionMark_home'),
    path('create_quote/', views.create_quote, name='GifsQuestionMark_create'),
    path('view_quotes/', views.view_quotes, name='GifsQuestionMark_view_quotes'),
    path('delTag/<int:id>/', views.removeTag, name="delTag"),
    path('delQuote/<int:id>/', views.removeQuote, name="delQuote"),
    path('success/', views.success, name='success'),
    path('tags/', views.view_tag, name='GifsQuestionMark_view_tags'),
    path('quote_content/<int:id>/', views.quote_content, name='GifsQuestionMark_quote_content'),
    path('quote_content/<int:id>/update/', views.editQuote.as_view(), name="edit_quote"),
    path('scraper/', views.goodreads_quote_scraper, name='GifsQuestionMark_scraper'),
    path('api/', views.api, name='GifsQuestionMark_api'),
    # path('tags/', views.view_tag, name='GifsQuestionMark_delete_tags'),
    path('post/ajax/tag', views.post_tag, name="post_tag"),
    # path('admin/', admin.site.urls),
    path('questions/', views.QuestionsAPIView.as_view(), name="GifsQuestionMark_questions"),
    path('api_search/', views.api_search, name='GifsQuestionMark_api_search'),






]
