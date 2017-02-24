from django.conf.urls import url, include
from rest_framework import routers

from . import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'roles', views.RoleViewSet)
router.register(r'works', views.WorkViewSet)
router.register(r'workpatterns', views.WorkPatternViewSet)
router.register(r'costcenters', views.CostCenterViewSet)
router.register(r'parttypes', views.PartTypeViewSet)
router.register(r'manufacturers', views.ManufacturerViewSet)
router.register(r'parts', views.PartViewSet)
router.register(r'files', views.FileViewSet)
router.register(r'places', views.PlaceViewSet)
router.register(r'worktypes', views.WorkTypeViewSet)
router.register(r'periods', views.PeriodViewSet)
router.register(r'eventstatuses', views.EventStatusViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'eventreports', views.EventReportViewSet)


#
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/',
        include('rest_framework.urls', namespace='rest_framework')),
    url(r'^$', views.index, name='index')]
