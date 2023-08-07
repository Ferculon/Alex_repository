from django.contrib.auth.models import Group
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView

from myapiapp.serializers import GroupSerializer


@api_view()
def hello_world_view(request: Request) -> Response:
    return Response({
        'message': 'Hello, World!',
    })


# реализация через ListCreateAPIView
class GroupsListView(ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# # реализация через GenericAPIView и ListModelMixin (возвращает список объектов)
# class GroupsListView(ListModelMixin, GenericAPIView):
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer
#
#     def get(self, request: Request) -> Response:
#         return self.list(request)


# # реализация через сериализатор
# class GroupsListView(APIView):
#     def get(self, request: Request) -> Response:
#         groups = Group.objects.all()
#         serialized = GroupSerializer(groups, many=True)   # many - указатель, что передается список объектов
#         return Response({
#             'groups': serialized.data,
#         })


# class GroupsListView(APIView):
#     def get(self, request: Request) -> Response:
#         groups = Group.objects.all()
#         data = [group.name for group in groups]
#         return Response({
#             'groups': data,
#         })
