Swing/JOGL GUI
===

### Description

This loader can read in an xml file and convert the xml to Java Swing components (including GLCanvas).  Each dialog and GLCanvas specified are loaded on read; however, they are not "compiled".  Dialog, GLCanvas, and other components can be activated/deactivated programatically to save memory and cpu time.

### Features

 - Convert XML to Swing with Jython
 - Support for GLCanvas (JOGL)

### Example


### To build:

Dependencies:

- [tecolote](https://github.com/pjdufour/tecolote)
- JOGL
- Jython
