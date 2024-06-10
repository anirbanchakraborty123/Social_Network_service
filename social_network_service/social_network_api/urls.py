from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from .views import SignupView, LoginView, UserSearchView, SendFriendRequestView, RespondFriendRequestView, FriendListView, PendingRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # To get a new access_token using the expired access token by passing the previous refresh_token
    path('search/', UserSearchView.as_view(), name='search-users'),
    path('friend-request/send/<int:user_id>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/<int:request_id>/<str:action>/', RespondFriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', FriendListView.as_view(), name='list-friends'),
    path('friend-requests/pending/', PendingRequestsView.as_view(), name='list-pending-requests'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
