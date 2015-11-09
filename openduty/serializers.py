__author__ = 'deathowl'

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Incident, SchedulePolicy, SchedulePolicyRule


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class IncidentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Incident
        fields = ('incident_key', 'service_key', 'event_type', 'description', 'details')


class SchedulePolicySerializer(serializers.HyperlinkedModelSerializer):
    rules = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = SchedulePolicy
        fields = ('name', 'repeat_times', 'rules')


class SchedulePolicyRuleSerializer(serializers.HyperlinkedModelSerializer):
    rules = serializers.RelatedField(many=True, read_only=True)

    class Meta:
        model = SchedulePolicyRule
        fields = ('schedule_policy', 'position', 'user_id', 'schedule', 'escalate_after')


class NoneSerializer(serializers.Serializer):
    class Meta:
        fields = ()


class OpsWeeklySerializer(serializers.Serializer):
    occurred_at = serializers.DateTimeField()
    output = serializers.CharField(max_length=2000)
    incindent_key = serializers.CharField(max_length=200)

class OnCallSerializer(serializers.Serializer):
    person = serializers.CharField()
    email = serializers.EmailField()
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()

