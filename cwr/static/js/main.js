/* Chrome Web Store Rank
 */

(function() {
  
  var plotChart = function() {
    
    nv.addGraph(function () {
        var chart = nv.models.lineChart()
            .x(function(d){
                return new Date(d[0]);
            })
            .y(function(d){
                return d[1];
            })
            .useInteractiveGuideline(true);

        chart.xAxis
            .axisLabel('Days')
            .tickFormat(function (d) {
                return d3.time.format('%x')(new Date(d));
            })
            ;

        chart.yAxis
            .axisLabel('Position')
            .tickFormat(function (d) {
                return d;
            });

        d3.select('#chart svg')
            .datum(CHART_DATA)
            .transition().duration(500)
            .call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
    });
    
  };
  
  // TODO use pjax to load the chart
  // and toggle the hide-show chart class when submitting
  
  var init = function() {
    
    $(document).ready(plotChart);
    
  };
  
  init();
  
}());


