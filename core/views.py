from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.views import View
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *


class NoContextView(View):
    template_name = None # required

    def get(self, request):
        return render(request, self.template_name)

class AboutView(NoContextView):
    template_name = 'about.html'

class ContactsView(NoContextView):
    template_name = 'contacts.html'

class QuestionsView(NoContextView):
    template_name = 'faq.html'

# class AboutView(View):
#     def get(self, request):
#         return render(request, 'about.html')

# Create your views here.
def homepage(request):
    context = {}
    posts_list = Post.objects.all() # SELECT * FROM Post;
    context["posts"] = posts_list

    shorts_list = Short.objects.all()
    context["shorts"] = shorts_list

    return render(request, "home.html", context)


def post_detail(request, id):
    context = {}
    post_object = Post.objects.get(id=id)
    context["post"] = post_object
    comment_form = CommentForm()
    context["comment_form"] = comment_form
    comments_list = Comment.objects.filter(post=post_object)
    context['comments'] = comments_list
    # от начала до сюда

    if request.method == "GET":
        return render(request, "post_info.html", context)
    elif request.method == "POST":
        # от сюда до конца
        if 'like' in request.POST:
            post_object.likes += 1
            post_object.save()
            Notification.objects.create(
                user=post_object.creator,
                text=f"{request.user.username} лайкнул ваш пост с id {post_object.id} "
            )
            return redirect(post_detail, id=id)
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.created_by = request.user
                new_comment.post = post_object
                new_comment.save()

                Notification.objects.create(
                    user=post_object.creator,
                    text=f"{request.user.username} оставил комментарий"
                )
                return HttpResponse("done")


class PostDetailView(View):
    def get_context(self):
        id = self.kwargs["id"]
        context = {}
        post_object = Post.objects.get(id=id)
        context["post"] = post_object
        comment_form = CommentForm()
        context["comment_form"] = comment_form
        comments_list = Comment.objects.filter(post=post_object)
        context['comments'] = comments_list
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context()
        return render(request, "post_info.html", context) 
    
    def post(self, request, *args, **kwargs):
        context = self.get_context()
        post_object = context["post"]
        if 'like' in request.POST:
            post_object.likes += 1
            post_object.save()
            Notification.objects.create(
                user=post_object.creator,
                text=f"{request.user.username} лайкнул ваш пост с id {post_object.id} "
            )
        else:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.created_by = request.user
                new_comment.post = post_object
                new_comment.save()

                Notification.objects.create(
                    user=post_object.creator,
                    text=f"{request.user.username} оставил комментарий"
                )
        return redirect('post-detail-cbv', id=post_object.id)


class PostListView(ListView):
    queryset = Post.objects.all()
    # template_name = 'core/post_list.html'

def profile_detail(request, id):
    context = {}
    profile = Profile.objects.get(id=id)
    context['profile'] = profile

    if request.method == "POST":
        profile.subscribers.add(request.user)
        profile.save()
    
    return render(request, 'profile_detail.html', context)


def add_profile(request):
    profile_form = ProfileForm()
    context = {'profile_form': profile_form}

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_object = profile_form.save(commit=False)
            profile_object.user = request.user
            profile_object.save()
            return redirect(profile_detail, id=profile_object.id)
        else:
            return HttpResponse("Not valid")

    return render(request, 'add_profile.html', context)


def shorts(request):
    context = {
        'shorts_list': Short.objects.all()
    }
    return render(request, "shorts.html", context)

class ShortsListView(ListView):
    queryset = Short.objects.all()


def short_info(request, id):
    try:
        short = Short.objects.get(id=id)
    except Short.DoesNotExist:
        return HttpResponse(
            "Ошибка 404. Такого объекта не существует"
        )
    short.views_qty += 1
    if request.user.is_authenticated:
        short.viewed_users.add(request.user)
    short.save()
    context = {"short": short}
    return render(request, "short_info.html", context)


class ShortDetailView(DetailView):
    queryset = Short.objects.all()
    template_name = "short_info.html"

    def get(self, request, *args, **kwargs):
        short = self.get_object()
        short.views_qty += 1
        if request.user.is_authenticated:
            short.viewed_users.add(request.user)
        short.save()
        return super().get(request, *args, **kwargs)
    

def saved_posts_list(request):
    posts = Post.objects.filter(saved_posts__user=request.user)
    context = {'posts': posts}
    return render(request, 'saved_posts.html', context)


def user_posts(request, user_id):
    user = User.objects.get(id=user_id)
    posts = Post.objects.filter(creator=user)
    context = {
        "user": user,
        "posts": posts
    }
    return render(request, 'user_posts.html', context)


def create_post(request):
    if request.method == "GET":
        return render(request, "create_post_form.html")
    elif request.method == "POST":
        data = request.POST  # словарь с данными с html-формы
        # print(data)
        new_post = Post()
        new_post.name = data["post_name"]
        new_post.description = data["description"]
        new_post.photo = request.FILES["photo"]
        new_post.creator = request.user
        new_post.save()
        return HttpResponse("done")


def update_post(request, id):

    context = {}
    post_object = Post.objects.get(id=id)

    if request.user != post_object.creator:
        return HttpResponse("нет доступа")

    if request.method == "POST":
        post_form = PostForm(
            data=request.POST,
            files=request.FILES,
            instance=post_object
        )
        if post_form.is_valid():
            post_form.save()
            return redirect(post_detail, id=post_object.id)
        else:
            messages.warning(request, "Форма не валидна")
            context["post_form"] = post_form
            return render(request, 'update_post.html', context)

    post_form = PostForm(instance=post_object)
    context["post_form"] = post_form
    return render(request, 'update_post.html', context)


def detele_post(request, id):
    post = Post.objects.get(id=id)

    if request.user != post.creator:
        return HttpResponse("нет доступа")

    post.delete()
    return redirect(homepage)


def add_post_form(request):
    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post_object = post_form.save(commit=False)
            post_object.creator = request.user
            post_object.save()
            return redirect(post_detail, id=post_object.id)
        else:
            messages.warning(request, f"Форма не валидна: {post_form.errors}")

    post_form = PostForm()
    context = {}
    context["post_form"] = post_form
    return render(request, 'create_post_django_form.html', context)


# from django.contrib.auth.decorators import login_required
@login_required(login_url='/users/sign-in/')
def add_short(request):
    # if not request.user.is_authenticated:
    #     return redirect('/')

    if request.method == "GET":
        return render(request, 'short_form.html')
    elif request.method == "POST":
        new_short_object = Short(
            user=request.user,
            video=request.FILES["video_file"]
        )
        new_short_object.save()
        return redirect('shorts-info', id=new_short_object.id)


def update_short(request, id):
    short = Short.objects.get(id=id)
    if request.method == "POST":
        new_description = request.POST["description"]
        short.description = new_description
        short.save()
        return redirect(short_info, id=short.id)

    context = {'short': short}
    return render(request, 'update_short.html', context)


def add_saved(request):
    if request.method == "POST":
        post_id = request.POST["post_id"]
        post_object = Post.objects.get(id=post_id)
        saved_post, created = SavedPosts.objects.get_or_create(
            user=request.user
        )
        saved_post.post.add(post_object)
        saved_post.save()
        return redirect('/saved_posts/')

def search(request):
    return render(request, 'search.html')

def search_result(request):
    key_word = request.GET["key_word"]
    # posts = Post.objects.filter(name__icontains=key_word)
    posts = Post.objects.filter(
        Q(name__icontains=key_word) |
        Q(description__icontains=key_word)
    )
    context = {"posts": posts}
    return render(request, 'home.html', context)


class SearchView(View):
    def get(self, request):
        return render(request, 'search.html')


class SearchResultView(View):
    def get(self, request):
        key_word = request.GET["key_word"]
        # posts = Post.objects.filter(name__icontains=key_word)
        posts = Post.objects.filter(
            Q(name__icontains=key_word) |
            Q(description__icontains=key_word)
        )
        context = {"posts": posts}
        return render(request, 'home.html', context)


def subscribe(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    profile.subscribers.add(request.user)
    profile.save()
    messages.success(request, "Вы успешно подписались!")

    new_notification = Notification(
        user=profile.user,
        text=f"Пользователь {request.user.username} подписался на вас!"
    )
    new_notification.save()

    return redirect(f'/profile/{profile.id}/')


def unsubscribe(request, profile_id):
    profile = Profile.objects.get(id=profile_id)
    profile.subscribers.remove(request.user)
    profile.save()
    messages.warning(request, "Вы успешно оптисались!")
    return redirect(f'/profile/{profile.id}/')


def notifications(request):
    notifications_list = Notification.objects.filter(user=request.user)
    for notification in notifications_list:
        notification.is_showed = True
    Notification.objects.bulk_update(notifications_list, ['is_showed'])
    context = {"notifications": notifications_list}
    return render(
        request=request,
        template_name='notifications.html',
        context=context,
    )

class NotificationView(View):
    def get(self, request):
        notifications_list = Notification.objects.filter(user=request.user)
        for notification in notifications_list:
            notification.is_showed = True
        Notification.objects.bulk_update(notifications_list, ['is_showed'])
        context = {"notifications": notifications_list}
        return render(
            request=request,
            template_name='notifications.html',
            context=context,
        )

def comment_edit(request, id):
    comment = Comment.objects.get(id=id)

    if request.user != comment.created_by:
        messages.warning(request, "Нет доступа")
        return redirect(post_detail, id=comment.post.id)
    
    if request.method == "POST":
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect(post_detail, id=comment.post.id)

    form = CommentForm(instance=comment)
    context = {"form": form}
    return render(request, 'comment_edit.html', context)


def comment_delete(request, id):
    comment = Comment.objects.get(id=id)

    if request.user != comment.created_by:
        messages.warning(request, "Нет доступа")
        return redirect(post_detail, id=comment.post.id)

    comment.delete()
    return redirect(post_detail, id=comment.post.id)


class SubscribesView(View):
    def get(self, request, *args, **kwargs):
        user_object = User.objects.get(id=kwargs['user_id'])
        profiles_list = user_object.followed_profile.all()
        context = {"profiles_list": profiles_list}
        return render(request, 'subscribers.html', context)
