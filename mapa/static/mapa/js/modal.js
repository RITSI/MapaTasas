'use strict';

/*
* Simplifica la creación y el procesado de ventanas modales
* @param element Identificador CSS del elemento
* */
var Modal = function(element){
    this.element = $(element);
    this.element.html('');
};

/**
 * Crea la ventana modal
 */
Modal.prototype.create = function(){
    var self = this;
    this.tasas_data = [];
    var $element = this.element;
    this.element.html('<div class="modal-content"></div>');
    this.element.on('click', '.close-modal', function(){
        self.hide();
    });

    $(window).click(function(event){
        if($(event.target).is($element)){
            self.hide();
        }
    });

    $(document).keyup(function(e){
        if(e.keyCode == 27){
            self.hide();
        }
    });
    this.element.on('change', '#curso-selector', function(){
        self.recalculate($(this).find("option:selected").attr('value'));
    });

    this.element.on('input', '.input-ects', function(){
       self.recalculate(self.element.find('#curso-selector').find("option:selected").attr('value'))
    });

};

Modal.prototype.render = function(content, data, include_calculator){
    this.element.find('.modal-content').html(content);
    if(include_calculator){
        this.createCalculator(data);
        this.recalculate(this.element.find('#curso-selector').find("option:selected").attr('value'))
    }

};

Modal.prototype.show = function(){
    this.element.fadeIn();
    //this.element.css('display', 'block');
};

Modal.prototype.hide = function(){
    //this.element.css('display', 'none');
    this.element.fadeOut();
};

Modal.prototype.createCalculator = function(data){
    var $calculadora = this.element.find('.calculadora');
    $calculadora.css('display', 'block');
    var $curso_selector = $calculadora.find('#curso-selector');
    this.tasas_data = data;
    var curso_actual = this.curso_actual;
    $.each(this.tasas_data, function(key, value){
        $curso_selector.append($("<option></option>").attr("value", value.curso).text(value.curso));
        $curso_selector.find("option[value="+curso_actual+"]").prop('selected', true);
    });

};

Modal.prototype.recalculate = function(curso){
    var self = this;
    var ects = [];
    this.element.find('.input-ects').each(function(index, value){
        var number_ects = parseInt($(value).val(), 10) || false;
        if(number_ects == false){
            number_ects = 0;
            $(this).val('');
        }
        ects.push(number_ects);
    });

    var tasas = this.tasas_data.find(function(element){
        return element.curso == curso;
    });
    
    if(tasas == null){
        return;
    }

    var total_ects = 0;
    var total_precio = 0;

    $.each(ects, function(index, value){
        var precio = value * tasas['tasas'+(index+1)];
        self.element.find('#total-'+(index+1)).text(precio.toFixed(2).toString() + ' €');
        total_ects+=value;
        total_precio+=precio;

    });

    self.element.find("#total-ects").text(total_ects.toFixed(2));
    self.element.find("#total").text(total_precio.toFixed(2).toString() + ' €');
};
