from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import *

from .serializers import *
from .models import Section, UserSection
from .permissions import IsStudentPermission, IsTeacherPermission, IsModeratorPermission


class ListCreateSectionsAPIView(ListCreateAPIView):

    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'teacher']
    ordering_fields = ['title', 'teacher']
    search_fields = ['title']

    def get_permissions(self):
        self.permission_classes = [IsAuthenticatedOrReadOnly] if self.request.method == 'GET' else [IsTeacherPermission|IsModeratorPermission]
        return super().get_permissions()

list_create_sections_view = ListCreateSectionsAPIView.as_view()


class RUDSectionsAPIView(RetrieveUpdateDestroyAPIView):

    serializer_class = SectionSerializer
    queryset = Section.objects.all()
    lookup_field = "title"

    def get_permissions(self):
        self.permission_classes = [IsModeratorPermission] if self.request.method in ['DELETE', 'PUT', 'PATCH'] else [IsAuthenticatedOrReadOnly]
        return super().get_permissions()
    
rud_sections_view = RUDSectionsAPIView.as_view()


class ListCreateUserSectionAPIView(ListCreateAPIView):
    permission_classes = [IsStudentPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['section', 'date']
    ordering_fields = ['section', 'date']
    search_fields = ['section__title']

    def get_queryset(self):
        return UserSection.objects.filter(student=self.request.user)


    def get_serializer(self, *args, **kwargs):
        self.serializer_class = StudentSectionSerializer if self.request.method == 'GET' else UserSectionSerializer
        return super().get_serializer(*args, **kwargs)


    def create(self, request, *args, **kwargs):

        section = request.data.get("section")
        student = request.user

        serializer_data = {"student": student, "section": section}

        serializer = self.get_serializer(data=serializer_data)
        serializer.is_valid(raise_exception=True)

        student = serializer.validated_data["student"]
        section = serializer.validated_data["section"]

        userSection_list = UserSection.objects.filter(student=student, section=section)

        if len(userSection_list):

            data = {"detail": f"You have already joined section {section}"}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

list_create_usersection_view = ListCreateUserSectionAPIView.as_view()


class RetrieveDestroyUserSectionAPIView(RetrieveDestroyAPIView):
    permission_classes = [IsStudentPermission]
    serializer_class = StudentSectionSerializer
    lookup_field = "section"

    def get_queryset(self):
        return UserSection.objects.filter(student=self.request.user)

rd_usersection_view = RetrieveDestroyUserSectionAPIView.as_view()