"use strict";

var width = 400;
var height = 30;

var tooltip = d3.select("body").append("div").attr("class", "tooltip");

function show_tooltip(message) {
    tooltip.html(message).style("left", d3.event.pageX + "px").style("top", d3.event.pageY - 28 + "px").style("opacity", 1);
}

function hide_tooltip() {
    tooltip.style("opacity", 0);
}

function insert_chart(target, data, colors) {
    var scale = d3.scale.linear().domain([0, d3.sum(data, function (d) {
        return d.value;
    })]).range([0, width]);

    var percentage = d3.scale.linear().domain([0, d3.sum(data, function (d) {
        return d.value;
    })]).range([0, 100]);

    var svg = d3.select(target).append("svg").attr("width", width).attr("height", height).on("mouseleave", function (d) {
        return hide_tooltip();
    });

    var curx = 0;

    var expanded = false;

    svg.selectAll("rect").data(data).enter().append("rect").attr("class", function (d, i) {
        return "rect-" + i;
    }).attr("width", function (d) {
        return scale(d.value);
    }).attr("height", height).attr("x", function (d) {
        var ret = curx;
        curx += scale(d.value);
        return ret;
    }).attr("y", 0).attr("fill", function (d, i) {
        return colors[i];
    }).on("mousemove", function (d) {
        if (!expanded) show_tooltip(d.label + ": " + Math.round(percentage(d.value)) + "%");
    });

    svg.on("click", function () {
        if (!expanded) {
            svg.selectAll("text").remove();
            hide_tooltip();

            var cury = 0;
            for (var i = 0; i < data.length; i++) {
                svg.select(".rect-" + i).transition().duration(100).attr("y", cury).transition().duration(100).attr("x", 130);

                svg.append("text").transition().delay(200).attr("x", 125).attr("y", cury + height / 2).attr("alignment-baseline", "middle").attr("dominant-baseline", "middle").attr("text-anchor", "end").text(data[i].label);

                var labelinside = percentage(data[i].value) > 20;
                var _width = scale(data[i].value);

                svg.append("text").transition().delay(200).attr("x", 130 + (labelinside ? _width - 5 : _width + 5)).attr("y", cury + height / 2).attr("dominant-baseline", "middle").attr("text-anchor", labelinside ? "end" : "start").text(Math.round(percentage(data[i].value)) + "%");

                cury += height;
            }

            svg.transition().duration(100).attr("height", cury);

            expanded = true;
        } else {
            (function () {
                svg.selectAll("text").remove();

                var curx = 0;
                svg.selectAll("rect").transition().duration(100).attr("x", function (d) {
                    var ret = curx;
                    curx += scale(d.value);
                    return ret;
                }).transition().duration(100).attr("y", 0);

                svg.transition().delay(100).duration(100).attr("height", height);

                expanded = false;
            })();
        }
    });
};

var insert_stacked = function insert_stacked(target, data, colors) {
    var height = 300;
    var margin = {
        left: 30,
        right: 30,
        top: 0,
        bottom: 30
    };

    data.forEach(function (year) {
        year.data.forEach(function (point) {
            point.year = year.label;
        });
    });

    var xScale = d3.scale.linear().domain(d3.extent(data, function (d) {
        return d.label;
    })).range([0, width]);

    var yScale = d3.scale.linear().domain([0, 1]).range([0, height]);

    var svg = d3.select(target).append("svg").attr("width", width + margin.left + margin.right).attr("height", height + margin.top + margin.bottom).attr("style", "margin-left: -" + margin.left + "px; " + ("margin-right: -" + margin.right + "px;")).on("mouseleave", function (d) {
        return hide_tooltip();
    }).append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    var xAxis = d3.svg.axis().scale(xScale).orient("bottom").ticks(data.length).tickValues(data.map(function (x) {
        return x.label;
    })).tickFormat(d3.format("d"));

    var stacking = d3.layout.stack().offset("expand").values(function (d) {
        return d.values;
    }).x(function (d) {
        return d.year;
    }).y(function (d) {
        return d.value;
    });

    var unnested = [].concat.apply([], data.map(function (year) {
        return year.data;
    }));

    var nested = d3.nest().key(function (d) {
        return d.label;
    }).entries(unnested);

    var layers = stacking(nested);

    var area = d3.svg.area().x(function (d) {
        return xScale(d.year);
    }).y0(function (d) {
        return yScale(d.y0);
    }).y1(function (d) {
        return yScale(d.y0 + d.y);
    });

    svg.selectAll(".layer").data(layers).enter().append("path").attr("class", "layer").attr("d", function (d) {
        return area(d.values);
    }).style("fill", function (d, i) {
        return colors[i];
    }).on("mousemove", function (d) {
        return show_tooltip(d.key);
    });

    svg.append("g").attr("class", "axis").attr("transform", "translate(0," + height + ")").call(xAxis);
};