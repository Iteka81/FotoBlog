
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView)
from django.urls import path

import authentication.views
import blog.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(
        template_name='authentication/login.html',
        redirect_authenticated_user=True),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', PasswordChangeView.as_view(
        template_name='authentication/password_change_form.html'),
         name='password_change'
         ),
    path('change-password-done/', PasswordChangeDoneView.as_view(
        template_name='authentication/password_change_done.html'),
         name='password_change_done'
         ),
    path('signup/', authentication.views.Signup_page.as_view(), name='signup'),
    path('profile-photo/upload', authentication.views.Upload_profile_photo.as_view(),
         name='upload_profile_photo'),
    path('home/', blog.views.Home.as_view(), name='home'),
    path('photo/upload/', blog.views.PhotoUpload.as_view(), name='photo_upload'),
    path('photo/feed/', blog.views.PhotoFeed.as_view, name='photo_feed'),
    path('blog/create', blog.views.Blog_and_photo_upload.as_view(), name='blog_create'),
    path('blog/<int:blog_id>' , blog.views.View_blog.as_view(), name='view_blog'),
    path('blog/<int:blog_id>/edit', blog.views.Edit_Blog.as_view(), name='edit_blog'),
    path('photo/upload-multiple/', blog.views.create_multiple_photos, name='create_multiple_photos'),
    path('follow-users/', blog.views.FollowUsers.as_view(), name='follow_users')
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)