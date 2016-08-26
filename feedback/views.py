from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback


@method_decorator(csrf_exempt, name='dispatch')
class FeedbackView(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        if self.request.user.is_authenticated():
            user = self.request.user
        else:
            user = None
        if 'user' in request.data:
            del request.data['user']

        user_agent = request.data.get('user_agent')
        if not user_agent:
            user_agent = request.META.get('HTTP_USER_AGENT', None)

        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, user_agent=user_agent)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
