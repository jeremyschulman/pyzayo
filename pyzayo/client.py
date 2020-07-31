from pyzayo.mtc_mixin import ZayoMatenanceMixin
from pyzayo.svcinv_mixin import ZayoServiceInventoryMixin


__all__ = ["ZayoClient"]


class ZayoClient(ZayoMatenanceMixin, ZayoServiceInventoryMixin):
    """
    Zayo Client class supporting the Maintenance and Sevice-Inventory functional areas.
    """

    pass
