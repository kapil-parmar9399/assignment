"""Box eligibility and cost-based recommendations, independent of HTTP views."""
from dataclasses import dataclass
from decimal import Decimal
from itertools import permutations


@dataclass(frozen=True)
class Recommendation:
    box: object
    total_weight_kg: Decimal


def _dimensions(obj):
    return (obj.length_cm, obj.width_cm, obj.height_cm)


def _orientations(product):
    """Return distinct axis-aligned rotations of a product."""
    return set(permutations(_dimensions(product)))


def _fits_all_items(box, items):
    """Backtrack over axis-aligned placements and reject intersecting items.

    Candidate coordinates are the box origin and the far faces of already
    placed items. This is a practical orthogonal-packing search for small
    order lines; it checks geometry rather than using volume as a proxy.
    """
    bounds = _dimensions(box)
    expanded = []
    for product, quantity in items:
        expanded.extend([product] * quantity)
    expanded.sort(key=lambda product: product.length_cm * product.width_cm * product.height_cm, reverse=True)
    placed = []  # (x, y, z, length, width, height)

    def search(index):
        if index == len(expanded):
            return True
        product = expanded[index]
        xs = {Decimal("0")}
        ys = {Decimal("0")}
        zs = {Decimal("0")}
        for x, y, z, length, width, height in placed:
            xs.add(x + length)
            ys.add(y + width)
            zs.add(z + height)
        for length, width, height in sorted(_orientations(product), reverse=True):
            if length > bounds[0] or width > bounds[1] or height > bounds[2]:
                continue
            for x in sorted(xs):
                for y in sorted(ys):
                    for z in sorted(zs):
                        if x + length > bounds[0] or y + width > bounds[1] or z + height > bounds[2]:
                            continue
                        overlaps = any(
                            x < px + pl and x + length > px
                            and y < py + pw and y + width > py
                            and z < pz + ph and z + height > pz
                            for px, py, pz, pl, pw, ph in placed
                        )
                        if overlaps:
                            continue
                        placed.append((x, y, z, length, width, height))
                        if search(index + 1):
                            return True
                        placed.pop()
        return False

    return search(0)


def recommend_box(order, boxes=None):
    """Return the least-cost available box that fits an order, or None.

    ``order`` may be an Order model instance or an iterable of OrderItem-like
    objects. When boxes is omitted, available database boxes are considered.
    """
    order_items = list(order.items.all()) if hasattr(order, "items") else list(order)
    if not order_items or any(item.quantity < 1 for item in order_items):
        return None
    # Reload products by primary key so an already-cached related Product
    # instance cannot supply an outdated weight or dimensions after an edit.
    from .models import Box, Product

    product_ids = {
        item.product_id if hasattr(item, "product_id") else item.product.pk
        for item in order_items
    }
    products = Product.objects.in_bulk(product_ids)
    if len(products) != len(product_ids):
        return None
    items = [
        (products[item.product_id if hasattr(item, "product_id") else item.product.pk], item.quantity)
        for item in order_items
    ]
    total_weight = sum((product.weight_kg * quantity for product, quantity in items), Decimal("0"))
    if boxes is None:
        boxes = Box.objects.filter(is_available=True)

    eligible = []
    for box in boxes:
        if not getattr(box, "is_available", True):
            continue
        if total_weight <= box.max_weight_kg and _fits_all_items(box, items):
            eligible.append(box)
    if not eligible:
        return None
    selected = min(eligible, key=lambda box: (box.cost, box.length_cm * box.width_cm * box.height_cm, box.name))
    return Recommendation(box=selected, total_weight_kg=total_weight)
