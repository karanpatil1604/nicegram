from django.urls import path
from .views import SuggestedUserView, UserSearchView, UserSignupView, UserLoginView, UserProfileView, UserProfileEditView


urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='search-user-profile'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('profile/edit/', UserProfileEditView.as_view(), name='edit-user-profile'),
    path('suggested/', SuggestedUserView.as_view(),
         name='suggested-users'),
    path('<str:username>/', UserProfileView.as_view(),
         name='other-user-profile'),

]
