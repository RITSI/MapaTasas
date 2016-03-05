var template_universidad_provincia;
var sizeChange = function() {
    //Intento de diseño para móviles
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
};

var createDropdownGrado = function(universidades_provincia){

    if(template_universidad_provincia === undefined) return; //TODO: handle error
    var rendered_data = template_universidad_provincia({"universidades":universidades_provincia});

    $('#bootstrap_lista_units').append(rendered_data);

    var $panelsButton = $('.dropdown-user');
    var $panels = $('.drop-panel');
    $panels.hide();

    $panelsButton.off();
    $panelsButton.click(function(){
       //TODO: Move to general binding using jQuery magic
        var dataFor = $(this).attr('data-for');
        var $idFor = $(dataFor);
        var $currentButton = $(this);
        $idFor.slideToggle(400, function(){
           if($idFor.is(':visible')){
               $currentButton.html('<i class="glyphicon glyphicon-chevron-up text-muted"></i>');
           }else{
               $currentButton.html('<i class="glyphicon glyphicon-chevron-down text-muted"></i>');
           }
            universidad = universidades_provincia.filter(function(value){
                return value.siglas == $idFor.attr('id');
            })[0];
            createGraph(universidad);

        });

    });
    $('[data-toggle="tooltip"]').tooltip();
};

var cargarGrado = function(d){
    //Vaciado de los datos
    $('#bootstrap_lista_units').html('');

    // Llamada a la API
    d3.json("/api/provincias/"+ d.id, function (error, universidades) {
        if(universidades.length == 0){
            $('#bootstrap_lista_units').html('<p>No se han encontrado universidades en la provincia de ' + d.properties.name + ' que oferten estudios de Ingeniería Informática.</p>');
        }
        else {
            createDropdownGrado(universidades);
        }
    });
};

//TODO: var cargarMaster

var provinciaHover = function(d){
    //Se crea el marcador con el nombre
    $('.subunit').tipsy({
        gravity: 's',
        html: true,
        title: function () {
            var m = this.__data__;
            //Se retorna el valor Unicode del nombre ASCII
            return m.properties.name;
        }
    });
};

var provinciaClick = function(d){
    //TODO
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
};

var createGraph = function(universidad){
    var x = ['x'];
    var primera_matricula = ['Primera matrícula'];
    var segunda_matricula = ['Segunda matrícula'];
    var tercera_matricula = ['Tercera matrícula'];
    var cuarta_matricula = ['Cuarta matrícula'];

    $.each(universidad.tasas, function(index,tasa){
        x.push(new Date(tasa.curso.toString()));
        primera_matricula.push(tasa.tasas1);
        segunda_matricula.push(tasa.tasas2);
        tercera_matricula.push(tasa.tasas3);
        cuarta_matricula.push(tasa.tasas4);
    });

    var chart = c3.generate({
        bindto: "#chart-"+universidad.siglas,
        data:{
            x:'x',
            x_format:'%Y',
            columns:[x,primera_matricula, segunda_matricula, tercera_matricula, cuarta_matricula]
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
};

$(function(){
    //TODO:Intento de diseño responsive
    if ($(window).width() < 480) {
        $("#content").attr('class', "row");
        $("#map").attr("class", "well well-lg");
        $("#bootstrap_lista_units").attr("class", "well");
    } else {
        $("#content").attr('class', "");
        $("#map").attr("class", "well well-lg col-xs-5 col-sm-5 col-md-5 col-lg-5 col-xs-offset-1 col-sm-offset-1 col-md-offset-1 col-lg-offset-1");
        $("#bootstrap_lista_units").attr("class", "well col-xs-5 col-sm-5 col-md-5 col-lg-5");
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
        $link = $(this);
        if (!($link.hasClass('current'))) {
            $('.current').removeClass('current');
            $link.addClass('current');
            datos = $link.attr('data');

            $('#bootstrap_lista_units').html('<p>Haz click en una provincia para conocer la oferta de estudios de ' + (datos == "grado" ? datos : "máster") + '.</p>');
        }
    });
});
