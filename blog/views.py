from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required,permission_required
from django.shortcuts import get_object_or_404 , redirect, render
from django.forms import formset_factory
from . import forms, models
from django.db.models import Q
from itertools import chain
from django.views import View
from django.utils.decorators import method_decorator




class PhotoFeed(View):
    def get(self,request):
        photos = models.Photo.Objects.filter(
            uploader__in=request.user.follows.all()).order_by('-date_created')
        context = {
            'photos': photos,
        }
        return render(request, 'blog/photo_feed.html', context=context)

'''def photo_feed(request):
    photos = models.Photo.Objects.filter(
        uploader__in=request.user.follows.all()).order_by('-date_created')
    context = {
        'photos': photos,
    }
    return render(request, 'blog/photo_feed.html', context=context)'''

class FollowUsers(View):
    @method_decorator(login_required)
    def get(self,request):
        form = forms.FollowUsersForm(instance=request.user)
        return render(request, 'blog/follow_users_form.html', context={'form': form})

    def post(self,request):
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')

'''def follow_users(request):
    form = forms.FollowUsersForm(instance=request.user)
    
    if request.method == 'POST':
        form = forms.FollowUsersForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    return render(request, 'blog/follow_users_form.html', context={'form': form})'''

'''class Create_multiple_photos(View):
    @method_decorator(login_required, permission_required('blog.add_photo'))
    def get(self, request):
        PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
        formset = PhotoFormSet()
        return render(request, 'blog/create_multiple_photos.html', {'formset': formset})

    def post(self,request):
            PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
            formset = PhotoFormSet(request.POST, request.FILES)
            if formset.is_valid():
                for form in formset:
                    if form.cleaned_data:
                        photo = form.save(commit=False)
                        photo.uploader = request.user
                        photo.save()
                return redirect('home')
            return render(request, 'blog/create_multiple_photos.html', {'formset': formset})'''


def create_multiple_photos(request):
    PhotoFormSet = formset_factory(forms.PhotoForm, extra=5)
    formset = PhotoFormSet()
    if request.method == 'POST' :
        formset = PhotoFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    photo = form.save(commit=False)
                    photo.uploader = request.user
                    photo.save()
            return redirect('home')
        return render(request, 'blog/create_multiple_photos.html', {'formset': formset})

    return render(request, 'blog/create_multiple_photos.html',{'formset': formset})

class PhotoUpload(View):
    @method_decorator(login_required, permission_required('blog.add_photo'))
    def get (self,request):
        form = forms.PhotoForm()
        return render(request, 'blog/photo_upload.html', context={'form': form})

    def post (self,request):
        if request.method == 'POST':
            form = forms.PhotoForm(request.POST, request.FILES)
            if form.is_valid():
                photo = form.save(commit=False)
                # set the uploader to the user before saving the model
                photo.uploader = request.user
                # now we can save
                photo.save()
                return redirect('home')

'''def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            # set the uploader to the user before saving the model
            photo.uploader = request.user
            # now we can save
            photo.save()
            return redirect('home')
    return render(request, 'blog/photo_upload.html', context={'form': form})'''



class Blog_and_photo_upload(View):
    @method_decorator(login_required, permission_required(['blog.add_photo', 'blog.add_blog']))
    def get(self,request):
        blog_form = forms.BlogForm()
        photo_form = forms.PhotoForm()
        context = {
            'blog_form': blog_form,
            'photo_form': photo_form,}
        return render(request, 'blog/create_blog_post.html', context=context)

    def post(self,request):
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author = request.user
            blog.photo = photo
            blog.save()
            blog.contributors.add(request.user, through_defaults={'contribution': 'Primary Author'})
            return redirect('home')



'''def blog_and_photo_upload(request):
    blog_form = forms.BlogForm()
    photo_form=forms.PhotoForm()
    if request.method=='POST' :
        blog_form = forms.BlogForm(request.POST)
        photo_form = forms.PhotoForm(request.POST,request.FILES)
        if all([blog_form.is_valid(), photo_form.is_valid()]):
            photo= photo_form.save( commit =False)
            photo.uploader= request.user
            photo.save()
            blog = blog_form.save(commit=False)
            blog.author= request.user
            blog.photo = photo
            blog.save()
            blog.contributors.add(request.user, through_defaults={'contribution': 'Primary Author'})
            return redirect('home')
    context = {
        'blog_form': blog_form,
        'photo_form': photo_form,
    }
    return render(request, 'blog/create_blog_post.html', context=context)'''


class Edit_Blog (View):
    @method_decorator(login_required, permission_required('blog.change_blog'))
    def get(self,request,blog_id):
        blog = get_object_or_404(models.Blog, id=blog_id)
        edit_form = forms.BlogForm(instance=blog)
        delete_form = forms.DeleteBlogForm()

        context = {
            'edit_form': edit_form,
            'delete_form': delete_form,
        }
        return render(request, 'blog/edit_blog.html', context=context)

    @method_decorator(login_required, permission_required('blog.change_blog'))
    def post(self,request,blog_id):
        blog = get_object_or_404(models.Blog, id=blog_id)
        if 'edit_blog' in request.POST:
            edit_form = forms.BlogForm(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_blog' in request.POST:
            delete_form = forms.DeleteBlogForm(request.POST)
            if delete_form.is_valid():
                blog.delete()
                return redirect('home')



'''def edit_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id = blog_id)
    edit_form = forms.BlogForm(instance=blog)
    delete_form = forms.DeleteBlogForm()
    if request.method == 'POST':
        if 'edit_blog' in request.POST:
            edit_form = forms.BlogForm(request.POST, instance=blog)
            if edit_form.is_valid():
                edit_form.save()
                return redirect('home')
        if 'delete_blog' in request.POST:
            delete_form = forms.DeleteBlogForm(request.POST)
            if delete_form.is_valid():
                blog.delete()
                return redirect('home')
    context = {
        'edit_form': edit_form,
        'delete_form': delete_form,
    }
    return render(request, 'blog/edit_blog.html', context=context)'''


class Home(View):
    @method_decorator(login_required)
    def get(self,request):
        blogs = models.Blog.objects.filter(Q(contributors__in=request.user.follows.all())| Q(starred=True))
        photos = models.Photo.objects.filter(
            uploader__in=request.user.follows.all()).exclude(
                blog__in=blogs
        )
        blogs_and_photos = sorted(
            chain(blogs, photos),
            key=lambda instance: instance.date_created,
            reverse=True
        )

        paginator = Paginator(blogs_and_photos,4)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'page_obj': page_obj,
                   }
        return render( request, 'blog/home.html', context=context)


def photo_feed(request):
        photos = models.Photo.objects.filter(
            uploader__in=request.user.follows.all()).order_by('-date_created')
        paginator = Paginator(photos, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, 'blog/photo_feed.html', context=context)


class View_blog(View):
    @method_decorator(login_required)
    def get(self,request,blog_id):
        blog = get_object_or_404(models.Blog, id=blog_id)
        return render(request, 'blog/view_blog.html', {'blog': blog})

'''def view_blog(request, blog_id):
    blog = get_object_or_404(models.Blog, id=blog_id)
    return render(request, 'blog/view_blog.html', {'blog': blog})'''