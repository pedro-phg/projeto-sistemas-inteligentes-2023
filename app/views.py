from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from .forms import PostForm
from .models import Post

# Create your views here.

def view(request):
    return render(request, 'app/home.html')

@login_required
def Feed(request):

    posts = Post.objects.order_by('-created_at')

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.translate_text_to_english()
            post.predict_emotion()
            post.translate_text_to_portuguese()
            post.save()
            return redirect('feed')
    else:
        form = PostForm()

    return render(request, 'app/base/base.html', {'form': form, 'posts' : posts})

def search_posts(request):
    query = request.GET.get('q')
    emotion = request.GET.get('emotion')

    posts = Post.objects.all()
    if query and emotion:
        posts = posts.filter(Q(content__icontains=query), emotion=emotion)
    if query:
        posts = posts.filter(Q(content__icontains=query))
    if emotion:
        posts = posts.filter(emotion=emotion)

    context = {
        'query': query,
        'emotion': emotion,
        'posts': posts,
    }
    return render(request, 'app/pages/results.html', context)