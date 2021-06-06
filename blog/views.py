from django.contrib.auth import login
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import EmailPostForm, CommentForm, UserRegisterForm, UserLoginForm
from django.contrib import messages


# Create your views here.


def post_list(request):
    """Обработчик страницы со списком постов"""
    object_list = Post.objects.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get("page")
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, year, month, day, post):
    """Обработчик страницы с одним постом"""
    post = Post.objects.get(publish__year=year, publish__month=month, publish__day=day, slug=post)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
        else:
            comment_form = CommentForm()
            return render(request, 'blog/post/detail.html', {'post': post, "comments": comments,
                                                             "new_comment": new_comment,
                                                             "comment_form": comment_form})

    return render(request, 'blog/post/detail.html', {'post': post, "comments": comments,
                                                     "new_comment": new_comment})


def post_share(request, post_id):
    """Обработчик страницы отправки поста на Email"""
    post = Post.objects.get(pk=post_id)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) рекомендует вам прочитать "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url,
                                                                    cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@myblog.com', [cd['to']])
            sent = True
        else:
            form = EmailPostForm()
            return render(request, "blog/post/share.html", {"post": post, "form": form, "sent": sent})
    return render(request, "blog/post/share.html", {"post": post, "sent": sent})


def user_register(request):
    """Обработчик страницы регистрации пользователя"""
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрировались")
            return redirect("blog:post_list")
        else:
            messages.error(request, "Ошибка при регистрации")
    else:
        form = UserRegisterForm()
    context = {"form": form}
    return render(request, "blog/post/register.html", context)


def user_authorization(request):
    """Обработчик страницы авторизации пользователя"""
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("blog:post_list")
    else:
        form = UserLoginForm()
    context = {"form": form}
    return render(request, "blog/post/login.html", context)
