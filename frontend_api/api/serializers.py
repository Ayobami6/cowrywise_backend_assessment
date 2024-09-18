from rest_framework import serializers


class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    
