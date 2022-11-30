from rest_framework.routers import DefaultRouter

from user.views import UserView

routers = DefaultRouter()

routers.register("mobile", UserView)

urlpatterns = routers.urls
