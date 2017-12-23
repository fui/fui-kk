$(function () {
  var vurdering = ["Lite bra", "Mindre bra", "Greit", "Bra", "Meget bra", "Særdeles bra"];
  var semesterkoder = {
    'H': 'høsten',
    'V': 'våren'
  };
  var title_prefix = 'Generell vurdering fra '
  var avg_score = {
    'V2009': 4.40,
    'H2009': 4.40,
    'V2010': 4.22,
    'H2010': 4.15,
    'V2011': 4.32,
    'H2011': 4.08,
    'V2012': 4.36,
    'H2012': 4.26,
    'V2013': 4.19,
    'H2013': 4.36,
    'V2014': 4.21,
    'H2014': 4.20,
    'V2015': 4.23,
    'H2015': 4.30,
    'V2016': 4.41
  }

  if (document.body.lang && document.body.lang == "en") {
    title_prefix = 'General rating since '
    vurdering = ["Not good", "Not that good", "OK", "Good", "Very good", "Exceptionally good"]
    semesterkoder = {
      'H': 'autumn',
      'V': 'spring'
    };
  }


  $('.fui_vurdering').each(function (i, div) {
    var _this = $(this)
    var emnekode = _this.data('emnekode');
    var emnedata = $("#emnedata").html()

    if (emnekode == "AVERAGE_SCORE") {
      emnedata = []
      for (var key in avg_score)
        emnedata.push([key, avg_score[key]])
    } else if (!emnedata) {
      console.log('ingen data for emnekode "' + emnekode + '"');
      return;
    } else {
      emnedata = JSON.parse(emnedata)
    }

    var emne_semester = $.map(emnedata, function (value, key) {
      return value[0];
    });
    var emne_vurdering = $.map(emnedata, function (value, key) {
      return value[1];
    });
    var avg_vurdering = $.map(emnedata, function (value, key) {
      return avg_score[value[0]];
    });

    var title = '';
    var semesterstreng = semesterkoder[('' + emne_semester[0]).substring(0, 1)];
    var div = $('<div />')

    if (semesterstreng) {
      title = title_prefix + semesterstreng + ' ' + emne_semester[0].substring(1);
      _this.html('<h2>' + title + '</h2>');
    }

    _this.append(div)
    div.highcharts({
      title: null,
      xAxis: {
        categories: emne_semester
      },
      yAxis: {
        allowDecimals: false,
        min: 1,
        max: 6,
        title: null,
        opposite: false,
        tickInterval: 1,
        labels: {
          formatter: function () {
            return vurdering[this.value - 1];
          }
        },
        plotLines: [{
          value: 0,
          width: 1,
          color: '#808080'
        }]
      },
      tooltip: {
        enabled: false
      },
      legend: {
                                layout: 'vertical',
        enabled: emnekode != 'AVERAGE_SCORE'
      },
      credits: {
        enabled: false
      },
      exporting: {
        enabled: false
      },
        plotOptions: {
            series: {
                animation: false
            }
        },
      series: [{
        name: emnekode,
        data: emne_vurdering,
        zIndex: 2
      }, {
        data: avg_vurdering,
        name: 'Gjennomsnitt på Ifi',
        marker: {
          enabled: false
        },
        dashStyle: 'dot',
        zIndex: 1,
        visible: emnekode != 'AVERAGE_SCORE'
      }]

    });
  });
});
