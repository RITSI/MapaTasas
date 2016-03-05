/*$(function(){

    var $modal = $('#tasa-modal');
    var $close = $('#close-modal');
    $close.click(function(){
        $modal.css('display', 'none');
    });
    $modal.css('display', 'block');


    $(document).keyup(function(e){
        if(e.keyCode == 27){
            $modal.css('display', 'none');
        }
    });
    #t
});*/

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
};

Modal.prototype.show = function(){
    this.element.css('display', 'block');
};

Modal.prototype.hide = function(){
    this.element.css('display', 'none');
};
