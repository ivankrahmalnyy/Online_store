from rest_framework import serializers

from store.models import Store, Location, Product
from store.serializers.location_serializers import LocationSerializer
from store.serializers.product_serializers import ProductSerializer


class StoreSerializer(serializers.ModelSerializer):
    # location = LocationSerializer(many=True)
    # product = ProductSerializer(many=True)
    location = serializers.ManyRelatedField(child_relation=LocationSerializer())
    product = serializers.ManyRelatedField(child_relation=ProductSerializer())

    def create(self, validated_data):
        if validated_data['level'] == 0 and validated_data['supplier']:
            raise serializers.ValidationError('Завод не может иметь поставщика')

        location_data = validated_data.pop('location')
        product_data = validated_data.pop('product')

        validated_data['location'] = []
        validated_data['product'] = []

        for location in location_data:
            location_object, _ = Location.objects.get_or_create(**location)
            validated_data['location'].append(location_object.pk)

        for product in product_data:
            product_object, _ = Product.objects.get_or_create(**product)
            validated_data['product'].append(product_object.pk)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data['level'] == 0 and validated_data['supplier']:
            raise serializers.ValidationError('Завод не может иметь поставщика')

        location_data = validated_data.pop('location')
        product_data = validated_data.pop('product')
        validated_data['location'] = []
        validated_data['product'] = []

        for location in location_data:
            location_object, _ = Location.objects.get_or_create(**location)
            validated_data['location'].append(location_object.pk)

        for product in product_data:
            product_object, _ = Product.objects.get_or_create(**product)
            validated_data['product'].append(product_object.pk)

        return super().update(instance, validated_data)

    class Meta:
        model = Store
        fields = '__all__'
        read_only_fields = ['created', 'debt']