(function($) {
    $(document).ready(function() {

        // recalcular totales al marcar o desmarcar algo como borrado
        $('form input[type=checkbox]').click(function(e) {
            calcular_total();
            calcular_duracion()
        });

        // recalcular totales al borrar un item de un detalle no guardador (con botoncito 'x' )
        $('.inline-deletelink').click(function() {
            calcular_total();
            calcular_duracion()

        });

        // calcular totales al editar campos numericos
        $('.auto').keyup(function(){
            calcular_total();
        });


        // traer datos por ajax
        $('select').change(function(){
            vector = $(this).attr("id").split("-")

            if( (vector[0] == "id_detalleordendetrabajo_set") && (vector[2] =="categoria_servicio") ){

                var optionSelected = $(this).find("option:selected");
                var valueSelected  = optionSelected.val();

                if(!valueSelected){
                    $("#id_detalleordendetrabajo_set-" + vector[1] + "-tela").val(null).trigger('change');
                    $("#id_detalleordendetrabajo_set-" + vector[1] + "-servicio").val(null).trigger('change');
                    $("#id_detalleordendetrabajo_set-" + vector[1] + "-precio").val("");
                    $("#id_detalleordendetrabajo_set-" + vector[1] + "-lista_de_materiales table tbody tr").remove();
                    $("#id_detalleordendetrabajo_set-" + vector[1] + "-duracion").val(0);
                    calcular_total();
                    calcular_duracion();
                    return
                }

                calcular_duracion();

            }

            if( (vector[0] == "id_detalleordendetrabajo_set") && (vector[2] =="servicio") ){

                var optionSelected = $(this).find("option:selected");
                var valueSelected  = optionSelected.val();



                $("#change_id_detalleordendetrabajo_set-"+vector[1]+"-servicio").attr("data-href-template", "/admin/servicios/servicio/add/?_to_field=id&_popup=1&servicioid="+ valueSelected);

                if(!valueSelected){
                    $("#id_detalleordendetrabajo_set-" + vector[1] + "-tela").val(null).trigger('change');
                    $("#id_detalleordendetrabajo_set-" + vector[1] + "-precio").val("");
                    $("#id_detalleordendetrabajo_set-" + vector[1] + "-lista_de_materiales table tbody tr").remove();
                    $("#id_detalleordendetrabajo_set-" + vector[1] + "-duracion").val(0);
                    calcular_total();
                    calcular_duracion();
                    return
                }


                $.ajax({
                    data : {'servicioid' : valueSelected },
                    url : "/admin/servicios/getlistadematerialesdelservicio",
                    type : "get",
                    success : function(data){
                        // alert(JSON.stringify(data))

                        $("#id_detalleordendetrabajo_set-" + vector[1] + "-lista_de_materiales table tbody tr").remove();
                        for (var i = 0; i < data.length; i++) {
                            $("#id_detalleordendetrabajo_set-" + vector[1] + "-lista_de_materiales table tbody").append('<tr><td>'+ data[i].material +'</td><td>'+data[i].cantidad+'</td></tr>');
                        }
                        calcular_total();
                    }
                });

                $.ajax({
                    data : {'servicio_id' : valueSelected },
                    async: false,
                    url : "/admin/servicios/get_duracion_servicio/",
                    type : "get",
                    success : function(data){
                        $('#id_detalleordendetrabajo_set-'+vector[1]+'-duracion').val(data.duracion);
                    }
                });

                calcular_duracion();


            }

            if( (vector[0] == "id_detalleordendetrabajo_set") && (vector[2] =="tela") ){
                var optionSelected = $(this).find("option:selected");
                var valueSelected  = optionSelected.val();

                if(!valueSelected){
                    $("#id_detalleordendetrabajo_set-" + vector[1] + "-precio").val("");
                    calcular_total();
                    return
                }

                servicioid = $("#id_detalleordendetrabajo_set-" + vector[1] + "-servicio").val();

                $.ajax({
                    data : {'telaid' : valueSelected, 'servicioid': servicioid },
                    url : "/admin/servicios/getpreciodelservicio",
                    type : "get",
                    success : function(data){
                        $("#id_detalleordendetrabajo_set-" + vector[1] + "-precio").val(data[0].precio);
                        calcular_total();
                    }
                });
            }
        });


        $("input[name='_continue']").hide()

    });

    function zeroFill( number, width )
    {
        width -= number.toString().length;
        if ( width > 0 )
        {
            return new Array( width + (/\./.test( number ) ? 2 : 1) ).join( '0' ) + number;
        }
        return number + ""; // always return a string
    }

    function formatDate(date) {
        var dia = zeroFill(date.getDate(),2);
        var mes = zeroFill(date.getMonth()+1,2)
        var anho = date.getFullYear()

        return ( dia+ '/' + mes+ '/' + anho)
    }


    function addDays(date, days) {
        var result = new Date(date);
        result.setDate(date.getDate() + days);
        return formatDate(result);

    }

    function get_minutos() {

        var duracion = 0;
        $('input[name*="-duracion"]').not('[name*="__prefix__"]').each(function () {
            var index = this.id.split('-')[1];
            var borrado = false;
            if ($('#id_detalleordendetrabajo_set-'+index+'-DELETE').is(':checked')){
                borrado = true;
            }
            var detalle_id = $('#id_detalleordendetrabajo_set-'+index+'-id').val();
            var valor = parseInt($(this).val()) || 0;
            if(detalle_id){
                $.ajax({
                    data : {'detalle_ot_id' : detalle_id},
                    async : false,
                    url : "/admin/produccion/get_detalle_ot_duracion/",
                    type : "get",
                    success : function(data){
                        // if(parseInt(data.duracion) < parseInt(valor)){
                        //     duracion += valor - parseInt(data.duracion);
                        //     // $('#id_detalleordendetrabajo_set-'+index+'-duracion').val(diff)
                        // }
                        if (borrado){
                            duracion += - parseInt(data.duracion);
                        }else{
                            duracion += valor - parseInt(data.duracion);
                        }
                    }
                });
            }else{
                duracion += valor;
            }
        });
        return duracion;

    }
    function calcular_duracion() {
        var duracion = get_minutos();
        var dias = Math.round((duracion/60)/8);
        var parts =$('#id_fecha_taller').val().split('-');
        var fecha_entrega = new Date(parts[0],parts[1]-1,parts[2]);
        var nueva_fecha = addDays(fecha_entrega,dias);
        $('#id_fecha_de_entrega').val(nueva_fecha.toString())
    }

    /*
     calculo de los totales
     */
    function calcular_total(){

        var total_general = 0;
        var subtotal = 0;
        var extra = 0;
        var descuento = 0;

        var total_forms = $('#id_detalleordendetrabajo_set-TOTAL_FORMS').val();
        for(i=0;i<total_forms;i++){

            var precio = ($('#id_detalleordendetrabajo_set-'+i+'-precio').val()!='')?unformat(document.getElementById('id_detalleordendetrabajo_set-'+i+'-precio')):'0';
            var cantidad = ($('#id_detalleordendetrabajo_set-'+i+'-cantidad').val()!='')?unformat(document.getElementById('id_detalleordendetrabajo_set-'+i+'-cantidad')):'0';

            if($('#id_detalleordendetrabajo_set-'+i+'-DELETE').is(':checked')==false){
                subtotal = parseFloat(subtotal) + parseFloat(precio*cantidad);
            }

        }

        if($('#id_ninos').is(':checked')==true){
            descuento = parseFloat(subtotal)*parseFloat(0.1);
        }

        if($('#id_express').is(':checked')==true){
            extra = parseFloat(extra) + parseFloat(10000);
        }

        if($('#id_con_forro').is(':checked')==true){
            extra = parseFloat(extra) + parseFloat(5000);
        }

        if($('#id_con_pedreria').is(':checked')==true){
            extra = parseFloat(extra) + parseFloat(5000);
        }

        if($('#id_gestion_de_compra').is(':checked')==true){
            extra = parseFloat(extra) + parseFloat(10000);
        }

        var total_general = parseFloat(subtotal) + parseFloat(extra) - parseFloat(descuento)

        $('#id_total').val( parseFloat(total_general).toString().replace(".",",") );
        format(document.getElementById('id_total'));

    }

})(django.jQuery);




