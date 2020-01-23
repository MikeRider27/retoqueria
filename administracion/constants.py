class TipoFlujoCaja:
    INGRESO = 'IN'
    EGRESO = 'EG'

    TIPOS = (
        (INGRESO, 'Ingreso'),
        (EGRESO, 'Egreso'),
    )


def get_categoria_flujo_venta():
    from administracion.models import CategoriaFlujoCaja
    queryset = CategoriaFlujoCaja.objects.filter(nombre='VENTAS')
    if queryset.exists():
        return queryset.first()
    return CategoriaFlujoCaja.objects.create(
        nombre='VENTAS',
        tipo=TipoFlujoCaja.INGRESO,
        activo=True
    )
