"""
Context processors for productos app.
Provides global template variables.
"""

def cart_and_notifications(request):
    """
    Add cart items count and unread notifications count to all templates.
    """
    context = {}
    
    if request.user.is_authenticated:
        # Cart items count
        try:
            cart = request.user.cart
            context['cart_items_count'] = cart.items.count()
        except Exception:
            context['cart_items_count'] = 0
        
        # Unread notifications count
        context['unread_notifications_count'] = request.user.notifications.filter(is_read=False).count()
    else:
        context['cart_items_count'] = 0
        context['unread_notifications_count'] = 0
    
    return context
