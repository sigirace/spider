from rest_framework.serializers import ModelSerializer
from .models import Users


class TinyUserSerializers(ModelSerializer):

    class Meta:
        model = Users
        fields = ["user_id", "name"]
