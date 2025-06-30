from rest_framework import serializers
from .models import Contact, Product, NetworkNode


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class NetworkNodeSerializer(serializers.ModelSerializer):
    contact = ContactSerializer()
    products = ProductSerializer(many=True)
    supplier = serializers.SlugRelatedField(
        slug_field='name',
        queryset=NetworkNode.objects.all(),
        required=False,
        allow_null=True
    )
    hierarchy_level = serializers.IntegerField(read_only=True)

    class Meta:
        model = NetworkNode
        fields = '__all__'
        read_only_fields = ('debt', 'created_at', 'hierarchy_level')

    def create(self, validated_data):
        contact_data = validated_data.pop('contact')
        products_data = validated_data.pop('products')

        contact = Contact.objects.create(**contact_data)
        network_node = NetworkNode.objects.create(contact=contact, **validated_data)

        for product_data in products_data:
            product, _ = Product.objects.get_or_create(**product_data)
            network_node.products.add(product)

        return network_node

    def update(self, instance, validated_data):
        # Запрещаем обновление поля debt через API
        if 'debt' in validated_data:
            del validated_data['debt']

        contact_data = validated_data.pop('contact', None)
        products_data = validated_data.pop('products', None)

        # Обновляем контактные данные
        if contact_data:
            contact_serializer = ContactSerializer(
                instance.contact,
                data=contact_data,
                partial=True
            )
            contact_serializer.is_valid(raise_exception=True)
            contact_serializer.save()

        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        # Обновляем продукты
        if products_data is not None:
            instance.products.clear()
            for product_data in products_data:
                product, _ = Product.objects.get_or_create(**product_data)
                instance.products.add(product)

        instance.save()
        return instance


class NetworkNodeListSerializer(serializers.ModelSerializer):
    supplier = serializers.StringRelatedField()
    hierarchy_level = serializers.IntegerField()
    contact = serializers.StringRelatedField()

    class Meta:
        model = NetworkNode
        fields = (
            'id',
            'name',
            'node_type',
            'hierarchy_level',
            'supplier',
            'contact',
            'debt',
            'created_at'
        )
