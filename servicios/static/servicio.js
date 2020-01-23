(function($) {

	  function addRow(options_prefix){
	        var addButton = $('.add-row');
	        var totalForms = $("#id_" + options_prefix + "-TOTAL_FORMS").prop("autocomplete", "off");
	        var nextIndex = parseInt(totalForms.val(), 10);
	        var maxForms = $("#id_" + options_prefix + "-MAX_NUM_FORMS").prop("autocomplete", "off");
	        var updateElementIndex = function(el, prefix, ndx) {
	            var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
	            var replacement = prefix + "-" + ndx;
	            if ($(el).prop("for")) {
	                $(el).prop("for", $(el).prop("for").replace(id_regex, replacement));
	            }
	            if (el.id) {
	                el.id = el.id.replace(id_regex, replacement);
	            }
	            if (el.name) {
	                el.name = el.name.replace(id_regex, replacement);
	            }
	        };

	        var template = $("#" + options_prefix + "-empty");
	        var row = template.clone(true);
	        row.removeClass("empty-row empty-form")
	                .addClass("dynamic-"+options_prefix)
	                .attr("id", options_prefix + "-" + nextIndex);

	        row.find("*").each(function() {
	            updateElementIndex(this, options_prefix, totalForms.val());
	        });
	        // Insert the new form when it has been fully edited
	        row.insertBefore($(template));
	        // Update number of total forms
	        $(totalForms).val(parseInt(totalForms.val(), 10) + 1);
	        nextIndex += 1;
	    }

    function deleteRow(options_prefix, index) {
        var addButton = $('.add-row');
        var totalForms = $("#id_" + options_prefix + "-TOTAL_FORMS").prop("autocomplete", "off");
        var nextIndex = parseInt(totalForms.val(), 10);
        var maxForms = $("#id_" + options_prefix + "-MAX_NUM_FORMS").prop("autocomplete", "off");
        var updateElementIndex = function(el, prefix, ndx) {
            var id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
            var replacement = prefix + "-" + ndx;
            if ($(el).prop("for")) {
                $(el).prop("for", $(el).prop("for").replace(id_regex, replacement));
            }
            if (el.id) {
                el.id = el.id.replace(id_regex, replacement);
            }
            if (el.name) {
                el.name = el.name.replace(id_regex, replacement);
            }
        };
        // Remove the parent form containing this button:
        $("#" + options_prefix + "-" + index).remove();
        nextIndex -= 1;

        // Update the TOTAL_FORMS form count.
        var forms = $("." + "dynamic-"+options_prefix);
        $("#id_" + options_prefix + "-TOTAL_FORMS").val(forms.length);
        // Show add button again once we drop below max
        if ((maxForms.val() == '') || (maxForms.val()-forms.length) > 0) {
            addButton.parent().show();
        }
        // Also, update names and ids for all remaining form controls
        // so they remain in sequence:
        for (var i=0, formCount=forms.length; i<formCount; i++) {
            updateElementIndex($(forms).get(i), options_prefix, i);
            $(forms.get(i)).find("*").each(function() {
                updateElementIndex(this, options_prefix, i);
            });
        }
        return false;
    }

    $(document).ready(function() {
		init_formsets();
    });

	function init_formsets(){
    	servicio_padre = $("#id_servicio_padre").val()
    	console.log(servicio_padre);
    	if(servicio_padre){

            $.ajax({
                data : {'servicioid': servicio_padre.toString()},
                url : "/admin/servicios/getlistadetelasdelservicio",
                type: "get",
                success : function(data){
                    var totalForms = $("#id_detalledeserviciotela_set-TOTAL_FORMS").val();

                    for(i=0; i<totalForms; i++){
                        deleteRow('detalledeserviciotela_set', 0);
                    }

                    for(i=0; i<data.length; i++){
                        addRow('detalledeserviciotela_set');
                        $('#id_detalledeserviciotela_set-' + i + '-tela').append('<option selected="selected" value="' + data[i].id+'">'+ data[i].tela +'</option>')
                        $("#id_detalledeserviciotela_set-" + i + "-precio").val(data[i].precio);
                    }
                    //calcular_total();
                }
            })

            $.ajax({
                data : {'servicioid': servicio_padre},
                url : "/admin/servicios/getlistadematerialesdelservicio",
                type: "get",
                success : function(data){
                    var totalForms = $("#id_detalledeserviciomaterial_set-TOTAL_FORMS").val();

                    for(i = 0; i<totalForms; i++){
                        deleteRow('detalledeserviciomaterial_set', 0);
                    }

                    for(i=0; i<data.length; i++){
                        addRow('detalledeserviciomaterial_set');
                        $('#id_detalledeserviciomaterial_set-' + i + '-material').append('<option selected="selected" value="' + data[i].id+'">'+data[i].material+'</option>')
                        $("#id_detalledeserviciomaterial_set-" + i + "-cantidad").val(data[i].cantidad);
                    }
                    //calcular_total();
                }
            })
        }

	}


})(django.jQuery);


