from . import views
from django.urls import path

app_name = "polls"
urlpatterns = [
       path('admin-login/', views.CustomLoginView.as_view(), name='admin_login'),
    path('logout/', views.custom_logout, name='logout'),
     # ex: /polls/
      # path('admin-login/',views. CustomLoginView.as_view(), name='admin_login'),
    path("", views.index, name="index"), 
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    # path("<int:question_id>/results/", views.results, name="results"),
        path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
  path('create/', views.create_question, name='create'),
    path('update/<int:question_id>/', views.update_question, name='update_question'),
   
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("<int:question_id>/delete/", views.delete, name="delete"),
    #  path('edit/<int:question_id>/', views.create_or_edit_question, name='edit_question'),
]