from rest_framework import serializers
from .models import PlanesUser, Balance, OpenedItems


class PlanesUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanesUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        # Creating balance for user
        balance = Balance(user=user, balance=0)
        balance.save()
        return user


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = ['balance']
        extra_kwargs = {
            'balance': {
                'read_only': True
            }
        }
