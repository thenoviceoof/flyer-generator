IDEAS
================================================================================

basic idea: 
      user ←→ web framework ←→ google / 2pdf

frameworks:
 - web.py
   - no documentation
   - simple/lightweight
 - cherrypy?
   - simple/lightweight
   - is an HTTP framework (not like PHP, has to run outside)
   - not heavily trafficed, not such a big deal
   - moses hackamura is the documentation
   - can run it on a fucking phone
 - rails
   - heavy
 - django
   - heavy

cherrypy doesn't come with a templating or db engine
 - jinja2/sqlalchemy?

conversion:
 - html2pdf
   - how quirky is the html renderer?
 - html2ps | ps2pdf [?]
 - wkhtml2pdf
   - http://code.google.com/p/wkhtmltopdf/
 - xhtml2pdf
   - quirky?
 - imagemagick (svg)
   - not so great, because output is raster
   - ~5MB outputs for fairly complex sheets at a fair resolutions
 - inkscape (svg2pdf)
   - doesn't come standard on server boxes
   - we'll have to run it on the ADI server, which isn't a bad thing
 - batik (svg)
   - java
   - looks like it just rasterizes?
   - have to test
 - pysvg
   - not much documentation
   - author is obviously not cool (zip?? doc??)
 - svglib (python)
   - comes with an svg2pdf
 - svg2pdf (cairo)
   - seems old, unmaintained
   - http://cgit.freedesktop.org/~cworth/svg2pdf/

Resources
--------------------------------------------------------------------------------

http://stackoverflow.com/questions/1048205/how-to-programmatically-convert-svg-to-pdf-on-windows
http://www.xhtml2pdf.com/
http://pypi.python.org/pypi/svglib/
http://code.google.com/apis/calendar/data/2.0/developers_guide_python.html
http://wiki.python.org/moin/WebFrameworks

conf



TESTS
================================================================================

 - Batik
   - Use rasterizer -m "application/pdf" file
   - does generates vector!
 - Inkscape
   - inkscape --export-pdf=out_file in_file
   - inkscape -A out_file in_file
 - svg2pdf (python)
   - does not have an ubuntu package, used easy_install
   - svg2pdf -o svg2pdf-simple-test.pdf simple-test.svg
   - mangled output, though
 - xhtml2pdf
   - No images
   - CSS not perfect
 - html2ps, ps2pdf
   - oh my god it's horrific
 - wkhtml2pdf
   - works like a charm
   - static, might not need dependencies