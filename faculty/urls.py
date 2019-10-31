from django.urls import path

from . import views

urlpatterns = [
    path('result_detail', views.result_detail, name='result_detail'),
    path('result_detail/<int:id>', views.result_detail, name='result_detail'),
    path('result_add', views.result_add, name='result_add'),
    # path('result_add/<int:pk>', views.result_add, name='result_add'),
    path('result_load/<int:course_id>', views.result_load, name='result_load'),
    path('all_students/', views.all_students, name='all_students'),

    path('clo_detail', views.clo_detail, name='clo_detail'),
    path('clo_detail/<int:course_id>', views.clo_detail, name='clo_detail'),
    path('clo_add', views.clo_add, name='clo_add'),
    path('clo_add/<int:pk>', views.clo_add, name='clo_add'),
    path('clo_load/<int:course_id>', views.clo_load, name='clo_load'),
    path('<int:clo_id>/clo_delete/', views.clo_delete, name='clo_delete'),

    path('slo_detail', views.slo_detail, name='slo_detail'),
    path('slo_detail/<int:program_id>', views.slo_detail, name='slo_detail'),
    path('slo_add', views.slo_add, name='slo_add'),
    path('slo_add/<int:program_id>', views.slo_add, name='slo_add'),
    path('slo_load/<int:program_id>', views.slo_load, name='slo_load'),
    path('all_slos/', views.all_slos, name='all_slos'),
    path('<int:slo_id>/slo_delete/', views.slo_delete, name='slo_delete'),

    path('plo_detail/', views.plo_detail, name='plo_detail'),
    path('plo_detail/<int:program_id>', views.plo_detail, name='plo_detail'),
    path('plo_add', views.plo_add, name='plo_add'),
    path('plo_add/<int:program_id>', views.plo_add, name='plo_add'),
    path('<int:plo_id>/plo_delete/', views.plo_delete, name='plo_delete'),
    path('validate_plo_code', views.validate_plo_code, name='validate_plo_code'),

    path('outline_detail', views.outline_detail, name='outline_detail'),
    path('outline_detail/<int:pk>', views.outline_detail, name='outline_detail'),
    path('outline_add', views.outline_add, name='outline_add'),
    path('outline_add/<int:pk>', views.outline_add, name='outline_add'),
]
