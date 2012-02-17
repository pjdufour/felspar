'''
Created on Feb 16, 2012

@author: Patrick
'''

import os, string, re, java, javax, sys, StringIO
from xml.dom import minidom
from java.awt import Color
from java.awt import FlowLayout
from java.awt import BorderLayout
from java.awt import Rectangle
from java.awt import GridLayout
from java.awt import GridBagLayout
from java.awt import GridBagConstraints
from java.awt import Dimension
from java.awt import Component
from java.awt import Font
from javax.swing import JFrame
from javax.swing import JInternalFrame
from javax.swing import JPanel
from javax.swing import JLabel
from javax.swing import JButton
from javax.swing import JTabbedPane
from javax.swing import BoxLayout
from javax.swing import Box
'''
from nova.library.graphics.novagl import NGLCanvas
from nova.library.core import Game
from nova.library.core import Settings
from nova.library.core import BuiltInCommand
from nova.library.core import PythonCommand
from nova.library.graphics.gui import GUI
from nova.library.graphics.gui import SettingsPanel
from nova.library.graphics.gui import LogsPanel
from nova.library.graphics.gui import CustomKeyListener
from nova.library.graphics.gui import CustomActionListener
from nova.library.graphics.gui import SimpleActionListener
from nova.library.graphics.gui import TulipDialog
'''
from java.awt.event import KeyListener
from java.awt import Component
from java.awt.event import KeyEvent

from nova.library.settings import Settings
from nova.library.graphics.listeners import SimpleActionListener


from nova.library.graphics.loader.swing import JPanel
from nova.library.graphics.loader.swing import JLabel
from nova.library.graphics.loader.swing import JButton
from nova.library.graphics.loader.parser import Parser

class FelsparLoader(object):

    def compileDialog(self,dialog,game,filename,id):
        "@sig public void compile_dialog(nova.library.graphics.gui.TulipDialog dialog, nova.library.core.Game game, java.lang.String filename, java.lang.String id)"
        #print "Compiling Dialog "+id+" from "+filename
        
        doc = minidom.parse(filename)
        xmlGUI = doc.getElementsByTagName("gui")[0]
        xmlDialog = None
        for node in xmlGUI.getElementsByTagName("dialog"):
            if(node.getAttribute("id")==id):
                xmlDialog = node
                break
        
        settings = game.getSettings();
        res = Parser.parseDimension(settings.getString(Settings.RESOLUTION))
        w = int(xmlDialog.getAttribute("width")) if xmlDialog.hasAttribute("width") else -1
        h = int(xmlDialog.getAttribute("height")) if xmlDialog.hasAttribute("height") else -1
        dialog.setDynamicSize(w,h)
        dialog.setBounds(0,0,(w if w >= 0 else int(res.getWidth())),(h if h >= 0 else int(res.getHeight())))
        dialog.add(self.compileComponent(game,dialog,self.getChild("jpanel",xmlDialog)))
    def compileComponent(self,game,dialog,node):
        c = None
        text = node.getAttribute("text") if node.hasAttribute("text") else ""
        align = int(node.getAttribute("align")) if node.hasAttribute("align") else 0
            
        #Components
        if node.nodeName=="jpanel":
            c = JPanel.load(game,dialog,node,text,align)
        elif node.nodeName=="jlabel":
            c = JLabel.load(game,dialog,node,text,align)
            
            
        elif node.nodeName=="jbutton":
            c = JButton.load(self,game,dialog,node,text,align)
            
        elif node.nodeName=="nglcanvas":
            c = NGLCanvas(game,int(self.getCascadingAttribute(game,node,"width")),int(self.getCascadingAttribute(game,node,"height")))
            dialog.registerCanvas(int(node.getAttribute("id")),c)
        
        #Layout
        if node.parentNode.getAttribute("layout")=="absolute":
            c.setBounds(self.getBounds(game,node))
        elif node.parentNode.getAttribute("layout")=="box-y":
            c.setAlignmentX(Component.CENTER_ALIGNMENT);
            if node.hasAttribute("width") and node.hasAttribute("height"):
                c.setPreferredSize(Dimension(int(self.getCascadingAttribute(game,node,"width")),int(self.getCascadingAttribute(game,node,"height"))))
            if node.hasAttribute("minWidth") and node.hasAttribute("minHeight"):
                c.setMinimumSize(Dimension(int(node.getAttribute("minWidth")),int(node.getAttribute("minHeight"))))
            if node.hasAttribute("maxWidth") and node.hasAttribute("maxHeight"):
                c.setMaximumSize(Dimension(int(node.getAttribute("maxWidth")),int(node.getAttribute("maxHeight"))))
        elif node.parentNode.getAttribute("layout")=="box-x":
            c.setAlignmentY(Component.CENTER_ALIGNMENT);
            if node.hasAttribute("width") and node.hasAttribute("height"):
                c.setPreferredSize(Dimension(int(self.getCascadingAttribute(game,node,"width")),int(self.getCascadingAttribute(game,node,"height"))))
            if node.hasAttribute("minWidth") and node.hasAttribute("minHeight"):
                c.setMinimumSize(Dimension(int(node.getAttribute("minWidth")),int(node.getAttribute("minHeight"))))
            if node.hasAttribute("maxWidth") and node.hasAttribute("maxHeight"):
                c.setMaximumSize(Dimension(int(node.getAttribute("maxWidth")),int(node.getAttribute("maxHeight"))))
    
        if node.nodeName!="nglcanvas" and node.nodeName!="jpanel": self.addListeners(game,c,node)
        return c;
    def createLayoutManager(self,jpanel,sLayout):
        if sLayout=="absolute": return None
        elif sLayout=="flow": return FlowLayout()
        elif sLayout=="border": return BorderLayout()
        elif sLayout.startswith("grid-"):#"grid-1x1"
            dim = Parser.parseDimension(sLayout.split("-")[1])
            return GridLayout(int(dim.getWidth()),int(dim.getHeight()))
        elif sLayout.startswith("box-y"):
            return BoxLayout(jpanel,BoxLayout.Y_AXIS)
        elif sLayout.startswith("box-x"):
            return BoxLayout(jpanel,BoxLayout.X_AXIS)
        elif sLayout.startswith("gridbag"):
            return GridBagLayout()
    def getGridBagConstraints(self,game,node):
        c = GridBagConstraints()
        for str in node.getAttribute("constraints").split(","):
            a = str.split(":")
            if a[0]=="fill":
                c.fill = int(a[1])
            elif a[0]=="gridwidth":
                c.gridwidth = int(a[1])
            elif a[0]=="gridheight":
                c.gridheight = int(a[1])
            elif a[0]=="gridx":
                c.gridx = int(a[1])
            elif a[0]=="gridy":
                c.gridy = int(a[1])
            elif a[0]=="weightx":
                c.weightx = int(a[1])
            elif a[0]=="weighty":
                c.weighty = int(a[1])
            else:
                print a[0]+"was not found"
        return c
    def getCascadingAttribute(self,game,node,attr):
        settings = game.getSettings();
        res = Parser.parseDimension(settings.getString(Settings.RESOLUTION))
        
        if node.hasAttribute(attr):
            return node.getAttribute(attr)
        else:
            if node.nodeName=="dialog":
                if(attr=="width"): return str(int(res.getWidth()))
                elif(attr=="height"): return str(int(res.getHeight()))
            else:
                return self.getCascadingAttribute(game,node.parentNode,attr)
    def getBounds(self,game,n): return Rectangle((int(n.getAttribute("x")) if n.hasAttribute("x") else 0),(int(n.getAttribute("y")) if n.hasAttribute("y") else 0),int(self.getCascadingAttribute(game,n,"width")),int(self.getCascadingAttribute(game,n,"height")))
    def getChild(self,tag,node):
        for child in node.childNodes:
            if child.nodeName==tag:
                return child
        return None
    def addListeners(self,game,component,node):
        keylistener = None
        actionlistener = None
        if node.hasAttribute("listeners"):
            for listener in node.getAttribute("listeners").split(","):
                if listener=="key":
                    keylistener = CustomKeyListener()
                    component.addKeyListener(keylistener)
                elif listener=="action":
                    actionlistener = SimpleActionListener()
                    component.addActionListener(actionlistener)
            
            bindings = self.getChild("bindings",node)
            if bindings!=None:
                for binding in bindings.childNodes:
                    if binding.nodeName!="#text":
                        if binding.nodeName=="keyevent":
                            for command in binding.getElementsByTagName("command"):
                                command_type = command.getAttribute("type")
                                if command_type=="builtin":
                                    if(command.hasAttribute("args")):
                                        keylistener.addKeyBinding(int(binding.getAttribute("type")),int(binding.getAttribute("code")),BuiltInCommand(game,command.getAttribute("name"),command.getAttribute("args")))
                                    else:
                                        keylistener.addKeyBinding(int(binding.getAttribute("type")),int(binding.getAttribute("code")),BuiltInCommand(game,command.getAttribute("name"),""))
                                elif command_type=="python":
                                    if(command.hasAttribute("args")):
                                        keylistener.addKeyBinding(int(binding.getAttribute("type")),int(binding.getAttribute("code")),PythonCommand(game,command.getAttribute("file"),command.getAttribute("args")))
                                    else:
                                        keylistener.addKeyBinding(int(binding.getAttribute("type")),int(binding.getAttribute("code")),PythonCommand(game,command.getAttribute("file"),""))
                        elif binding.nodeName=="actionevent":
                            for command in binding.getElementsByTagName("command"):
                                command_type = command.getAttribute("type")
                                if command_type=="builtin":
                                    if(command.hasAttribute("args")):
                                        actionlistener.addCommand(BuiltInCommand(game,command.getAttribute("name"),command.getAttribute("args")))
                                    else:
                                        actionlistener.addCommand(BuiltInCommand(game,command.getAttribute("name"),""))
                                elif command_type=="python":
                                    if(command.hasAttribute("args")):
                                        actionlistener.addCommand(PythonCommand(game,command.getAttribute("file"),command.getAttribute("args")))
                                    else:
                                        actionlistener.addCommand(PythonCommand(game,command.getAttribute("file"),""))
                                          

    def __init__(self):
        '''
        Constructor
        '''
        