TODO
================================================================================

In rough order of what to do...

 - test if svg images give better res than png images
   - generate svg versions of the logo
   - change the template to include the svg
   - compare svg vs png versions of pdf
 - make the fields on the template contentEditable
 - decide if current fields are enough
 - create the style editor
 - add multiple styles
   - need to abstract out the render dialog
   - style editor also needs to be abstracted (or restricted)
   - need interface to choose styles somewhere
 - allow more styles to be added easily
   - ties in with the previous
 - store past PDFs in a directory/track them in a db
   - sqlite, maybe
 - do drafts (db)
   - store meta info (fields) in a draft
 - do auth
   - mostly as prep for the next step
 - add meta-info/hook into auth so interface is open to other clubs

