from rest_framework.routers import DefaultRouter
from user.api.viewsets import GroupsView, PermissionsView, UsersView

router = DefaultRouter()
router.register(r'groups', GroupsView, basename='groups_view')
router.register(r'permissions', PermissionsView, basename='permissions_view')
router.register(r'users', UsersView, basename='users_view')
urlpatterns = router.urls
