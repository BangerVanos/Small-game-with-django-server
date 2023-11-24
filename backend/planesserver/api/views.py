from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import PlanesUserSerializer, BalanceSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound, NotAcceptable
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .models import PlanesUser, Balance, OpenedItems


# Create your views here.
class CreateUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PlanesUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class BalanceView(APIView):
    def get(self, request):
        balance: Balance = Balance.objects.filter(user=request.user).first()
        if balance is None:
            raise NotFound('There is no connected balance to this account.')
        return Response({'balance': balance.get_balance})

    def post(self, request):
        balance: Balance = Balance.objects.filter(user=request.user).first()
        if balance is None:
            raise NotFound('There is no connected balance to this account.')
        if request.data.get('action', None) is None:
            raise NotAcceptable('There is no chosen action. Choose \'add\' or \'subtract\'.')
        if request.data.get('value', None) is None:
            raise NotAcceptable('There is no value to add/subtract. Enter one via filling \'value\' in request body')

        # Finally, providing operations with balance
        value = request.data.get('value')
        if request.data.get('action') == 'add':
            try:
                balance.add(value)
            except ValueError as err:
                raise NotAcceptable(err)
        elif request.data.get('action') == 'subtract':
            try:
                balance.subtract(value)
            except ValueError as err:
                raise NotAcceptable(err)
        else:
            raise NotAcceptable('There is no such action. Choose only between \'add\' ans \'subtract\'')
        return Response({'balance': balance.get_balance})


class OpenedItemsView(APIView):
    def get(self, request):
        items = OpenedItems.objects.filter(user=request.user).all()
        if not items.exists():
            return Response({})
        return Response({'unlocked_items': [item.item_id for item in items]})

    def post(self, request):
        if request.data.get('item_id', None) in (None, ''):
            raise NotAcceptable('Please, provide item\'s id by adding \'item_id\' to request\'s body.')
        item = OpenedItems(user=request.user, item_id=request.data.get('item_id'))
        item.save()
        return Response({'item_id': item.item_id})


class UserInfoView(APIView):
    def get(self, request):
        user = PlanesUser.objects.filter(id=request.user.id).first()
        if user is None:
            return Response({})
        return Response({'id': request.user.id, 'username': request.user.username})
