'use strict';

document.addEventListener("DOMContentLoaded", function(){
    var select_tipo_tasa = document.getElementsByClassName("tipo-tasa-selector");
    var form = document.getElementById("tasas-form");
    var submitButton = document.getElementById("submit-tasas");
    var PRECIO_POR_CREDITO = 0;
    var PAGO_UNICO = 1;
    var MISCELANEO = 2;

    var classes_tipo_tasa = {};
    classes_tipo_tasa[PRECIO_POR_CREDITO] = "porcredito";
    classes_tipo_tasa[PAGO_UNICO] = "global";
    classes_tipo_tasa[MISCELANEO] = "miscelaneo";


    var remove_contradictory_data = function(option, element){
        var options = [0,1,2];
        if(option === undefined || option ===""){
            return remove_contradictory_data([0,1,2], element);
        }

        if(option == parseInt(option, 10)){
            options.splice(option, 1);
          return remove_contradictory_data(options, element);
        }

        if(option.constructor == Array){

            Array.prototype.forEach.call(option, function(o){
                var fields;
                switch (o){
                    case 0:
                        fields = element.getElementsByClassName("tipo-tasa")[0];

                        break;
                    case 1:
                        fields = element.getElementsByClassName("tipo-tasa")[1];
                        break;
                    case 2:
                        fields = element.getElementsByClassName("tipo-tasa")[2];
                        break;

                }
                var input_fields = fields.getElementsByTagName('input');
                var textarea_fields = fields.getElementsByTagName('textarea');


                Array.prototype.forEach.call(input_fields, function(field){
                    field.value = "";
                });
                Array.prototype.forEach.call(textarea_fields, function(field){
                    field.value = "";
                });

            });
        }


    };

    var initialize = function(){
        submitButton.addEventListener('click', function(){
            var tasas = form.getElementsByClassName('tasas-data');
            Array.prototype.forEach.call(tasas, function(tasa){
                var parent = tasa.parentNode.getElementsByClassName('basics')[0];
                var selector = parent.getElementsByTagName('select')[0];
                remove_contradictory_data(selector.options[selector.selectedIndex].value, tasa);
            });

        });

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

            element.addEventListener('change', function(){
                var tasas_div = this.parentNode.parentNode.parentNode.getElementsByClassName('tasas-data')[0];
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


    initialize();
});
