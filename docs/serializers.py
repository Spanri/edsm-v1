from .models import Doc
from rest_framework import serializers

class DocSerializer(serializers.HyperlinkedModelSerializer):    
    # notif = serializers.HyperlinkedIdentityField(view_name='notif-list')

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
        