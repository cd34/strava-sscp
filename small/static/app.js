var sscp = angular.module('sscp', []).
  config(['$routeProvider', '$locationProvider', 
    function($routeProvider, $locationProvider) {
      $locationProvider.hashPrefix('!');
      $routeProvider.
        when('/', {templateUrl: 'static/partials/index.html'}).
        when('/:id', {templateUrl: 'static/partials/club.html', 
          controller: ClubCtrl}).
        when('/:id/:lastmonth', {templateUrl: 'static/partials/club.html', 
          controller: ClubCtrl}).
        otherwise({redirectTo: '/'});
  }]).filter('meters_feet', function () {
    return function (distance, measurement) {
      return meters_in_feet(distance, measurement);
    };
  }).filter('meters_km_miles', function () {
    return function (distance, measurement) {
      return meters_km_miles(distance, measurement);
    };
  });

function MainCtrl($scope, $http) {
  $scope.master= {};

  $scope.update = function(submitted) {
    $scope.master= angular.copy(submitted);
    if (submitted.match(/^[0-9]+$/)) {
      window.location = '#!/' + submitted;
    } else {
      clubname = submitted;
      if (submitted.match(/^http/)) {
// http://app.strava.com/clubs/bike-commuter-cabal
        clubname = submitted.match(/http:\/\/app.strava.com\/clubs\/(.*)$/)[1].replace(/-/g,' ');
      }
      $http.post('/clubname', $.param({'clubname':clubname}),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'}})
        .success(function(data, status, headers, config) {
          if (data.data.length == 1) {
            window.location = '#!/' + data.data[0]['id'];
          } else {
            $scope.clublist = data.data;
            var element = angular.element('#clubs');
            element.modal('show');
          }
        });
    }
  }; 
}

function ClubCtrl($scope, $routeParams, $http) {
  $scope.$watch('predicate', function(predicate) {
    $scope.$watch('measurement', function(measurement) {
      $scope.$watch('member_data', function(member_data) {
        create_chart(predicate, member_data, $scope.measurement);
      });
    });
  });

  var element = angular.element('#loading');
  element.modal('show');

  url = '/json/' + $routeParams['id'];
  if ($routeParams['lastmonth']) {
    url += '/lastmonth';
  }
  $http.get(url).success(function(data, status, headers, config) {
    $scope.member_data = data.member_data;
    $scope.club_data = data.club_data;
    element.modal('hide');
  });
}

function create_chart(predicate, member_data, measurement) {
  if (predicate[0] == '-') {
    predicate = predicate.substr(1);
  }
  // elevation | avg_elevation = pie chart
  // wattage = line
  // distance | ride | commute | trainer = stacked bar

  var width = 700, height = 570, margin = 60;
  d3.select("svg").remove();

  switch(predicate) {
    case 'elevation':
    case 'avg_elevation':
      //pie_chart(member_data, 'elevation');
      bar_chart(member_data, 'elevation', measurement);
      break;
    case 'wattage':
      bar_chart(member_data, 'wattage');
      break;
    case 'total_distance':
    case 'ride':
    case 'commute':
    case 'trainer':
      stacked_bar_chart(member_data, measurement);
      break;
  }
}

function meters_km_miles(distance, system) {
  if (system == 'imperial') {
    // convert meters to miles
    return distance * 0.000621371;
  } else {
    return distance / 1000;
  }
}

function meters_in_feet(distance, system) {
  if (system == 'imperial') {
    // convert meters to feet
    return distance * 3.28084;
  } else {
    return distance;
  }
}

function stacked_bar_chart(member_data, measurement) {
  if (member_data) {
    var margin = {top: 20, right: 20, bottom: 30, left: 60},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
      .rangeRound([height, 0]);

    var color = d3.scale.ordinal()
      .range(["#ff9", "#f99", "#39f"]);

    var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

    var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .tickFormat(d3.format(".2s"));

    var svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    data = new Array();
    member_data.forEach(function(d) {
      if (d.total_distance > 0) {
        data.push({'Rider':d.name, 
          'Commute':meters_km_miles(d.commute, measurement), 
          'Trainer':meters_km_miles(d.trainer, measurement),
          'Ride':meters_km_miles(d.ride, measurement)});
        }
    });

    color.domain(d3.keys(data[0]).filter(function(key) { return key !== "Rider"; }));

    data.forEach(function(d) {
      var y0 = 0;
      d.distances = color.domain().map(function(name) { return {name: name, y0: y0, y1: y0 += +d[name]}; });
      d.total = d.distances[d.distances.length - 1].y1;
    });

    data.sort(function(a, b) { return b.total - a.total; });

    x.domain(data.map(function(d) { return d.Rider; }));
    y.domain([0, d3.max(data, function(d) { return d.total; })]);

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", -50)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Distance");

    var rider = svg.selectAll(".rider")
      .data(data)
      .enter().append("g")
      .attr("class", "g")
      .attr("transform", function(d) { return "translate(" + x(d.Rider) + ",0)"; });

    rider.selectAll("rect")
      .data(function(d) { return d.distances; })
      .enter().append("rect")
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.y1); })
      .attr("height", function(d) { return y(d.y0) - y(d.y1); })
      .style("fill", function(d) { return color(d.name); });

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .selectAll("text")
        .attr("transform", function(d) {
          return "translate(-15, -60) rotate(-90)"
        });

    var legend = svg.selectAll(".legend")
      .data(color.domain().slice().reverse())
      .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

    legend.append("rect")
      .attr("x", width - 18)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", color);

    legend.append("text")
      .attr("x", width - 24)
      .attr("y", 9)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .text(function(d) { return d; });
  }
}

function bar_chart(member_data, key, measurement) {
  if (member_data) {
    data = member_data.filter(function (d) {
      if (d[key]) { 
        if (key == 'elevation') { 
          d.elevationgain = meters_in_feet(d.elevation, measurement);
          return d; 
        } else {
          return d; 
        }
      }
    });
    if (key == 'elevation') { 
      key = 'elevationgain';
    }
    data.sort(function(a, b) { return b[key] - a[key]; });

    var margin = {top: 20, right: 20, bottom: 30, left: 70},
      width = 960 - margin.left - margin.right,
      height = 500 - margin.top - margin.bottom;

    var x = d3.scale.ordinal()
      .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
      .range([height, 0]);

    var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");

    var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left");

    var svg = d3.select("body").append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    x.domain(data.map(function(d) { return d.name; }));
    y.domain([0, d3.max(data, function(d) { return d[key]; })]);

    svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
      .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", -65)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text(key.charAt(0).toUpperCase() + key.slice(1));

    svg.selectAll(".bar")
      .data(data)
      .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.name); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { 
          return y(d[key]); 
      })
      .attr("height", function(d) { return height - y(d[key]); });

    svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
      .style('text-anchor', 'start')
      .selectAll("text")
        .attr("transform", function(d) {
          return "translate(-15, -60) rotate(-90)"
        });
  }
}
