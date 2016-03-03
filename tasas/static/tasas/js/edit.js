'use strict'

var select_tipo_tasa = document.getElementsByClassName("tipo-tasa-selector");

var PRECIO_POR_CREDITO = 0;
var PAGO_UNICO = 1;
var MISCELANEO = 2;

var classes_tipo_tasa = {};
classes_tipo_tasa[PRECIO_POR_CREDITO] = "porcredito";
classes_tipo_tasa[PAGO_UNICO] = "global";
classes_tipo_tasa[MISCELANEO] = "miscelaneo";

var initialize = function(){
    Array.prototype.forEach.call(select_tipo_tasa, function(element){
        var tasas_div = element.parentNode.parentNode.getElementsByClassName('tasas-data')[0];
        var selector = element;

		if(selector.options[selector.selectedIndex].value === ""){
			Array.prototype.forEach.call(tasas_div.querySelectorAll('.tipo-tasa'), function (element) {
				element.style.display = "none";
			}, false);
		}
		else
		{
			var classForSelected = classes_tipo_tasa[parseInt(selector.options[selector.selectedIndex].value, 10)];
			Array.prototype.forEach.call(tasas_div.querySelectorAll('.tipo-tasa'), function (element) {
				if (element.className.split(' ').indexOf(classForSelected) > -1)
					element.style.display = "inherit";
				else
					element.style.display = "none";
			}, false);
		}

        element.addEventListener('change', function(e){
            var tasas_div = this.parentNode.parentNode.getElementsByClassName('tasas-data')[0];
            var selector = this;

            if(selector.options[selector.selectedIndex].value === ""){
                Array.prototype.forEach.call(tasas_div.querySelectorAll('.tipo-tasa'), function (element) {
                    element.style.display = "none";
                }, false);
            }
            else
            {
                var classForSelected = classes_tipo_tasa[parseInt(selector.options[selector.selectedIndex].value, 10)];
                Array.prototype.forEach.call(tasas_div.querySelectorAll('.tipo-tasa'), function (element) {
                    if (element.className.split(' ').indexOf(classForSelected) > -1)
                        element.style.display = "inherit";
                    else
                        element.style.display = "none";
                }, false);
            }


        }, false);
});


};

document.addEventListener("DOMContentLoaded", function(e){
    initialize();
});



/*
$(function(){
	$(".tipo-tasa").on("change", function(){
		var tipo = $(this).find("option:selected").attr("value");
		var panel = $(this).closest(".panel-body")
		console.log(panel)
		panel.find(".tipo").hide()
		switch(tipo){
			case "0":
				panel.find(".porcredito").show()
				break;
			case "1":
				panel.find(".global").show()
				break;
			default:
				panel.find(".miscelaneo").show()
				break;
		}
	});

	$(".nuevocurso").on("click", function(){
		var lista = $(this).closest(".lista").find(".lista-tasas");
		lista.append("<p>Hola</p>");
	});

	$("#actualizartasas").on("click", function(){
		var tasas = {};
		tasas.grado = {};
		tasas.master = {};

		var tasas_grado = tasas.grado;
		var tasas_master = tasas.master;
		$("#tasasgrado").find(".panel-body").each(function(index, item){
			var anno = $(item).find("select[name=curso] option:selected")[0].value;

			tasas_grado[anno] = {};

			var $tipotasa = $(item).find("select[name=tasa] option:selected")

			if($tipotasa.length > 0){
				tasas_grado[anno].tipo = parseInt($tipotasa[0].value)
			}else{
				tasas_grado[anno].tipo = 0
			}

			tasas_grado[anno].url = $(item).find("input[name=url]")[0].value;
			//console.log($(item).find("input[name=url]")[0].value)
			console.log(tasas_grado[anno].tipo)
			switch(tasas_grado[anno].tipo){
				case 0:
					// Precio por crédito
					var i = 1;
					while(i <= 4){
						console.log("Here")
						tasas_grado[anno]['tasas'+i] = $(item).find("input[name=tasas"+i+"]")[0].value;
						i++;
					}
					break;
				case 1:
					// Pago único
					tasas_grado[anno]['precio_unico'] = $(item).find("input[name=global]")[0].value;
					break;
				case 2:
					// Misceláneo
					tasas_grado[anno]['miscelaneo'] = $(item).find("textarea[name=descripcion]")[0].value;
					break;
				default:
					console.log("Error")
					break;

			}
		});
		$("#tasasmaster").find(".panel-body").each(function(index, item){
			var anno = $(item).find("select[name=curso] option:selected")[0].value;
			tasas_master[anno] = {};
			//tasas_master[anno].tipo = $(item).find("select[name=tasa] option:selected")[0].value
			tasas_master[anno].url = $(item).find("input[name=url]").text();
			switch(tasas_master[anno].tipo){
				case "0":
					// Precio por crédito
					var i = 1;
					while(i <= 4){
						tasas_master[anno]['tasas'+i] = $(item).find("input[name=tasas"+i+"]").text();
						i++;
					}
					break;
				case "1":
					// Pago único
					tasas_master[anno]['precio_unico'] = $(item).find("input[name=global]").text();
					break;
				case "2":
				default:
					// Misceláneo
					tasas_master[anno]['miscelaneo'] = $(item).find("textarea[name=descripcion]").text();
					break;
			}
		});

		$.ajax(".",{
			method: "POST",
			dataType: "json",
			//contentType: "application/json",
			data: {"tasas":JSON.stringify(tasas)},
			beforeSend: function(xhr, settings) {
				console.log(tasas)
		        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
		            // Send the token to same-origin, relative URLs only.
		            // Send the token only if the method warrants CSRF protection
		            // Using the CSRFToken value acquired earlier
		            xhr.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));
		        }
		    },
			success: function(data, textStatus, jqXhr){
				console.log(data);
			},
			error: function(jqXhr, textStatus, errorThrown){
				console.log(textStatus)
				console.log(errorThrown	)
				console.log(jqXhr.responseText)
			}
		});
	});
});
*/
/*
$(function(){
	$("#tasas-grado").find(".curso").each(function(index, item){
		$(item).text(min_curso + index + "/" + (min_curso + index + 1));
	});
	$("#tasas-master").find(".curso").each(function(index, item){
		$(item).text(min_curso + index + "/" + (min_curso + index + 1));
	});
});
*/