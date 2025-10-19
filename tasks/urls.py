from django.urls import path
from . import views

urlpatterns = [
    path('',views.list_tasks,name="task_list"),
    path('create/',views.create_task,name="create_task"),
    path('update/<int:pk>/',views.update_task,name="update_task"),
    path('delete/<int:pk>/',views.delete_task,name="delete_task"),
    path('signup/',views.signup_view,name="signup"),
    path('login/',views.login_view,name="login"),
    path('delete/',views.logout_view,name="login"),
]
