<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:py="http://genshi.edgewall.org/"
      xmlns:xi="http://www.w3.org/2001/XInclude">
<head>
  <title>${self.title()}</title>
  <meta http-equiv="Content-Type" content="application/xhtml+xml; charset=utf-8" />
  <link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon" />
  <link href="/static/bootstrap/css/bootstrap.min.css" rel="stylesheet" type="text/css"/>
${self.head_js()}
</head>

<body>
<%include file="header.mako" />
<div class="container">
  <div class="row">

<h2>${self.title()}</h2>

${self.body()}

  </div>
</div>

</body>
</html>

<%def name="title()">
</%def>

<%def name="head_js()">
</%def>
