from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.bb
from polls.models import Choice, Question
from django.http import HttpResponse ,Http404,HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import F

from django.contrib.auth.views import LoginView

# Custom login view using the built-in LoginView
class CustomLoginView(LoginView):
    template_name = 'polls/admin_login.html'
    def get_redirect_url(self):
        # Provide the absolute URL you want to redirect to after logout
        return self.request.scheme + "://" + self.request.get_host() + reverse('polls:create') # Redirect to an absolute UR

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
# Custom check function for admin-like users (superusers or staff members)
from django.contrib.auth.decorators import login_required, user_passes_test
def is_admin_user(user):
    return user.is_staff or user.is_superuser
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout,login
@login_required  # Ensure only logged-in users can access the logout functionality
def custom_logout(request):
    logout(request)  # Log the user out
    return redirect('polls:admin_login')  # Redirect to the login page after logout
# Admin Login View (Custom login)
def admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = form.get_user()
            # Log the user in
            login(request, user)
            return redirect('polls:question_list')  # Redirect to a page after login, e.g., question list
    else:
        form = AuthenticationForm()

    return render(request, 'polls/admin_login.html', {'form': form})

@login_required
@user_passes_test(is_admin_user)
def delete(request,question_id):
    context = {}
    question=get_object_or_404(Question, pk=question_id)
    question.delete()
    return HttpResponseRedirect(reverse("polls:index",))

from .forms import QuestionForm, ChoiceForm  # Assuming you have forms for validation

# View for creating a new question
@login_required
def create_question(request):
    if request.method == 'POST':
        # Creating a new Question form
        question_form = QuestionForm(request.POST)

        # Handle choices (assuming 4 choices)
        choice_forms = []
        for i in range(1, 5):
            choice_form = ChoiceForm(request.POST, prefix=f'choice{i}')
            choice_forms.append(choice_form)

        if question_form.is_valid() and all(form.is_valid() for form in choice_forms):
            # Save the question first (this will assign a primary key)
            question = question_form.save()

            # Save each choice form and associate it with the created question
            for form in choice_forms:
                form.instance.question = question  # Associate the choice with the saved question
                form.save()

            # Redirect to another page after creation, e.g., question list or detail
            return redirect('polls:index')

    else:
        # Initialize empty forms for GET request
        question_form = QuestionForm()
        choice_forms = [ChoiceForm(prefix=f'choice{i}') for i in range(1, 5)]

    return render(request, 'polls/create.html', {
        'question_form': question_form,
        'choice_forms': choice_forms
    })


# View for updating an existing question
def update_question(request, question_id):
    question = get_object_or_404(Question, id=question_id)

    if request.method == 'POST':
        # Populate the form with the existing question data
        question_form = QuestionForm(request.POST, instance=question)

        # Handle choices (assuming 4 choices)
        choice_forms = []
        for i in range(1, 5):
            choice_instance = question.choice_set.all()[i-1] if i <= len(question.choice_set.all()) else None
            choice_form = ChoiceForm(request.POST, prefix=f'choice{i}', instance=choice_instance)
            choice_forms.append(choice_form)

        if question_form.is_valid() and all(form.is_valid() for form in choice_forms):
            # Save the question (this will update the existing question)
            question = question_form.save()

            # Save each choice form, associating them with the updated question
            for form in choice_forms:
                form.save()

            # Redirect to another page after updating, e.g., question list or detail page
            return redirect('polls:question_list')

    else:
        # Handle GET request - initialize forms with existing data
        question_form = QuestionForm(instance=question)
        choice_forms = [ChoiceForm(prefix=f'choice{i}', instance=question.choice_set.all()[i-1] if i <= len(question.choice_set.all()) else None) for i in range(1, 5)]

    return render(request, 'polls/update_question.html', {
        'question_form': question_form,
        'choice_forms': choice_forms,
        'question': question
    })