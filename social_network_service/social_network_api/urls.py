from django.urls import path
from .views import SignupView, LoginView, UserSearchView, SendFriendRequestView, RespondFriendRequestView, FriendListView, PendingRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='search-users'),
    path('friend-request/send/<int:user_id>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/<int:request_id>/<str:action>/', RespondFriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', FriendListView.as_view(), name='list-friends'),
    path('friend-requests/pending/', PendingRequestsView.as_view(), name='list-pending-requests'),
]
