from .models import Cart

def get_or_create_cart(request):
    # si el usuario esta autenticado obtenemos el usuario actual
    user = request.user if request.user.is_authenticated else None
    cart_id = request.session.get('cart_id')
    # usamos elmetodo filter que nos da el first() y evitamos detonar la excepcion que da get al no encontrar card_id
    cart = Cart.objects.filter(cart_id=cart_id).first()  # [] -> None
    print(user)
    print(cart_id)

    if cart is None:
        cart = Cart.objects.create(user=user)

    if user and cart.user is None:
        cart.user = user
        cart.save()

    #
    # if cart_id:
    #     cart = Cart.objects.get(cart_id=cart_id)  # obtenemos el carrito
    # else:
    #     # creamos carrito que puede o no pertenecer a un usuario por la validacion atras de user
    #     cart = Cart.objects.create(user=user)

    request.session['cart_id'] = cart.cart_id
    print('valor de id: ', cart.id)
    print('valor de cart_id: ', cart.cart_id)

    return cart