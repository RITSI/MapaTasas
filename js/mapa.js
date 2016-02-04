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


    /*El mapa a utilizar es esp-ascii.json . Es igual que esp.json, excepto que todos los caracteres son ASCII
     Se hace asi dado que los nombres de las provincias son los ids de cada contorno svg. Si se utilizaran caracteres
     no ASCII, no funcionaría*/
    d3.json("maps/esp.json", function (error, esp) {
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
    sizeChange();

    // Cómputo de la media nacional con los datos disponibles:
    var indexes = ['tasas_2011', 'tasas_2012', 'tasas_2013', 'tasas_2014', 'tasas_2015'];
    var average = {},
            avCount = {};

    indexes.forEach(function (index) {
        average[index] = 0;
        avCount[index] = 0;
    });

    // Si se pone a true, faltan datos de tasas de algún centro
    var avError = false;

    d3.json("data/uni/unis.json", function (error, file) {
        file.unis.forEach(function (uni) {
            // Para cada centro
            indexes.forEach(function (index) {
                // Para cada año
                if (uni[index] && uni[index]['tasas1']) {
                    average[index] += parseInt(uni[index]['tasas1']);
                    avCount[index]++;
                } else
                    avError = true;
            });
        });

        indexes.forEach(function (index) {
            if (avCount[index])
                average[index] /= avCount[index];
            else
                average[index] = 0;
        });
    });

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
        switch ($('.current').attr('data')) {
            case "master":
                cargar_master(d);
                break;
            default:
            case "grado":
                cargar_grado(d);
                break;
        }

    }

    function cargar_grado(d) {
        var resultados = [];
        var convenios_filter = [];

        //Vaciado de los datos
        $('#bootstrap_lista_units').html('');

        //Filtrado de las universidades presentes en la provincia
        d3.json("data/uni/unis.json", function (error, unis) {
            var universidades = unis.unis;
            /*Se recorren todas las universidades presentes, 
             y si alguna tiene como provincia la seleccionada por el cursor, 
             se incluye en el array*/
            $.each(universidades, function (index, value) {
                if (value.provincia === d.id)
                    resultados.push(value);
            });

            var universidades_provincia = [];
            if (resultados.length > 0) {
                $.each(resultados, function (index, value) {
                    universidades_provincia.push(resultados[index]);
                    for (var i = universidades.length - 1; i >= 0; i--) {
                        if (resultados[index].convenios.indexOf(universidades[i].siglas) > -1) {
                            convenios_filter.push(universidades[i]);
                        }
                    }
                    ;
                });
                create_dropdown_grado(universidades_provincia, convenios_filter);
            } else {
                //Si no hay universidades
                $('#bootstrap_lista_units').html('<p>No se han encontrado universidades en la provincia de ' + d.properties.name + ' que oferten estudios de Ingeniería Informática.</p>');
            }
        });
    }

    function cargar_master(d) {
        var resultados = [];
        //Vaciado de los datos
        $('#bootstrap_lista_units').html('');

        d3.json("data/uni/unis-master.json", function (error, unis) {
            var universidades = unis.unis;
            $.each(universidades, function (index, value) {
                if (value.provincia === d.id)
                    resultados.push(value);
            });
            if (resultados.length < 1) {
                $('#bootstrap_lista_units').html('<p>No se han encontrado universidades en la provincia de ' + d.properties.name + ' que oferten estudios de Ingeniería Informática.</p>');
            } else {

                create_dropdown_grado(resultados, undefined);
            }
        });
    }

    function create_graph(value) {
        if (value.tasas_2011 && value.tasas_2012 && value.tasas_2013 && value.tasas_2014 && value.tasas_2015) {
            var averageErrorFlag = "",
                    averageErrorText = "";

            if (avError) {
                averageErrorFlag = "*";
                averageErrorText = "La media nacional se computa con los datos disponibles sobre las tasas de las universidades incluídas en este mapa, este dato es una aproximación. ";
            }

            averageErrorText += "La media nacional sólo tiene en cuenta las tasas de <strong>primera matrícula</strong>.";

            var chart = c3.generate({
                bindto: "#chart-" + value.siglas,
                data: {
                    x: 'x',
                    x_format: '%Y',
                    columns: [
                        ['x', new Date('2011'), new Date('2012'), new Date('2013'), new Date('2014'), new Date('2015')],
                        ['Primera matrícula', value.tasas_2011.tasas1, value.tasas_2012.tasas1, value.tasas_2013.tasas1, value.tasas_2014.tasas1, value.tasas_2015.tasas1],
                        ['Segunda matrícula', value.tasas_2011.tasas2, value.tasas_2012.tasas2, value.tasas_2013.tasas2, value.tasas_2014.tasas2, value.tasas_2015.tasas2],
                        ['Tercera matrícula', value.tasas_2011.tasas3, value.tasas_2012.tasas3, value.tasas_2013.tasas3, value.tasas_2014.tasas3, value.tasas_2015.tasas3],
                        ['Cuarta matrícula', value.tasas_2011.tasas4, value.tasas_2012.tasas4, value.tasas_2013.tasas4, value.tasas_2014.tasas4, value.tasas_2015.tasas4],
                        ['Media nacional' + averageErrorFlag, average['tasas_2011'].toFixed(2), average['tasas_2012'].toFixed(2), average['tasas_2013'].toFixed(2), average['tasas_2014'].toFixed(2), average['tasas_2015'].toFixed(2)]
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
            if (value.observaciones) {
                $('#chart-' + value.siglas).append('<p class="alert alert-info">' + value.observaciones + '</p>');
            }
            $('#chart-' + value.siglas).append('<p class="alert alert-warning">' + averageErrorText + '</p>');
        }

    }

    //Función de creación del dropdown con los datos. Utiliza la biblioteca mustache.js http://mustache.github.io/
    function create_dropdown_grado(universidades_provincia, universidades) {
        var dropdown = [];
        var graph_data = {};
        $.each(universidades_provincia, function (index, value) {
            /*Los campus siguen  la regla {{universidad}}-{{nombre campus}}, 
             * al eliminar todo lo que se encuentra detras del guión podemos utilizar siempre la misma imagen, para distintos campus
             */
            var siglas = value.siglas.replace(/\-.*/g, '');

            //El archivo .mst contiene la plantilla compatible con Mustache
            $.get('templates/template_universidad_provincia.mst', function (template_universidad_provincia) {
                //Se añaden los datos del curso actual, y los datos generales
                var render_resultados = Mustache.render(template_universidad_provincia, {
                    nombre: value.nombre,
                    campus: value.campus,
                    centro: value.centro,
                    tipo: value.tipo,
                    url: value.url,
                    siglas: value.siglas.replace(/-.*/, ''),
                    siglas_completas: value.siglas,
                    observaciones: value.observaciones,
                    clase: 'chart-' + value.siglas,
                    tasas1: value.tasas_2014.tasas1,
                    tasas2: value.tasas_2014.tasas2,
                    tasas3: value.tasas_2014.tasas3,
                    tasas4: value.tasas_2014.tasas4,
                    tasas5: value.tasas_2015.tasas5,
                    urls: [{
                            "url": value.tasas_2011.url,
                            "fecha": 2011
                        }, {
                            "url": value.tasas_2012.url,
                            "fecha": 2012
                        }, {
                            "url": value.tasas_2013.url,
                            "fecha": 2013
                        }, {
                            "url": value.tasas_2014.url,
                            "fecha": 2014
                        }, {
                            "url": value.tasas_2015.url,
                            "fecha": 2015
                        }]
                });

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
        $link = $(this);
        if (!($link.hasClass('current'))) {
            $('.current').removeClass('current');
            $link.addClass('current');
            datos = $link.attr('data');

            $('#bootstrap_lista_units').html('<p>Haz click en una provincia para conocer la oferta de estudios de ' + (datos == "grado" ? datos : "máster") + '.</p>');
        }
    });

});