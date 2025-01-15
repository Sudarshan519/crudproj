from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from polls.models import Question
from django.http import HttpResponse ,Http404
from django.shortcuts import get_object_or_404, render
from django.views import generic
def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": latest_question_list}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    try:
        question = get_object_or_404(Question, pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
    # question = get_object_or_404(Question, pk=question_id)
    # return render(request, "polls/detail.html", {"question": question})
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)