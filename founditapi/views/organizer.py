"""View module for handling requests about organizers"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from django.contrib.auth.models import User
from founditapi.models import Organizer

"""HyperlinkedModelSerializer class
Author: Sam Birky
Purpose:  Allows user to communicate with the Bangazon
database to GET PUT POST and DELETE by using hyperlinking
between entities. Like the Model Serializer, it implements
create() and update() methods by default.
Methods: GET, PUT, POST, DELETE
"""

class UserSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)
    """JSON serializer for users

    Arguments:
        serializers.HyperlinkedModelSerializer

    """
    class Meta:
        model = User
        fields = ('id', 'url', 'username', 'first_name',
                  'last_name', 'email', 'date_joined', 'is_active')
        depth = 1

class OrganizerSerializer(serializers.HyperlinkedModelSerializer):

    """JSON serializer for organziers

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
# Meta class is used to define props to associate with the model
# that won't be part of the db. Great way to display related
# properties of a model.
    class Meta:
        model = Organizer
        # HyperlinkedIdentityField is used with HyperlinkedModelSerializer
        # instead of PrimaryKeyIdentityField(used with Model Serializer)
        url = serializers.HyperlinkedIdentityField(
            view_name='organzier',
        )
        fields = ('id', 'url', 'user', 'phone_number')
        # The default ModelSerializer uses primary keys for relationships,
        # but you can also easily generate nested representations using the depth option:
        # It is an integer value that indicates the depth of relationships that should
        # be traversed before reverting to a flat representation.
        depth = 1


class Organizers(ViewSet):
    """Organziers for Found It!"""

    def retrieve(self, request, pk=None):

        """Handle GET requests for single organizer

        Returns:
            Response -- JSON serialized organizer instance
        """
        try:
            organizer = Organizer.objects.get(pk=pk)
            serializer = OrganizerSerializer(organizer, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):

        """Handle PUT requests for a organizer

            Response -- Empty body with 204 status code
        """
        organizer = Organizer.objects.get(pk=pk)
        organizer.user.is_active = False
        organizer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def list(self, request):
        """Handle GET requests to organizers resource

        Returns:
            Response -- JSON serialized list of organizers
        """
        organizers = Organizer.objects.all()
        serializer = OrganizerSerializer(
            organizers,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
