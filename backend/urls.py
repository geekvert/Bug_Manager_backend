from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register('projects', ProjectViewSet)
router.register('project_bug', ProjectBugViewSet, 'project_bug')
router.register('my_page', MyPage, 'my_page')
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('bug_images', ImageViewSet, 'bug_images')

urlpatterns = router.urls

urlpatterns += [
    path('oauth/redirect/', Auth),
    path('afterLogin/', AfterLogin),
]
