from .models import Doc, FileCabinet
# from users.serializers import NotifSerializer
from users.models import Notif
from rest_framework import serializers
import datetime

class FileCabinetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FileCabinet
        fields = (
            'id',
            'name',
        )

class DocSerializer(serializers.HyperlinkedModelSerializer):
    fileCabinet = FileCabinetSerializer(required=False)
    fileCabinet_id = serializers.IntegerField(write_only=True, required=False)

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
            'fileCabinet',
            'fileCabinet_id',
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
