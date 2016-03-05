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
            if(self.universidades.length > 0) self.curso_actual = self.universidades[0].tasas_curso_actual.curso
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
};

Modal.prototype.render = function(content){
    this.element.find('.modal-content').html(content);
    this.element.find('.calculadora');
};

Modal.prototype.show = function(){
    this.element.css('display', 'block');
};

Modal.prototype.hide = function(){
    this.element.css('display', 'none');
};
