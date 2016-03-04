$(document).ready(function () {
    //Intento de diseño responsive
    if ($(window).width() < 480) {
        $("#content").attr('class', "row");
        $("#map").attr("class", "well well-lg");
        $("#bootstrap_lista_units").attr("class", "well");
    } else {
        $("#content").attr('class', "");
        $("#map").attr("class", "well well-lg col-xs-5 col-sm-5 col-md-5 col-lg-5 col-xs-offset-1 col-sm-offset-1 col-md-offset-1 col-lg-offset-1");
        $("#bootstrap_lista_units").attr("class", "well col-xs-5 col-sm-5 col-md-5 col-lg-5");
    }
    var template_universidad_provincia;
    $.ajax({
        type:"GET",
        url:template_universidad_provincia_url,
        async: false,
        success: function(data){
            template_universidad_provincia = data;
        }
    });

    /*Creación del mapa programáticamente*/

    var width = 760;
    var height = 470;

    //Proyección Albers de los datos con ajustes para la Península
    var projection = d3.geo.albers()
            .center([0, 39.23])
            .rotate([3.4, 0])
            .parallels([50, 90])
            .scale(1200 * 2.3)
            .translate([width / 2.5, height / 2]);

    /*Creacion de un path según los ajustes de proyección*/
    var path = d3.geo.path()
            .projection(projection);

    /*Se añade un svg al div que contendrá el mapa*/
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
                .on("mouseover", provincia_hover)
                .on("click", provincia_click);

        svg.append("path")
                .datum(topojson.mesh(esp, esp.objects.subunits, function (a, b) {
                    return a !== b
                }))
                .attr("d", path)
                .attr("class", "subunit-boundary");
    });


    /*El diseño responsive del mapa no funciona con propiedades CSS, 
     debido a la naturaleza del mismo. Se debe redimensionar por JavaScript*/
    d3.select(window).on('resize', sizeChange);
    sizeChange(); // Redimensionado inicial

    // Cómputo de la media nacional con los datos disponibles:
    //TODO:
    // var indexes = ['tasas_2011', 'tasas_2012', 'tasas_2013', 'tasas_2014', 'tasas_2015'];
    //var average = {},
    //        avCount = {};
    //
    //indexes.forEach(function (index) {
    //    average[index] = 0;
    //    avCount[index] = 0;
    //});
    //
    //// Si se pone a true, faltan datos de tasas de algún centro
    //var avError = false;
    //
    //d3.json("data/uni/unis.json", function (error, file) {
    //    file.unis.forEach(function (uni) {
    //        // Para cada centro
    //        indexes.forEach(function (index) {
    //            // Para cada año
    //            if (uni[index] && uni[index]['tasas1']) {
    //                average[index] += parseInt(uni[index]['tasas1']);
    //                avCount[index]++;
    //            } else
    //                avError = true;
    //        });
    //    });
    //
    //    indexes.forEach(function (index) {
    //        if (avCount[index])
    //            average[index] /= avCount[index];
    //        else
    //            average[index] = 0;
    //    });
    //});

    function sizeChange() {
        //Intento de diseño para móviles
        if ($(window).width() < 480) {
            $("#content").attr('class', "row");
            $("#map").attr("class", "well well-lg");
            $("#bootstrap_lista_units").attr("class", "well");
        } else {
            $("#map").attr("class", "well well-lg col-xs-5 col-sm-5 col-md-5 col-lg-5 col-xs-offset-1 col-sm-offset-1 col-md-offset-1 col-lg-offset-1");
            $("#bootstrap_lista_units").attr("class", "well col-xs-5 col-sm-5 col-md-5 col-lg-5");
        }

        //Redimensionado en función del tamaño de la ventana
        d3.select("#map>svg>g").attr("transform", "scale(" + $("#map").width() / 700 + ")");
        $("#map>svg").height($("#map").width() * 0.618);
        $("#map>svg").width($("#map").width());

        d3.select("#map-canarias>svg>g").attr("transform", "scale(" + $("#map-canarias").width() / 200 + ")");
        $("#map-canarias>svg").height($("#map-canarias").width() * 0.518);
        $("#map-canarias>svg").width($("#map-canarias").width());
    }

    function provincia_hover(d) {
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
    }

    //Al dispararse este evento, se cargan los valores
    function provincia_click(d) {
        //TODO
        switch ($('.current').attr('data')) {
            case "master":
                //TODO
                //cargar_master(d);
                break;
            default:
            case "grado":
                cargar_grado(d);
                break;
        }

    }

    function cargar_grado(d) {

        //var resultados = [];
        //var convenios_filter = [];

        //Vaciado de los datos
        $('#bootstrap_lista_units').html('');

        //Filtrado de las universidades presentes en la provincia
        d3.json("/api/provincias/"+ d.id, function (error, unis) {

            var universidades = unis;

            if(universidades.length == 0){
                $('#bootstrap_lista_units').html('<p>No se han encontrado universidades en la provincia de ' + d.properties.name + ' que oferten estudios de Ingeniería Informática.</p>');
            }
            else
                create_dropdown_grado(universidades);
        });
    }

    //function cargar_master(d) {
    //    var resultados = [];
    //    //Vaciado de los datos
    //    $('#bootstrap_lista_units').html('');
    //
    //    d3.json("data/uni/unis-master.json", function (error, unis) {
    //        var universidades = unis.unis;
    //        $.each(universidades, function (index, value) {
    //            if (value.provincia === d.id)
    //                resultados.push(value);
    //        });
    //        if (resultados.length < 1) {
    //            $('#bootstrap_lista_units').html('<p>No se han encontrado universidades en la provincia de ' + d.properties.name + ' que oferten estudios de Ingeniería Informática.</p>');
    //        } else {
    //
    //            create_dropdown_grado(resultados, undefined);
    //        }
    //    });
    //}

    function create_graph(universidad) {

        var x = ['x'];
        var primera_matricula = ['Primera matrícula'];
        var segunda_matricula = ['Segunda matrícula'];
        var tercera_matricula = ['Tercera matrícula'];
        var cuarta_matricula = ['Cuarta matrícula'];

        console.log(universidad.tasas)
        $.each(universidad.tasas, function(index,tasa){
            x.push(new Date(tasa.curso.toString()));
            primera_matricula.push(tasa.tasas1);
            segunda_matricula.push(tasa.tasas2);
            tercera_matricula.push(tasa.tasas3);
            cuarta_matricula.push(tasa.tasas4);
        });
        //.parse("%yyyy", tasa.curso)

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
                            //              format : "%m/%d" // https://github.com/mbostock/d3/wiki/Time-Formatting#wiki-format
                            format: "%Y" // https://github.com/mbostock/d3/wiki/Time-Formatting#wiki-format
                        }
                    }
                }
        });
        /*if (universidad.observaciones) {
                $('#chart-' + universidad.siglas).prepend('<p class="alert alert-info">' + universidad.observaciones + '</p>');
            }*/

         //TODO $('#chart-' + universidad.siglas).append('<p class="alert alert-warning">' + averageErrorText + '</p>');

        return;
        ////TODO
        if (universidad.tasas_2011 && universidad.tasas_2012 && universidad.tasas_2013 && universidad.tasas_2014 && universidad.tasas_2015) {
            var averageErrorFlag = "",
                    averageErrorText = "";

            if (avError) {
                averageErrorFlag = "*";
                averageErrorText = "La media nacional se computa con los datos disponibles sobre las tasas de las universidades incluídas en este mapa, este dato es una aproximación. ";
            }

            averageErrorText += "La media nacional sólo tiene en cuenta las tasas de <strong>primera matrícula</strong>.";
        //TODO: Universidades con pago único/misceláneo

            var chart = c3.generate({
                bindto: "#chart-" + universidad.siglas,
                data: {
                    x: 'x',
                    x_format: '%Y',
                    columns: [
                        ['x', new Date('2011'), new Date('2012'), new Date('2013'), new Date('2014'), new Date('2015')],
                        ['Primera matrícula', universidad.tasas_2011.tasas1, universidad.tasas_2012.tasas1, universidad.tasas_2013.tasas1, universidad.tasas_2014.tasas1, universidad.tasas_2015.tasas1],
                        ['Segunda matrícula', universidad.tasas_2011.tasas2, universidad.tasas_2012.tasas2, universidad.tasas_2013.tasas2, universidad.tasas_2014.tasas2, universidad.tasas_2015.tasas2],
                        ['Tercera matrícula', universidad.tasas_2011.tasas3, universidad.tasas_2012.tasas3, universidad.tasas_2013.tasas3, universidad.tasas_2014.tasas3, universidad.tasas_2015.tasas3],
                        ['Cuarta matrícula', universidad.tasas_2011.tasas4, universidad.tasas_2012.tasas4, universidad.tasas_2013.tasas4, universidad.tasas_2014.tasas4, universidad.tasas_2015.tasas4],
                        //['Media nacional' + averageErrorFlag, average['tasas_2011'].toFixed(2), average['tasas_2012'].toFixed(2), average['tasas_2013'].toFixed(2), average['tasas_2014'].toFixed(2), average['tasas_2015'].toFixed(2)]
                    ]
                },
                axis: {
                    x: {
                        type: 'timeseries',
                        tick: {
                            //              format : "%m/%d" // https://github.com/mbostock/d3/wiki/Time-Formatting#wiki-format
                            format: "%Y" // https://github.com/mbostock/d3/wiki/Time-Formatting#wiki-format
                        }
                    }
                }
            });
            if (universidad.observaciones) {
                $('#chart-' + universidad.siglas).prepend('<p class="alert alert-info">' + universidad.observaciones + '</p>');
            }
            $('#chart-' + universidad.siglas).append('<p class="alert alert-warning">' + averageErrorText + '</p>');
        }

    }

    //Función de creación del dropdown con los datos. Utiliza la biblioteca mustache.js http://mustache.github.io/
    function create_dropdown_grado(universidades_provincia) {

        var rendered_data = Mustache.render(template_universidad_provincia, {"universidades":universidades_provincia});

        $('#bootstrap_lista_units').append(rendered_data);
        var panelsButton = $('.dropdown-user');
        var panels = $('.drop-panel');
        panels.hide();

        panelsButton.off();
        panelsButton.click(function(){
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
                create_graph(universidad);

            });

        });
        $('[data-toggle="tooltip"]').tooltip();

        return;


        //var dropdown = [];
        //var graph_data = {};
        $.each(universidades_provincia, function (index, value) {
            /*Los campus siguen  la regla {{universidad}}-{{nombre campus}}, 
             * al eliminar todo lo que se encuentra detras del guión podemos utilizar siempre la misma imagen, para distintos campus
             */
            //var siglas = value.siglas.replace(/\-.*/g, '');

            /*
             * creamos la estructura
             */ 
            //var estructura = {
            //    nombre: value.nombre,
            //    campus: value.campus,
            //    centro: value.centro,
            //    tipo: value.tipo,
            //    url: value.url,
            //    siglas: value.siglas.replace(/-.*/, ''),
            //    siglas_completas: value.siglas,
            //    observaciones: value.observaciones,
            //    clase: 'chart-' + value.siglas,
            //    tasas1: value.tasas_2015.tasas1,
            //    tasas2: value.tasas_2015.tasas2,
            //    tasas3: value.tasas_2015.tasas3,
            //    tasas4: value.tasas_2015.tasas4,
            //    urls: [{
            //            "url": value.tasas_2011.url,
            //            "fecha": 2011
            //        }, {
            //            "url": value.tasas_2012.url,
            //            "fecha": 2012
            //        }, {
            //            "url": value.tasas_2013.url,
            //            "fecha": 2013
            //        }, {
            //            "url": value.tasas_2014.url,
            //            "fecha": 2014
            //        }, {
            //            "url": value.tasas_2015.url,
            //            "fecha": 2015
            //        }]
            //}
            

            //El archivo .mst contiene la plantilla compatible con Mustache
            $.get('templates/template_universidad_provincia.mst', function (template_universidad_provincia) {
                //Se añaden los datos del curso actual, y los datos generales
                var render_resultados = Mustache.render(template_universidad_provincia, estructura);

                $('#bootstrap_lista_units').append(render_resultados); //.create_graph(value);
                //create_graph(value);

                var panelsButton = $('.dropdown-user');
                var panels = $('.drop-' + value.siglas.replace('/-.*/', ''));
                panels.hide();

                //Se desactivan todos los eventos, dado que en caso contrario origina problemas al añadir y eliminar un panel de información (se superponen eventos)
                panelsButton.off();
                //Se reañade el evento
                panelsButton.click(function () {
                    //Se obtiene el atributo data-for
                    var dataFor = $(this).attr('data-for');
                    var idFor = $(dataFor);
                    var currentButton = $(this);
                    idFor.slideToggle(400, function () {

                        if (idFor.is(':visible')) {
                            currentButton.html('<i class="glyphicon glyphicon-chevron-up text-muted"></i>');
                        } else {
                            currentButton.html('<i class="glyphicon glyphicon-chevron-down text-muted"></i>');
                        }

                        d3.json("data/uni/unis.json", function (error, unis) {
                            var value = $.grep(unis.unis, function (e, i) {
                                return e.siglas === dataFor.replace('\.drop-', '')
                            });
                            create_graph(value[0]);
                        });
                    });

                });
                $('[data-toggle="tooltip"]').tooltip();
            });
        });
    }
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