from .models import Doc
# from users.serializers import NotifSerializer
from users.models import Notif
from rest_framework import serializers

class DocSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Doc
        fields = (
            'id',
            'title',
            'file',
            'date',
            'common',
            'preview',
            'description',
            'signature',
        )
