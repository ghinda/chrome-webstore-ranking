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
                
            // clean-up CHART_DATA labels
            CHART_DATA.forEach(function(item) {
                item.key = JSON.parse(item.key);
                item.key = item.key.hl;
            });

            d3.select('#chart svg')
                .datum(CHART_DATA)
                .transition().duration(500)
                .call(chart);

            nv.utils.windowResize(chart.update);

            return chart;
        });

    };

    // use pjax to load the chart
    // and toggle the hide-show chart class when submitting
    
    var submitForm = function(e) {

        var $body = $('body');
        var $container = $('.chart-container');
        var $form = $('.search-form');
        var formData = $form.serialize();
        var formUrl = $form.attr('action');
        
        var xhr = new XMLHttpRequest();
        xhr.open('POST', formUrl, false);
        xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
        
        xhr.onreadystatechange = function() {
            if(xhr.readyState == 4 && xhr.status == 200) {
                
                var d = new DocumentFragment();
                d.appendChild(document.createElement('div'));
                d.querySelector('div').innerHTML = xhr.responseText;
                
                $container.html(d.querySelector('.chart-container').innerHTML);
                
                $body.addClass('chart--show');
                
                setTimeout(function() {
                    plotChart();
                    
                    $body.removeClass('chart--loading');
                }, 500);
                
            }
        };
        
        $body.addClass('chart--loading');
        
        history.pushState({}, '', formUrl + '?' + formData);
        
        xhr.send(formData);
        
        return false;
        
    };

    var init = function() {

        $(document).ready(plotChart);

        $('.search-form').on('submit', submitForm);

    };

    init();
  
}());


