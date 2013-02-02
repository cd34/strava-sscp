<!doctype html>
<html ng-app="sscp" ng-controller="MainCtrl">
  <head>
    <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
    <script src="/static/bootstrap/js/bootstrap.min.js"></script>
    <script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.4/angular.min.js"></script>
    <script type="text/javascript" src="/static/app.js"></script>
    <script src="/static/d3.v3.min.js"></script>
    <title>${self.title()}</title>
    <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
    <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon" />
    <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css"/>
    <link href="/static/d3.css" rel="stylesheet" type="text/css"/>
<style type="text/css">
  .table tr td.textright {text-align:right};
</style>
<script type="text/javascript">
$('.dropdown-toggle').dropdown()
</script>
  </head>
  <body>
<%include file="header.mako" />
<div class="container">
<div ng-view></div>
</div>
  </body>
</html>

<%def name="title()">
</%def>
