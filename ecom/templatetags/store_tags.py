
from django import template

register = template.Library()

HUE_COUNT = 6


@register.filter
def money(value):
    """Format a number as a price: 1234.5 -> 'Rs 1,234.50'. Change the prefix to suit."""
    try:
        return f"Rs {float(value):,.2f}"
    except (TypeError, ValueError):
        return value


@register.filter
def hue(category):
    """Map a category (or its id) to a colour slot 1-6 used by the .hue-N CSS classes."""
    pk = getattr(category, "pk", category)
    try:
        return (int(pk) % HUE_COUNT) + 1
    except (TypeError, ValueError):
        return 1


@register.filter
def add_class(field, css):
    """Add a CSS class to a form field widget: {{ field|add_class:"input" }}"""
    existing = field.field.widget.attrs.get("class", "")
    return field.as_widget(attrs={"class": f"{existing} {css}".strip()})


@register.simple_tag(takes_context=True)
def active(context, *url_names):
    """Return 'is-active' when the current URL name matches one of the given names."""
    match = getattr(context["request"], "resolver_match", None)
    if match and (match.view_name in url_names or match.url_name in url_names):
        return "is-active"
    return ""


@register.simple_tag(takes_context=True)
def cart_count(context):
    """Total quantity in the session cart. Expects `cart` in the context (context processor)."""
    cart = context.get("cart")
    if cart is None:
        return 0
    try:
        return sum(item["quantity"] for item in cart)
    except TypeError:
        return len(cart)


@register.filter
def quantity_range(stock, limit=10):
    """Options for a quantity <select>: 1..min(stock, limit)."""
    try:
        top = max(1, min(int(stock), int(limit)))
    except (TypeError, ValueError):
        top = 1
    return range(1, top + 1)


@register.inclusion_tag("partials/product_card.html", takes_context=True)
def product_card(context, product):
    """Render one product card: {% product_card product %}"""
    return {"product": product, "request": context.get("request")}
