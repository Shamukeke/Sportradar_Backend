from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription publique (compte "personal").
    Ne permet pas de choisir le type, force "personal".
    """
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    preferences = serializers.JSONField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'preferences']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def create(self, validated_data):
        pwd = validated_data.pop('password')
        prefs = validated_data.pop('preferences', {})

        # Création d'un compte "personal" par défaut
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=pwd,
            type='personal'
        )
        user.preferences = prefs
        user.save()
        return user


class BusinessRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer pour l'inscription de comptes entreprise.
    Accessible uniquement aux admins via un endpoint protégé.
    """
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    preferences = serializers.JSONField(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'preferences']
        extra_kwargs = {
            'email': {'required': True},
            'username': {'required': True},
        }

    def create(self, validated_data):
        pwd = validated_data.pop('password')
        prefs = validated_data.pop('preferences', {})

        # Création d'un compte "business"
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=pwd,
            type='business'
        )
        user.preferences = prefs
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer pour exposer les données utilisateur.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'type', 'preferences', 'avatar']
        fields = ['id', 'email', 'username', 'type',
                  'preferences', 'avatar', 'is_staff']
        read_only_fields = ['id', 'email',
                            'username', 'type', 'avatar', 'is_staff']
