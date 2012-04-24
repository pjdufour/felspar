Jython Swing/JOGL GUI Loader
===

### Description

This loader can read in an xml file and convert the xml to Java Swing components (including GLCanvas).  Each dialog and GLCanvas specified are loaded on read; however, they are not "compiled".  Dialog, GLCanvas, and other components can be activated/deactivated programatically to save memory and cpu time.  Although targeted for use with the compatible GUI framework, the code can easily be distilled to just support Swing.

### Features

 - Convert XML to Swing with Jython
 - Support for GLCanvas (JOGL)

### Example


### To build:

Dependencies:

- [tecolote](https://github.com/pjdufour/tecolote)
- JOGL
- Jython
