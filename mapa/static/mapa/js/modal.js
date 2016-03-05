/*
* Simplifica la creación y el procesado de ventanas modales
* @param element Identificador CSS del elemento
* */
var Modal = function(element){
    this.element = $(element);
    this.element.html('');
    var self = this;
    $.ajax({
        url:"/api/universidad/?fields[]=siglas&fields[]=nombre&fields[]=tasas_curso_actual",
        async:false,
        type:"GET",
        success:function(data){
            self.universidades = data;
            self.curso_actual = (self.universidades.length > 0) ? self.universidades[0].tasas_curso_actual.curso : false;
        },
        error: function(xhr, textStatus){
            //TODO
        }
    })
};

/**
 * Crea la ventana modal
 * @param content Contenido a mostrar
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
    this.element.on('change', '.curso-selector', function(e){
        self.recalculate($(this).find("option:selected").attr('value'));
    });

};

Modal.prototype.render = function(content, data, include_calculator){
    this.element.find('.modal-content').html(content);
    if(include_calculator){
        this.createCalculator(data);
    }

};

Modal.prototype.show = function(){
    this.element.css('display', 'block');
};

Modal.prototype.hide = function(){
    this.element.css('display', 'none');
};

Modal.prototype.createCalculator = function(data){
    var $calculadora = this.element.find('.calculadora');
    $calculadora.css('display', 'block');
    var $curso_selector = $calculadora.find('.curso-selector');
    this.tasas_data = data;
    var curso_actual = this.curso_actual;
    $.each(this.tasas_data, function(key, value){
        $curso_selector.append($("<option></option>").attr("value", value.curso).text(value.curso));
        $curso_selector.find("option[value="+curso_actual+"]").prop('selected', true);
    });

};

Modal.prototype.recalculate = function(curso){
    var ects = [];
    this.element.find('.input-ects').each(function(index, value){
        var number_ects = parseInt($(value).val(), 10) || 0;
        if(number_ects == 0){
            $(this).val(0);
        }
        ects.push(number_ects);
    });

    var tasas = tasas_data.find(function(element, index, array){
        return element.curso == curso;
    });
    console.log(tasas)
    if(tasas == undefined){
        return;
    }
    $.each(tasas, function(index, value){
        console.log(index, value);
    });
    /*console.log(this.element.find('#ects1').text())
    console.log(this.element.find('#ects2').text())
    console.log(this.element.find('#ects3').text())
    console.log(this.element.find('#ects4').text())*/
};