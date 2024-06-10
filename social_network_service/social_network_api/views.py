from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django_ratelimit.decorators import ratelimit
from django.db.models import Q
from .models import FriendRequest
from .serializers import UserSerializer, FriendRequestSerializer

CustomUser = get_user_model()

class UserPagination(PageNumberPagination):
    page_size = 10
    
class SignupView(generics.CreateAPIView):
    """ To handle user signup and returns the user data. """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save(password=self.request.data['password'])

class LoginView(APIView):
    """ To handle Login and return access_token and refresh_token. """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserSearchView(generics.ListAPIView):
    """
       Returns list of user or a specific user based on the search keyword 
       with a paginated result of 10 per/pages.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = UserPagination

    def get_queryset(self):
        keyword = self.request.query_params.get('q', '').strip().lower()
        return CustomUser.objects.filter(
            Q(email__iexact=keyword) | Q(username__icontains=keyword) | Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword)
        )

class SendFriendRequestView(APIView):
    """ View to handle the sending of friend requests with proper validation and rate limiting. """
    
    @ratelimit(key='user', rate='3/m', method='POST', block=True)
    def post(self, request, user_id):
        sender = request.user
        try:
            receiver = CustomUser.objects.get(id=user_id)
        except:
            receiver = None
        
        if receiver:
            if FriendRequest.objects.filter(sender=sender, receiver=receiver).exists():
                return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)
            FriendRequest.objects.create(sender=sender, receiver=receiver)
            return Response({'detail': 'Friend request sent'}, status=status.HTTP_201_CREATED)
        
        return Response({'detail': 'Error sending friend request. Please try after some time!'}, status=status.HTTP_400_BAD_REQUEST)        
class RespondFriendRequestView(APIView):
    """
       Returns and respond to a specific friend request with an
       action i.e accepted or rejected.
    """
    def post(self, request, request_id, action):
        try:
            friend_request = FriendRequest.objects.get(id=request_id)
        except:
            friend_request = None
        
        if friend_request:
            if action == 'accept':
                friend_request.status = 'accepted'
                friend_request.save()
                return Response({'detail': 'Friend request accepted'}, status=status.HTTP_200_OK)
            elif action == 'reject':
                friend_request.delete()
                return Response({'detial': 'Friend request rejected and deleted'}, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'detail': 'No friend request found. Please try after some time!'}, status=status.HTTP_400_BAD_REQUEST)

class FriendListView(generics.ListAPIView):
    """
        Returns a list of all friends(list of users 
        who have accepted friend request) 
    """
    serializer_class = UserSerializer

    def get_queryset(self):
        friends = FriendRequest.objects.filter(
            (Q(sender=self.request.user) | Q(receiver=self.request.user)) & Q(status="accepted")
        ).values_list('sender', 'receiver')
        friend_ids = [friend_id for pair in friends for friend_id in pair if friend_id != self.request.user.id]
        return CustomUser.objects.filter(id__in=friend_ids)

class PendingRequestsView(generics.ListAPIView):
    """
       Returns a list of all pending friend requests(received friend request)
    """
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        return FriendRequest.objects.filter(receiver=self.request.user, status="pending")
