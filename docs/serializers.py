from .models import Doc
# from users.serializers import NotifSerializer
from users.models import Notif
from rest_framework import serializers
import datetime

class DocSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Doc
        fields = (
            'id',
            'title',
            'file',
            'size',
            'date',
            'common',
            'preview',
            'description',
            'signature',
        )
    
    def create(self, validated_data):
        now = datetime.datetime.now()
        doc = Doc.objects.create(**validated_data)
        doc.date = now.strftime("%Y-%m-%d")
        doc.save()
        return doc
    
    def update(self, instance, validated_data):
        try:
            return super(DocSerializer, self).update(instance, validated_data)
        except:
            content = {'error': 'Something else went wrong'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
