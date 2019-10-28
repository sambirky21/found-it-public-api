"""View module for handling requests about items"""
from django.http import HttpResponseServerError
from django.core.validators import RegexValidator
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from founditapi.models import Item, Category, CategoryItem, Organizer

"""HyperlinkedModelSerializer class
Author: Sam Birky
Purpose:  Allows organizer to communicate with the Found It!
database to GET PUT POST and DELETE by using hyperlinking
between entities. Like the Model Serializer, it implements
create() and update() methods by default.
Methods: GET, PUT, POST, DELETE
"""


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for items
    Arguments:
        serializers.HyperlinkedModelSerializer
    """

    class Meta:
        model = Item
        url = serializers.HyperlinkedIdentityField(
            view_name='item',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'description', 'quantity',
                  'location', 'created_at', 'category', 'organizer')
        depth = 2



class Items(ViewSet):
    """Items for Found It!"""

    def create(self, request):
        """Handle POST operations
        Returns:
            Response -- JSON serialized Item instance
        """
        new_item = Item()

        new_item.name = request.data["name"]
        new_item.organizer = Organizer.objects.get(user=request.auth.user)
        new_item.description = request.data["description"]
        new_item.quantity = request.data["quantity"]
        new_item.created_at = request.data["created_at"]
        new_item.category = Category.objects.get(
            pk=request.data["category"])
        new_item.location = request.data["location"]
        new_item.save()

        serializer = ItemSerializer(
            new_item, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single item
        Returns:
            Response -- JSON serialized item instance
        """
        try:
            single_item = Item.objects.get(pk=pk)
            serializer = ItemSerializer(
                single_item, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an individual item to be edited
        Returns:
            Response -- Empty body with 204 status code
        """
        item = Item.objects.get(pk=pk)
        item.quantity = request.data["quantity"]
        item.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single item
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            item = Item.objects.get(pk=pk)
            item.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Item.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to items resource
        Returns:
            Response -- JSON serialized list of items
        """
        organizer = Organizer.objects.get(user=request.auth.user)
        items = Item.objects.fileter(organizer=organizer)

        serializer = ItemSerializer(
            items, many=True, context={'request': request})

        return Response(serializer.data)
