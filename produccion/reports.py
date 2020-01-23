# -*- coding: utf-8 -*-
from io import BytesIO

import time

from reportlab.pdfgen import canvas
from django.http import HttpResponse

from django.db import connection


def reporte_lista_materiales_ot_pdf(request, datos):

    print(datos)

    def contenido(canvas):
        fecha_actual = time.strftime("%Y/%m/%d")
        hora_actual = time.strftime("%X")

        from reportlab.lib.colors import white, darkblue, black

        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawString(40, 760, "Lista de Materiales en Ordenes de Trabajo")

        canvas.setFillColor(darkblue)
        canvas.setFillColor(black)
        canvas.setStrokeColor(black)
        canvas.setFont("Helvetica", 11)

        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawString(40, 730, "OT Nro")
        canvas.drawString(120, 730, "Prenda")
        canvas.drawString(280, 730, "Material")

        canvas.drawString(388, 730, "Cantidad")
        canvas.drawString(450, 730, "Unid. medida")

        auxhorizontal = 40
        auxvertical = 730
        auxparalasots = 300

        i = 0
        todos = []

        query = "SELECT det_orden.orden_de_trabajo_id, ord_tra.prenda, det_ser.material_id, mat.descripcion, sum(det_ser.cantidad), uni_med.simbolo, uni_med.nombre FROM materiales_unidaddemedida uni_med JOIN materiales_material mat ON uni_med.id=mat.unidad_de_medida_id JOIN produccion_detalleordendetrabajo det_orden ON mat.id=det_ser.material_id  JOIN servicios_detalledeserviciomaterial det_ser ON det_ser.servicio_id=det_orden.servicio_id JOIN  produccion_ordendetrabajo ord_tra  ON ord_tra.id=det_orden.orden_de_trabajo_id where det_orden.orden_de_trabajo_id IN (%s)   group by det_orden. orden_de_trabajo_id, det_ser.material_id;" % ",".join(
            map(str, datos))

        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        print(rows)
        j=0
        aux = []
        for ot in rows:
            print ot
            auxparalasots2 = auxparalasots
            auxvertical = auxvertical - 20
            canvas.setFont("Helvetica", 11)

            if ot[0] not in aux:
                aux.append(ot[0])
                canvas.drawString(auxhorizontal, auxvertical, str(ot[0]))
                canvas.drawString(auxhorizontal+80, auxvertical, str(ot[1]))
            canvas.drawString(auxparalasots-20, auxvertical, str(ot[3]))
            canvas.drawString(auxparalasots2 + 100, auxvertical, str(ot[4]))
            canvas.drawString(auxparalasots2 + 152, auxvertical, str(ot[6]))
            j+=1

        # EL CUADRO DE ABAJO
        # linea vertical de la izquierda
        canvas.line(30, 750, 30, auxvertical - 8)
        # linea vertical de la derecha
        canvas.line(550, 750, 550, auxvertical - 8)
        # tercera linea horizontal (contar de arriba a abajo)
        canvas.line(30, 750, 550, 750)
        # linea de abajo
        canvas.line(30, auxvertical - 8, 550, auxvertical - 8)

        auxvertical = auxvertical - 30
        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawString(auxhorizontal, auxvertical, "Resumen")
        auxvertical = auxvertical - 20
        canvas.drawString(auxhorizontal, auxvertical, "Categoria")
        canvas.drawString(auxhorizontal + 240, auxvertical, "Material")
        canvas.drawString(auxhorizontal + 350, auxvertical, "Cantidad")
        canvas.drawString(auxhorizontal + 410, auxvertical, "Unid. medida")

        query_resumen = "SELECT det_orden.orden_de_trabajo_id, ord_tra.prenda, det_ser.material_id, mat.descripcion, sum(det_ser.cantidad), uni_med.simbolo, uni_med.nombre, cat.nombre FROM materiales_unidaddemedida uni_med JOIN materiales_material mat ON uni_med.id=mat.unidad_de_medida_id JOIN materiales_categoriadematerial cat ON cat.id=mat.categoria_id  JOIN produccion_detalleordendetrabajo det_orden ON mat.id=det_ser.material_id  JOIN servicios_detalledeserviciomaterial det_ser ON det_ser.servicio_id=det_orden.servicio_id JOIN  produccion_ordendetrabajo ord_tra  ON ord_tra.id=det_orden.orden_de_trabajo_id where det_orden.orden_de_trabajo_id IN (%s)   group by cat.nombre, det_ser.material_id;" % ",".join(
            map(str, datos))

        with connection.cursor() as cursor:
            cursor.execute(query_resumen)
            rows = cursor.fetchall()

        print(rows)
        j = 0
        aux = []
        for ot in rows:
            auxparalasots2 = auxparalasots
            auxvertical = auxvertical - 20
            canvas.setFont("Helvetica", 11)

            if ot[7] not in aux:
                aux.append(ot[7])
                canvas.drawString(auxhorizontal, auxvertical, str(ot[7]))
            canvas.drawString(auxparalasots - 20, auxvertical, str(ot[3]))
            canvas.drawString(auxparalasots2 + 100, auxvertical, str(ot[4]))
            canvas.drawString(auxparalasots2 + 152, auxvertical, str(ot[6]))
            j += 1




        # la parte final
        canvas.setFont("Helvetica-Bold", 11)
        auxvertical -= 20
        # canvas.drawString(400, auxvertical, "TOTAL: %s" % separar(total))
        # canvas.drawString(400, auxvertical, "TOTAL: %s" % total)
        canvas.setFont("Helvetica-Bold", 11)
        auxvertical -= 20
        # auxvertical = auxvertical_dos -20
        canvas.drawString(33, auxvertical, "Fecha:")
        canvas.setFont("Helvetica", 11)
        canvas.drawString(73, auxvertical, str(fecha_actual))
        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawString(193, auxvertical, "hora:")
        canvas.setFont("Helvetica", 11)
        canvas.drawString(223, auxvertical, str(hora_actual))
        canvas.setFont("Helvetica-Bold", 11)
        canvas.drawString(383, auxvertical, "Impreso por: ")
        canvas.setFont("Helvetica", 11)
        canvas.drawString(453, auxvertical, str(request.user))

        # canvas.setFont("Helvetica-Bold", 18)
        # canvas.drawInlineImage(BASE_DIR + "/static/img/logo.jpg", 30, 760, 160, 60)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="lista_materiales_ot.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)
    contenido(p)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
