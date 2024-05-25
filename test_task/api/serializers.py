from django.utils.text import slugify
from rest_framework import serializers
from .models import Section, UserSection, ApiUser

class ApiUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiUser
        fields = ["username", "role"]


class UserSectionSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(slug_field='username', queryset=ApiUser.objects.all())
    class Meta:
        model = UserSection
        fields = ["student",
                  "section",
                  "date"]


class StudentSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSection
        fields = ["section", "date"]
        

class NestedUserSectionSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(source="student", slug_field="username", read_only=True)
    class Meta:
        model = UserSection
        fields = ["username", "date"]


class SectionSerializer(serializers.ModelSerializer):
    teacher = serializers.SlugRelatedField(slug_field='username', queryset=ApiUser.objects.all(), required=False)
    students = NestedUserSectionSerializer(many=True, source="usersection_set", required=False)

    class Meta:
        model = Section
        fields = ["title", 
                  "teacher",
                  "students"]

    def validate_title(self, value):

        value = slugify(value)

        section_list = Section.objects.filter(title=value)
        if len(section_list):
            raise serializers.ValidationError(f"There is already section with title {value}")
        return value
    
    def validate_teacher(self, value):
        if value.role != 'TEACHER':
            raise serializers.ValidationError("Teacher must have role TEACHER")
        return value
