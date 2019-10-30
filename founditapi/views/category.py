"""View module for handling requests about categories"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from founditapi.models import Category
from founditapi.models import Item
from founditapi.models import Organizer


class CategoryItemSerializer(serializers.HyperlinkedModelSerializer):
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
        fields = ('id', 'name')

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    # Author: Sam Birky
    # Purpose: Allow a user to communicate with the Bangazon database to GET PUT POST and DELETE entries.
    # Methods: GET POST PUT DELETE

    """JSON serializer for categories

    Arguments:
        serializers.HyperlinkedModelSerializer
    """
    class Meta:
        model = Category
        url = serializers.HyperlinkedIdentityField(
            view_name='Category',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'organizer_items')
        depth = 2

class Categories(ViewSet):
    """Categories"""

    def list(self, request):
        """Handle GET requests to categories resource

        Returns:
            Response -- JSON serialized list of categories
        """
        # items = Item.objects.get(user=request.auth.user)
        my_categories = []

        categories = Category.objects.all()
        organizer = Organizer.objects.get(user=request.auth.user)
        for category in categories:
            items = Item.objects.filter(category=category, organizer=organizer)
            json_items = CategoryItemSerializer(items, many=True, context={'request': request})

            category.organizer_items = json_items.data
            serializer = CategorySerializer(
                category,
                many=False,
                context={'request': request}
            )
            my_categories.append(serializer.data)

        # categories = Category.objects.values_list('name','items__name').filter(items__organizer=organizer)
        # print(categories.query.__str__())
        # items = Category.item_set.get(organizer=request.auth.user)
        # categories = categories.filter(items__organizer=organizer)
        # serializer = CategorySerializer(
        #     categories,
        #     many=True,
        #     context={'request': request}
        # )
        return Response(my_categories)

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized Category instance
        """
        category = Category()
        category.name = request.data["name"]
        category.save()

        serializer = CategorySerializer(category, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single category

        Returns:
            Response -- JSON serialized category instance
        """
        try:
            category = Category.objects.get(pk=pk)
            serializer = CategorySerializer(category, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a category

        Returns:
            Response -- Empty body with 204 status code
        """
        category = Category.objects.get(pk=pk)
        category.name = request.data["name"]
        category.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single product type

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            category = Category.objects.get(pk=pk)
            category.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Category.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)