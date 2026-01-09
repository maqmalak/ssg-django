from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.django_dashboard, name='dashboard'),
    path('api/chart/shift/', views.chart_data_by_shift, name='chart_shift'),
    path('api/chart/source/', views.chart_data_by_source, name='chart_source'),
    path('api/chart/production/', views.chart_data_by_production, name='chart_production'),
    path('api/chart/line/', views.chart_data_line, name='chart_line'),
    path('api/chart/line-offloading/', views.chart_data_by_line_offloading, name='chart_line_offloading'),
    path('api/chart/line-loading/', views.chart_data_by_line_loading, name='chart_line_loading'),
    path('api/chart/line-target-summary/', views.chart_data_line_target_summary, name='chart_line_target_summary'),
    path('api/chart/line-wise-targets/', views.chart_data_line_wise_targets, name='chart_line_wise_targets'),
]
