from rest_framework import generics, status

from .models import User
from .serializers import UserSerializer
from rest_framework.response import Response

class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GetUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get(self, request, format=None):
        # print(request.META)
        # return Response(data={
        #     # 'subject': request.user.subject,
        #     'enrollment_class': request.user.enrollment_class,
        #     },
        #     status=status.HTTP_200_OK)
        return Response(data={
            'test': 'test'
        })