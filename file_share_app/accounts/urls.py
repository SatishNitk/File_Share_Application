from django.urls import path,include,re_path
from accounts.views import *

urlpatterns = [
    path('upload/', upload_view, name="upload_view"),
    path('home/', home_view, name="home_view"),
    path('login/', login_view, name="login_view"),
    path('signup/', signup_view, name="signup_view"),
    path('logout/', logout_view, name="logout_view"),
    path('delete/<int:pk>/', delete_view, name="delete_view"),
    path('book_list/', book_list_view, name='book_list_view'),
    path('book_listu/', book_list_view_by_u, name='book_list_view_by_u'),
    path('book_listother/', book_list_view_by_other, name='book_list_view_by_other'),
    path('audio_download/', mp3downloader_view, name='mp3downloader_view'),
    path('video_download/', mp4downloader_view, name='mp4downloader_view'),
    path('downloader/', pdfdownloader_view, name='downloader_view'),
    re_path(r'^test/', getFile)

]

