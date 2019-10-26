"""View module for handling requests about items"""
from django.http import HttpResponseServerError
from django.core.validators import RegexValidator
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from founditapi.models import Item, Category, CategoryItem
from django.contrib.auth.models import User

"""HyperlinkedModelSerializer class
Author: Sam Birky
Purpose:  Allows user to communicate with the Found It!
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
                  'location', 'created_at', 'category')
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
        new_item.user = request.data["user"]
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
        items = Item.objects.all()
        item_list = list()

        serializer = ItemSerializer(
            items, many=True, context={'request': request})

        return Response(serializer.data)

        # support filtering by category
        # category = self.request.query_params.get('category', None)
        # if category is not None:
        #     items = items.filter(category_item_id=category)
        #     for item in items:
        #         if item.quantity > 0:
        #             item_list.append(item)
        #     items = item_list

        # support filtering by quantity
        # quantity = self.request.query_params.get('quantity', None)
        # if quantity is not None:
        #     quantity = int(quantity)
        #     length = len(products)
        #     new_products = list()
        #     count = 0
        #     for product in products:
        #         count += 1
        #         if count - 1 + quantity >= length:
        #             new_products.append(product)
        #             if count == length:
        #                 products = new_products
        #                 break

        # location = self.request.query_params.get('location', None)
        # if location is not None:
        #     products = products.filter(location=location)
        #     for product in products:
        #         if product.quantity > 0:
        #             product_list.append(product)
        #     products = product_list

        # aproduct = list(products)[0]

        # serializer = ProductSerializer(
        #     products, many=True, context={'request': request})

        # return Response(serializer.data)

    # Custom Action that supports filtering products by customer by creating a new route
    # @action(methods=['get'], detail=False)
    # def myproduct(self, request):

    #     try:
    #         customer = Customer.objects.get(user=request.auth.user)
    #         products_of_customer = Product.objects.filter(customer=customer)
    #     except Product.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    #     serializer = ProductSerializer(products_of_customer, many=True, context={'request': request})
    #     return Response(serializer.data)
