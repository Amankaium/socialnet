from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *

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
    if request.method == "GET":
        return render(request, "post_info.html", context)
    elif request.method == "POST":
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

def short_info(request, id):
    short = Short.objects.get(id=id)
    short.views_qty += 1
    short.viewed_users.add(request.user)
    short.save()
    context = {"short": short}
    return render(request, "short_info.html", context)


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

