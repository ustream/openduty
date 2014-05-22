__author__ = 'deathowl'

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from openduty.serializers import UserSerializer, GroupSerializer, SchedulePolicySerializer, SchedulePolicyRuleSerializer
from models import SchedulePolicy, SchedulePolicyRule


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class SchedulePolicyViewSet(viewsets.ModelViewSet):
    queryset = SchedulePolicy.objects.all()
    serializer_class = SchedulePolicySerializer

class SchedulePolicyRuleViewSet(viewsets.ModelViewSet):
    queryset = SchedulePolicyRule.objects.all()
    serializer_class = SchedulePolicyRuleSerializer