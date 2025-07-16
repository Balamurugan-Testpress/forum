from django.http import HttpResponse
from django.shortcuts import render
from .models import Board
# Create your views here.


def Home(request):
    boards = Board.objects.all()
    board_names = list()
    for board in boards:
        board_names.append(board.name)
    return render(request, "boards/home.html", context={"boards": boards})
