from .models import Doc
# from users.serializers import NotifSerializer
from rest_framework import serializers

class DocSerializer(serializers.HyperlinkedModelSerializer):    
    # notif = serializers.HyperlinkedIdentityField(view_name='notif-list')
    # notif = NotifSerializer(required=False)

    class Meta:
        model = Doc
        fields = (
            'id',
            # 'owner_id',
            'title',
            'file',
            'date',
            'common',
            'signature',
            # 'notif',
        )
        
