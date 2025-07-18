from django.contrib.auth.models import User
from django.contrib.auth.views import login_required
from django.shortcuts import get_object_or_404, redirect, render
from boards.forms import NewTopicForm
from .models import Board, Post


def Home(request):
    boards = Board.objects.all()
    board_names = list()
    for board in boards:
        board_names.append(board.name)
    return render(request, "boards/home.html", context={"boards": boards})


def board_topics(request, pk):
    # board = Board.objects.get(pk=pk)
    board = get_object_or_404(Board, pk=pk)
    return render(request, "boards/topics.html", {"board": board})


@login_required
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get("message"),
                topic=topic,
                created_by=request.user,
            )
            return redirect(
                "board_topics", pk=board.pk
            )  # TODO: redirect to the created topic page
    else:
        form = NewTopicForm()
    return render(request, "boards/new_topic.html", {"board": board, "form": form})
