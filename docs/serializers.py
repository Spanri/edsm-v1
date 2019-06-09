from .models import Doc, FileCabinet
# from users.serializers import NotifSerializer
from users.models import Notif
from rest_framework import serializers
import datetime
from django.utils import timezone

class FileCabinetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileCabinet
        fields = (
            'id',
            'name',
        )

class DocSerializer(serializers.HyperlinkedModelSerializer):
    file_cabinet = FileCabinetSerializer(required=False)
    file_cabinet_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Doc
        fields = (
            'id',
            'title',
            'file',
            'size',
            'date',
            'common',
            'description',
            'signature',
            'signature_end',
            'cancel_description',
            'cancel_file',
            'file_cabinet',
            'file_cabinet_id',
        )
    
    def create(self, validated_data):
        now = timezone.now()
        doc = Doc.objects.create(**validated_data)
        doc.date = now
        doc.save()
        return doc
    
    def update(self, instance, validated_data):
        try:
            return super(DocSerializer, self).update(instance, validated_data)
        except Exception as e:
            print(str(e))
            content = {'error': 'Something else went wrong'}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
