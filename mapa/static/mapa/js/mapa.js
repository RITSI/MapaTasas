'use strict';

/*
 * Incrementa el número dado. Útil para representar cursos
 * @param text Valor a aumentar
 * return: El número incrementado como cadena de caracteres
 */
//noinspection JSUnresolvedVariable
Handlebars.registerHelper('increment', function(text){
    return (parseInt(text)+1).toString();
});

var template_universidad_provincia = null;
var template_universidad_detalle = null;
var modal;

/**
 * Redimensiona los diferentes elementos al cambiar las dimensiones de la pantalla
 */
function sizeChange() {
    var $map = $("#map");
    if ($(window).width() < 480) {
        $("#content").attr('class', "row");
        $map.attr("class", "well well-lg");
        $("#bootstrap_lista_units").attr("class", "well");
    } else {
        $map.attr("class", "well well-lg col-xs-5 col-sm-5 col-md-5 col-lg-5 col-xs-offset-1 col-sm-offset-1 col-md-offset-1 col-lg-offset-1");
        $("#bootstrap_lista_units").attr("class", "well col-xs-5 col-sm-5 col-md-5 col-lg-5");
    }

    //Redimensionado en función del tamaño de la ventana

    d3.select("#map>svg>g").attr("transform", "scale(" + $map.width() / 700 + ")");
    $map.find("svg").height($map.width() * 0.618).width($map.width());
}

/**
 * Crea el panel de información sobre la universidad
 * @param universidades Lista de universidades en la provincia dada
 * @param media Media nacional
 */
function createDropdownGrado(universidades, media){
    //TODO: print media for current curso
    if(!template_universidad_provincia) return; //TODO: handle error

    universidades.forEach(function(uni){
        uni.tasas_curso_actual = uni.tasas.find(function(tasa){
            return tasa.actual;
        });
    });
    var rendered_data = template_universidad_provincia({universidades: universidades});

    $('#bootstrap_lista_units').append(rendered_data);

    var $panelsButton = $('.dropdown-user');
    var $panels = $('.drop-panel');
    $panels.hide();

    $panelsButton.off();
    $panelsButton.click(function(){
        var dataFor = $(this).attr('data-for');
        var $idFor = $(dataFor);
        var $currentButton = $(this);
        $idFor.slideToggle(400, function(){
            var universidad = universidades.find(function(value){
                   return value.siglas == $idFor.attr('id');
                });
            if($idFor.is(':visible')){
                $currentButton.html('<i class="glyphicon glyphicon-chevron-up text-muted"></i>');
                createGraph(universidad, media);
            }else{
                $currentButton.html('<i class="glyphicon glyphicon-chevron-down text-muted"></i>');
                $("#chart-"+universidad.siglas).html('');
            }
        });
    });
    $('[data-toggle="tooltip"]').tooltip();
}

var cargarGrado = function(d){
    //Vaciado de los datos
    $('#bootstrap_lista_units').html('');

    // Llamada a la API
    d3.json("/api/provincias/"+ d.id, function (error, universidades) {
        //TODO: Handle error
        if(universidades.length == 0){
            $('#bootstrap_lista_units').html('<p>No se han encontrado universidades en la provincia de '
                                             + d.properties.name +
                                             ' que oferten estudios de Ingeniería Informática.</p>');
        }
        else {
            d3.json("api/average/", function(error, average){
                createDropdownGrado(universidades, average);
            });
        }
    });
};

//TODO: var cargarMaster

/**
 * Crea el marcador con el nombre de la provincia
 */
function provinciaHover(){
    $('.subunit').tipsy({
        gravity: 's',
        html: true,
        title: function () {
            var m = this.__data__;
            //Se retorna el valor Unicode del nombre ASCII
            return m.properties.name;
        }
    });
}

/**
 * Carga la información sobre la provincia
 */
function provinciaClick(d){
    switch ($('.current').attr('data')) {
        case "master":
            //TODO
            //cargar_master(d);
            break;
        default:
        case "grado":
            cargarGrado(d);
            break;
    }
}

/**
 * Crea y muestra el gráfico con la información de tasas
 * @param universidad Datos
 * @param media Media nacional
 */
function createGraph(universidad, media){
    var x = ['x'];
    var primera_matricula = ['Primera matrícula'];
    var segunda_matricula = ['Segunda matrícula'];
    var tercera_matricula = ['Tercera matrícula'];
    var cuarta_matricula = ['Cuarta matrícula'];
    var media_nacional = ['Media nacional'];
    var cursos = new Set();
    universidad.tasas.forEach(function(tasa){
        // TODO: Se incluye una condición para así poder mostrar sólo las tasas de grado.
        // NOTE: Retocarlo cuando se haga la parte de máster
        if (tasa.tipo_titulacion === 0){
            x.push(new Date(tasa.curso.toString()));
            cursos.add(tasa.curso.toString());
            primera_matricula.push(tasa.tasas1.toFixed(2));
            segunda_matricula.push(tasa.tasas2.toFixed(2));
            tercera_matricula.push(tasa.tasas3.toFixed(2));
            cuarta_matricula.push(tasa.tasas4.toFixed(2));
        }
    });

    Object.keys(media).sort().forEach(function(curso){
        if(cursos.has(curso))
            media_nacional.push(media[curso].media_1.data.toFixed(2));
    });

    //TODO: Compute
    var averageErrorText = "La media nacional se computa con los datos disponibles sobre las tasas de las"
                            + " universidades incluidas en este mapa, este dato es una aproximación. ";
    averageErrorText += "La media nacional sólo tiene en cuenta las tasas de <strong>primera matrícula</strong>.";
    var chart = c3.generate({
        bindto: "#chart-"+universidad.siglas,
        data:{
            x:'x',
            x_format:'%Y',
            columns:[x,primera_matricula, segunda_matricula, tercera_matricula, cuarta_matricula, media_nacional]
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: "%Y" // https://github.com/mbostock/d3/wiki/Time-Formatting#wiki-format
                }
            }
        }
    });
    $('#chart-' + universidad.siglas).append('<p class="alert alert-warning">' + averageErrorText + '</p>');
}

var createDetalle = function(universidad){
    $.ajax({
        url: "/api/universidad/"+universidad,
        success: function(data){
            modal.render(template_universidad_detalle(data), data.tasas, true);
            modal.show();
        },
        error: function(xhr, textStatus){
            //TODO
        }
    })
};

$(function(){
    //TODO:Intento de diseño responsive
    var $bootstrap_lista_units = $("#bootstrap_lista_units");
    if ($(window).width() < 480) {
        $("#content").attr('class', "row");
        $("#map").attr("class", "well well-lg");
        $bootstrap_lista_units.attr("class", "well");
    } else {
        $("#content").attr('class', "");
        $("#map").attr("class", "well well-lg col-xs-5 col-sm-5 col-md-5 col-lg-5 col-xs-offset-1 col-sm-offset-1 col-md-offset-1 col-lg-offset-1");
        $bootstrap_lista_units.attr("class", "well col-xs-5 col-sm-5 col-md-5 col-lg-5");
    }

    // Petición bloqueante que descarga (una vez) la plantilla de Mustache.
    $.ajax({
        type:"GET",
        url:template_universidad_provincia_url,
        async: false,
        success: function(data){
            template_universidad_provincia = Handlebars.compile(data);
        },
        error: function(xhr, textStatus){
            //TODO
        }
    });

    $.ajax({
        type:"GET",
        url:template_universidad_detalle_url,
        async:false,
        success: function(data){
            template_universidad_detalle = Handlebars.compile(data);
        },
        error: function(xhr, textStatus){
            //TODO
        }
    });

    //Creación programática del mapa
    var width = 760; //TODO: adjust to window resolution
    var height = 470;

    //Proyección Albers de los datos con ajustes para la Península
    var projection = d3.geo.albers()
            .center([0, 39.23])
            .rotate([3.4, 0])
            .parallels([50, 90])
            .scale(1200 * 2.3)
            .translate([width / 2.5, height / 2]);

    //Creacion de un path SVG según los ajustes de proyección
    var path = d3.geo.path()
            .projection(projection);

    // Se añade un svg al div que contendrá el mapa
    var svg = d3.select("#map")
            .append("svg")
            .append("g")
            .attr("width", width)
            .attr("height", height);

    d3.json(mapa_url, function (error, esp) {
        //Se añaden una a una las provincias descritas en el JSON
        svg.selectAll(".subunit")
                .data(topojson.feature(esp, esp.objects.subunits).features)
                .enter().append("path")
                .attr("class", function (d) {
                    return "subunit " + d.id;
                })
                .attr("d", path)
                //Se asignan handlers a los eventos de interes
                .on("mouseover", provinciaHover)
                .on("click", provinciaClick);

        svg.append("path")
                .datum(topojson.mesh(esp, esp.objects.subunits, function (a, b) {
                    return a !== b
                }))
                .attr("d", path)
                .attr("class", "subunit-boundary");
    });

    /*TODO:El diseño responsive del mapa no funciona con propiedades CSS,
     debido a la naturaleza del mismo. Se debe redimensionar por JavaScript*/
    d3.select(window).on('resize', sizeChange);
    sizeChange(); // Redimensionado inicial

    //TODO:
    $('.tab-link').click(function () {
        //TODO
        var $link = $(this);
        if (!($link.hasClass('current'))) {
            $('.current').removeClass('current');
            $link.addClass('current');
            var datos = $link.attr('data');

            $bootstrap_lista_units.html('<p>Haz click en una provincia para conocer la oferta de estudios de ' + (datos == "grado" ? datos : "máster") + '.</p>');
        }
    });
    modal = new Modal('#tasa-modal');
    modal.create();
    $bootstrap_lista_units.on('click', '.tasa-modal', function(e){
        createDetalle($(this).attr('data-for'));
    });
});
