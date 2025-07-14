'''
from rest_framework import serializers
from .models import Plan, Company, Invitation
from django.contrib.auth import get_user_model
User = get_user_model()

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id','name','price','billing_period','features','popular']

class CompanySerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)
    plan_id = serializers.PrimaryKeyRelatedField(queryset=Plan.objects.all(), source='plan', write_only=True)
    class Meta:
        model = Company
        fields = ['id','name','plan','plan_id','created_at']

class InvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitation
        fields = ['id','email','token','created_at','used']

class AcceptInvitationSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            invite = Invitation.objects.get(token=data['token'], used=False)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid or used token.")
        data['invite'] = invite
        return data
    
    def create(self, validated_data):
        invite = validated_data['invite']
        user = User.objects.create_user(
            email=invite.email,
            username=validated_data['username'],
            password=validated_data['password'],
            type='business'
        )
        user.company = invite.company
        user.save()
        invite.used = True
        invite.save()
        return user
'''