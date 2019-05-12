from .models import Doc
from rest_framework import serializers

class DocSerializer(serializers.HyperlinkedModelSerializer):    
    class Meta:
        model = Doc
        fields = (
            'id',
            'title',
            'owner', 
            'file',
            'date',
            'signature',
        )
        extra_kwargs = {
            'owner': {'lookup_field': 'email'}
        }
        