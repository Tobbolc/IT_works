from django.urls import path

from app01 import views

urlpatterns = [
    path('', views.blindbox_index, name='index'),
    path('blindbox/add/', views.blindbox_add, name='blindbox_add'),
    path('blindbox/list/male/', views.blindbox_list_male, name='blindbox_list_male'),
    path('blindbox/list/female/', views.blindbox_list_female, name='blindbox_list_female'),
    path('blindbox/male/', views.blindbox_male, name='blindbox_male'),
    path('blindbox/female/', views.blindbox_female, name='blindbox_female'),
    path('blindbox/<int:nid>/detail/',views.blindbox_detail,name='blindbox_detail'),
    path('blindbox/placed/myself/',views.blindbox_placed_myself,name='blindbox_placed_myself'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('login/email/', views.login_email, name='login_email'),
    path('logout/', views.logout, name='logout'),
    path('image/code/',views.image_code),
    path('email/code/',views.email_code),
    path('random/chose/', views.blindbox_random_chose, name='blindbox_random_chose'),
    path('chosen/myself/', views.blindbox_chosen_myself, name='blindbox_chosen_myself'),
    path('blindbox/comment/delete/', views.blindbox_comment_delete, name='blindbox_comment_delete'),
    path('comment/', views.comment, name='comment'),
    path('personal/data/', views.personal_data, name='personal_data'),

    path('task/list/', views.task_list, name='task_list'),
    path('task/ajax/', views.task_ajax, name='task_ajax'),
    path('task/ajax1/', views.task_ajax1, name='task_ajax1'),

]
