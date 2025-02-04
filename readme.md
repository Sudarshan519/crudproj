# Django tutorial

## mkdir djangotutorial
```bash
 django-admin startproject mysite djangotutorial
```


## Development Server
```bash
python manage.py runserver
```

## Create Polls app
```bash
python manage.py startapp polls
```


## Create Superuser
```bash 
python manage.py createsuperuser
```
## Register app
```python 
INSTALLED_APPS = [
    "polls.apps.PollsConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
```
# Update models
```python
# models.py

from django.db import models
import datetime
from django.utils import timezone
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published",auto_now_add=True)
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.question.question_text + " = "+self.choice_text
```
## Run Migrations
```python 
python manage.py migrate
python manage.py makemigrations polls
```

## Run Shells
```bash 
python manage.py shell
```

```python
>>> from polls.models import Choice, Question  # Import the model classes we just wrote.

# No questions are in the system yet.
>>> Question.objects.all()
<QuerySet []>

# Create a new Question.
# Support for time zones is enabled in the default settings file, so
# Django expects a datetime with tzinfo for pub_date. Use timezone.now()
# instead of datetime.datetime.now() and it will do the right thing.
>>> from django.utils import timezone
>>> q = Question(question_text="What's new?", pub_date=timezone.now())

# Save the object into the database. You have to call save() explicitly.
>>> q.save()

# Now it has an ID.
>>> q.id
1

# Access model field values via Python attributes.
>>> q.question_text
"What's new?"
>>> q.pub_date
datetime.datetime(2012, 2, 26, 13, 0, 0, 775217, tzinfo=datetime.timezone.utc)

# Change values by changing the attributes, then calling save().
>>> q.question_text = "What's up?"
>>> q.save()

# objects.all() displays all the questions in the database.
>>> Question.objects.all()
<QuerySet [<Question: Question object (1)>]>
```
## polls/admin.py
```python 
from django.contrib import admin

from .models import Question

admin.site.register(Question)
```

## polls/views.py
```python
from django.http import HttpResponse

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

## polls/urls.py
```python 
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
]
```

## polls/views.py
```python 
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

# Leave the rest of the views (detail, results, vote) unchanged
```

## polls/templates/polls/index.html
```html
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

## polls/views.py
```python
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))
```

## polls/views.py
```python
from django.http import Http404
from django.shortcuts import render

from .models import Question


# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
```

## polls/views.py
```python
from django.shortcuts import get_object_or_404, render

from .models import Question


# ...
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})
```
## polls/templates/detail.html
```html
<h1>{{ question.question_text }}</h1>
<ul>
{% for choice in question.choice_set.all %}
    <li>{{ choice.choice_text }}</li>
{% endfor %}
</ul>
```



# Update Detail.html page
```html
<!-- vote.html -->
{% extends "polls/base.html" %}

{% block title %}Vote{% endblock %}

{% block main %}
<form action="{% url 'polls:vote' question.id %}" method="post">
    {% csrf_token %}
    <fieldset>
        <legend><h1>{{ question.question_text }}</h1></legend>
        {% if error_message %}<p><strong>{{ error_message }}</strong></p>{% endif %}
        <ul class="list-group"></ul>
        {% for choice in question.choice_set.all %}

            <input type="radio" name="choice" id="choice{{ forloop.counter }}" value="{{ choice.id }}">
            <label for="choice{{ forloop.counter }}">{{ choice.choice_text }}</label><br>
        {% endfor %}
    </fieldset>
    <br>
    <input type="submit" class="btn btn-primary" value="Vote">
    </form>

    {% endblock %}
```


# Template inheritance base.html
```html
<!-- base.html -->
{% load static %}

<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta http-equiv="content-type" content="text/html; charset=UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{% block title %}{% endblock %}</title>

        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        <link rel="stylesheet" type="text/css" href="{% static 'style.css' %}" />

    </head>
    <body>
        <nav class="navbar navbar-default" role="navigation">
            <div class="container">
                <!-- Brand and toggle get grouped for better mobile display -->
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-ex1-collapse">
                        <span class="sr-only">Toggle navigation</span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                    </button>
                    <a class="navbar-brand" href="{% url 'polls:index' %}">Poll Application</a>
                </div>

                <!-- Collect the nav links, forms, and other content for toggling -->
                <div class="collapse navbar-collapse navbar-ex1-collapse">
                    <ul class="nav navbar-nav">
                        <li class="{% block home %}{% endblock %}"><a href="{% url 'polls:index' %}" >Home</a></li>
                        <li class="{% block create %}{% endblock %}"><a href="{% url 'polls:create' %}">Create</a></li>

                    
                        
            
                    </ul>
                    
                </div><!-- /.navbar-collapse -->
            </div>
        </nav>

        <div class="container">
            {% block main %}{% endblock %}
        </div>

    </body>
</html>
```


# Update Views.py for vote
```python
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

```

# for urls.py for vote
 
```python
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
```        
# results function

```python
def results(request,pk):
    question = get_object_or_404(Question, pk=question_id)
    return render('polls/results.html',{'question':queston})
```

# or
```python
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
```


# urls.py for  

# Using Forms
```python 
# forms.py
from django import forms
from .models import Question, Choice

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
```

# style.css

```
For the style.css, we need to put it in a directory directory. It can be put it in a directory called poll/static.

/* style.css */
.navbar-default, .btn, .form-control, .panel {
    border-radius: 0;
}
.navbar-default {
    /* background-color: rgba(245, 245, 220, .7); */
    /* border-color: rgba(245, 245, 220, .6); */
    /* box-shadow: 0px 3px 3px 0px #ddd; */
}
.navbar-default .navbar-nav>.active>a, 
.navbar-default .navbar-nav>.active>a:focus, 
.navbar-default .navbar-nav>.active>a:hover {
    /* background-color: rgba(245, 245, 220, .9); */
    /* border-bottom: 4px solid #ddd; */
}
.panel-default > .panel-heading {
    color: #333;
    /* background-color: rgba(245, 245, 220, .7); */
    /* border-color: rgba(245, 245, 220, .6); */
    border-top-left-radius: 0;
    border-top-right-radius: 0; 
}
.panel-footer {
    /* background-color: rgba(245, 245, 220, .5); */
    /* border-color: rgba(245, 245, 220, .4); */
}
.panel {
    box-shadow: 0px 3px 3px 0px #ddd;
}
a.navbar-brand, .panel-title {
    font-weight: bolder;
}
```

# create
```
def create_question(request):
    # if request.method == 'POST':
    #     # Creating a new Question form
    #     question_form = QuestionForm(request.POST)

    #     # Handle choices (assuming 4 choices)
    #     choice_forms = []
    #     for i in range(1, 5):
    #         choice_form = ChoiceForm(request.POST, prefix=f'choice{i}')
    #         choice_forms.append(choice_form)

    #     if question_form.is_valid() and all(form.is_valid() for form in choice_forms):
    #         # Save the question first (this will assign a primary key)
    #         question = question_form.save()

    #         # Save each choice form and associate it with the created question
    #         for form in choice_forms:
    #             form.instance.question = question  # Associate the choice with the saved question
    #             form.save()

    #         # Redirect to another page after creation, e.g., question list or detail
    #         return redirect('polls:index')

    # else:
        # Initialize empty forms for GET request
    question_form = QuestionForm()
    choice_forms = [ChoiceForm(prefix=f'choice{i}') for i in range(1, 5)]

    return render(request, 'polls/create.html', {
        'question_form': question_form,
        'choice_forms': choice_forms
    })

```


# create.html
```
{% extends "polls/base.html" %}

{% block create %} active
 {% endblock %}

{% block title %}Create a New Question{% endblock %}

{% block main %}
<div class="row">
    <div class="col-lg-8 col-lg-offset-2">
        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">Create a New Question</h3>
            </div>
            <form method="POST">
                {% csrf_token %}
                <div class="panel-body">
                    <div class="form-group">
                        <label for="question_text">Question</label>
                        {{ question_form.as_p }}
                    </div>

                    <div class="form-group">
                        <label for="choices">Choices</label>
                        <div id="choices">
                            {% for form in choice_forms %}
                                <div class="form-group">
                                    {{ form.as_p }}
                                </div>
                            {% endfor %}
                        </div>
                    </div>

                    <div class="row">
                        <hr />
                        <div class="col-lg-4">
                            <button type="submit" class="btn btn-info">Create Question</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}
```

# polls/urls.py
```python 

  path('create/', views.create_question, name='create'),
```


# update
# View for updating an existing question
```python
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

    return render(request, 'polls/create.html', {
        'question_form': question_form,
        'choice_forms': choice_forms,
        'question': question
    })
```

# polls/urls.py
```python 

      path('update/<int:question_id>/', views.update_question, name='update_question'),
   
```

