from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),

    # Subject with name (important)
    path('subject/<str:name>/', views.subject, name='subject'),

    # Subject list page (optional)
    path('subjects/', views.subject_list, name='subject_list'),

    # 3D view
    path('view-3d/<int:id>/', views.view_3d, name='view_3d'),

    # Email
    path('send-email/', views.send_email, name='send_email'),
]