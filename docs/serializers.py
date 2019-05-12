from .models import Doc
from rest_framework import serializers

class DocSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Doc
        fields = (
            'id',
            'owner_id',
            'title',
            'file',
            'date',
            'common',
            'signature',
        )
        