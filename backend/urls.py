from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import *

router = SimpleRouter()
router.register('users', UserViewSet) # admin page
router.register('projects', ProjectViewSet) # Homepage
router.register('bugs', BugViewSet) # update delete for project page
router.register('comments', CommentViewSet)
router.register('tags', TagViewSet)

urlpatterns = router.urls
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
urlpatterns += [
    path('project_bug/', ProjectBugViewSet.as_view({'get': 'anon', 'post': 'create'})), # project page
    path('my_page/', MyPage.as_view({'get': 'list'})), # my page
    path('oauth/redirect/', Auth),

    path('zoo/', testing),
    path('test/', testView)
]
