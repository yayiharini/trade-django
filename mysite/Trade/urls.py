from django.urls import path,include
from django.contrib import admin
from django.conf.urls import url

from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns=[
    path('', views.getcitycounty,name='getcitycounty'),
    path('plu',views.consql,name='plu'),
    path('getwatershed',views.getwatershed,name='getwatershed'),
    path('getwaterboard',views.getwaterboard,name='getwaterboard'),
    path('getplu',views.getplu,name='getplu'),
    path('getrecord',views.getrecords,name='getrecord'),
    path('getPieChartData', views.get_material_group_count, name='get_material_group_count'),
    path('getSubPieChartData', views.get_material_category_data, name='get_material_category_data'),
    path('getBarChartData', views.get_material_group_count, name='get_material_group_count'),
    path('getSubBarChartData', views.get_material_category_data, name='get_material_category_data'),
    path('getLineChartDataByYear', views.get_material_group_yearly_data, name='get_material_group_yearly_data'),
    path('getLineChartDataByQuarter', views.get_material_group_quarterly_data, name='get_material_group_quarterly_data'),
    path('getLineChartDataByMonth', views.get_material_group_monthly_data, name='get_material_group_monthly_data'),
    path('getLineChartDataSemiAnually', views.get_material_group_semianually_data, name='get_material_group_semianually_data'),

    path('getSubLineChartDataByYear', views.get_sub_line_chart_yearly_data, name='get_material_group_yearly_data'),
    path('getSubLineChartDataByQuarter', views.get_sub_line_chart_quarterly_data,name='get_sub_line_chart_quarterly_data'),
    path('getSubLineChartDataByMonth', views.get_sub_line_chart_monthly_data, name='get_sub_line_chart_monthly_data'),
    path('getSubLineChartDataSemiAnually', views.get_sub_line_chart_semianual_data, name='get_sub_line_chart_semianual_data'),

    path('getLitterIndexDataByYear', views.get_litter_index_yearly_data, name='get_litter_index_yearly_data'),
    path('getLitterIndexDataByQuarter', views.get_litter_index_quarterly_data, name='get_litter_index_quarterly_data'),
    path('getLitterIndexDataByMonth', views.get_litter_index_monthly_data, name='get_litter_index_monthly_data'),
    path('getLitterIndexSemiAnnuallyData', views.get_litter_index_semi_annually_data, name='get_litter_index_semi_annually_data'),
    path('permitte',views.getpermitte,name='permittee')
    ]