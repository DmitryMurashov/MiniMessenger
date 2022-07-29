from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from authapp.serializers import RegisterSerializer, LoginSerivalizer, ProfileSerializer
from rest_framework.views import Response, status
from rest_framework.generics import RetrieveUpdateAPIView


class RegisterApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginApiView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerivalizer

    def post(self, request):
        user_data = request.data.get('user', {})
        serializer = self.serializer_class(data=user_data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class ProfileApiView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user.profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('profile', {})

        serializer = self.serializer_class(request.user.profile, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
