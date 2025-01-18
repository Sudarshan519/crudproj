from django.utils import timezone
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from polls.models import Choice, Question
from django.http import HttpResponse ,Http404
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic
from django.db.models import F
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
    context = {}

    try:
        question = get_object_or_404(Question, pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    if request.method == 'POST':
        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
                # Redisplay the question voting form.
                return render(
                    request,
                    "polls/detail.html",
                    {
                        "question": question,
                        "error_message": "You didn't select a choice.",
                    },
                )
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()
            return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))
    return render(request, 'polls/vote.html', {"question": question})
def delete(request,question_id):
    context = {}
    question=get_object_or_404(Question, pk=question_id)
    question.delete()
    return HttpResponseRedirect(reverse("polls:index",))
def create(request):
    context = {}
    if request.method == 'POST':
        question_text=request.POST['question']
        choice1=request.POST['option1']
        choice2=request.POST['option2']
        choice3=request.POST['option3']
        choice4=request.POST['option4']

        question=Question(question_text=question_text,pub_date= timezone.now())
        question.save()
        choice=Choice(question= question,choice_text=choice1,votes=0)
        choice.save()
        choice=Choice(question= question,choice_text=choice2,votes=0)
        choice.save()
        choice=Choice(question= question,choice_text=choice3,votes=0)
        choice.save()
        choice=Choice(question= question,choice_text=choice4,votes=0)
        choice.save()
    return render(request, 'polls/create.html', context)