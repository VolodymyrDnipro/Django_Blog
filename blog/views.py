from django.views.generic import ListView, DetailView, FormView
from django.contrib.auth.forms import AuthenticationForm
from django.core.cache import cache
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.views import generic, View
from django import forms
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail

from django.conf import settings

from .models import Post, UserProfile, User, Comment, Notification
from .forms import PostForm, RegisterForm, CommentForm, FeedbackForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        cache_key = "public_posts"
        cached_posts = cache.get(cache_key)

        if cached_posts is not None:
            return cached_posts
        else:
            public_posts_queryset = Post.objects.filter(is_draft=False).order_by('-created_at')
            public_posts = list(public_posts_queryset)
            cache.set(cache_key, public_posts, timeout=300)
            return public_posts


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        comments_count = Comment.objects.filter(post=post, is_published=True).count()
        context['comments_count'] = comments_count
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'is_draft']
    template_name = 'blog/update_post.html'
    login_url = 'blog:login'


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = ''


class LoginRequiredColorMixin(LoginRequiredMixin):
    login_url = '/login/'


class UserDetailView(LoginRequiredMixin, DetailView):
    template_name = 'profile/сurrent_user_profile.html'
    context_object_name = 'user'

    def get_object(self, queryset=None):
        user = self.request.user
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        return {
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'biography': user_profile.bio,
            'profile_picture': user_profile.profile_picture,
        }


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']


class UserUpdateView(LoginRequiredMixin, UpdateView):
    form_class = UserUpdateForm
    second_form_class = UserProfileUpdateForm
    template_name = "profile/update_profile.html"
    success_url = reverse_lazy('blog:profile')
    login_url = reverse_lazy('blog:login')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['user_form'] = self.form_class(self.request.POST, instance=self.object)
            context['profile_form'] = self.second_form_class(self.request.POST, instance=self.object.userprofile)
        else:
            context['user_form'] = self.form_class(instance=self.object)
            context['profile_form'] = self.second_form_class(instance=self.object.userprofile)
        return context

    def form_valid(self, form):
        user_form = self.form_class(self.request.POST, instance=self.object)
        profile_form = self.second_form_class(self.request.POST, instance=self.object.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class RegisterFormView(generic.FormView):
    template_name = "registration/registration.html"
    form_class = RegisterForm
    success_url = reverse_lazy("profile:profile")

    def form_valid(self, form):
        user = form.save()

        user = authenticate(self.request, username=user.username, password=form.cleaned_data.get("password1"))
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class CreatePostView(LoginRequiredMixin, FormView):
    form_class = PostForm
    template_name = 'blog/create_post.html'
    login_url = reverse_lazy('blog:login')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.owner = self.request.user
        post.save()
        return redirect(post.get_absolute_url())


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_post_list.html'
    context_object_name = 'user_posts'
    paginate_by = 6
    login_url = reverse_lazy('blog:login')

    def get_queryset(self):
        cache_key = f"user_posts_{self.request.user.id}"
        cached_posts = cache.get(cache_key)

        if cached_posts is not None:
            return cached_posts
        else:
            user_posts_queryset = Post.objects.filter(owner=self.request.user).order_by('-created_at')
            user_posts = list(user_posts_queryset)
            cache.set(cache_key, user_posts, timeout=300)
            return user_posts


class UserProfileView(DetailView):
    model = User
    template_name = 'profile/user_profile.html'
    context_object_name = 'user_profile'


class CommentListView(ListView):
    model = Comment
    template_name = 'blog/comments.html'
    context_object_name = 'comments'
    paginate_by = 6

    def get_queryset(self):
        post_id = self.kwargs['pk']
        cache_key = f"comments_list_{post_id}"
        cached_comments = cache.get(cache_key)

        if cached_comments is not None:
            return cached_comments
        else:
            comments_queryset = Comment.objects.filter(post_id=post_id, is_published=True)
            comments_list = list(comments_queryset)
            cache.set(cache_key, comments_list, timeout=300)
            return comments_list


class CommentCreateView(FormView):
    template_name = 'blog/create_comment.html'
    form_class = CommentForm

    def form_valid(self, form):
        post_id = self.kwargs['post_id']
        comment = form.save(commit=False)
        comment.post_id = post_id

        if self.request.user.is_authenticated:
            comment.username = self.request.user.username
        else:
            comment.username = 'Anonymous'

        comment.save()
        return redirect('blog:post_detail', post_id)


class FeedbackView(View):
    template_name = 'blog/feedback.html'

    def get(self, request, *args, **kwargs):
        form = FeedbackForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender_email = form.cleaned_data['sender_email']
            admin_email = settings.ADMINS[0][1]  # Assuming the first admin email is used

            send_mail(
                subject,
                message,
                sender_email,
                [admin_email],
                fail_silently=False,
            )

            return redirect('feedback_success')  # Assuming you have a success page

        return render(request, self.template_name, {'form': form})