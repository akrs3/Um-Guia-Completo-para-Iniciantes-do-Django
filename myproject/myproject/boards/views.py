from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.db.models import Count

from .models import Board, Topic, Post
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required

#from django.views.generic import View
#from django.views.generic import CreateView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.utils import timezone
from django.utils.decorators import method_decorator

def home(request):
    boards = Board.objects.all()
    return render (request, 'home.html', {'boards': boards})

    
# Create your views here.

def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    return render(request, 'topics.html', {'board': board, 'topics': topics})

    
@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    #user = User.objects.first()  # TODO: get the currently logged in user
    
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                created_by=request.user
            )
            return redirect('topic_posts', pk=pk, topic_pk=topic.pk)  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

#view de relacao entre o Board e os Topicos correspondentes
def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    topic.views += 1
    topic.save()
    return render(request, 'topic_posts.html', {'topic': topic})


@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

#view baseada em funcao -- esta cria novo post
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'new_post.html', {'form': form})

#classe baseada em view - tbm cria novo post
'''class NewPostView(View):
    def render(self, request):
        return render(request, 'new_post.html', {'form': self.form})

    def post(self, request):
        self.form = PostForm(request.POST)
        if self.form.is_valid():
            self.form.save()
            return redirect('post_list')
        return self.render(request)

    def get(self, request):
        self.form = PostForm()
        return self.render(request)'''

#GCBV - view generica baseada em classe - tbm cria novo post
'''
class NewPostView(CreateView):
    model = Post
    form_class = PostForm
    success_url = reverse_lazy('post_list')
    template_name = 'new_post.html'
'''



#decorator que exige a autenticacao do ususario em views baseadas em classe
#dispatch e um metodo interno do Django, por onde passa tds os pedidos
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView): #GCBV - para editar um post
    model = Post
    fields = ('message', ) #usado p criar um formulario modelo on-the-fly
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk' # usado p identificar o nome do argumento da palavra-chave p recuperar o objeto Post.
    #é o mesmo q definimos
    context_object_name = 'post' #renomeia o 'object' Post para ser chamado de 'post' 

    def get_queryset(self):
        queryset = super().get_queryset() #reusa o get_query_set da classe UpdateView
        return queryset.filter(created_by=self.request.user) #adiciona filtro extra, p pegar so do usuario conectado

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_at = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.board.pk, topic_pk=post.topic.pk)


#simulando a view def home() com GCBV
class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'