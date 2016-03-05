$(function(){

    var $modal = $('#tasa-modal');
    var $close = $('#close-modal');
    $close.click(function(){
        $modal.css('display', 'none');
    });
    $modal.css('display', 'block');
    $(window).click(function(event){
        if($(event.target).is($modal)){
            $modal.css('display', 'none');
        }
    });
});

/*
* Simplifica la creación y el procesado de ventanas modales
* @param element Identificador CSS del elemento
* */
var Modal = function(element){
    this.element = $(element);
};

/**
 * Crea la ventana modal
 * @param content Contenido a mostrar
 */
Modal.prototype.create = function(content){
    this.element.html('<div class="modal-content"><span id="close-modal">x</span><p>Some text in the Modal..</p></div>');
};

Modal.prototype.show = function(){
    this.element.css('display', 'block');
};

Modal.prototype.hide = function(){
    this.element.css('display', 'none');
}