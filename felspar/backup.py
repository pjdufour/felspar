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
from nova.library.utilities import Parser
from java.awt.event import KeyListener
from java.awt import Component
from java.awt.event import KeyEvent


def getChild(tag,node):
    for child in node.childNodes:
        if child.nodeName==tag:
            return child
    return None
def addListeners(game,component,node):
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
        
        bindings = getChild("bindings",node)
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
                                      
def reload_dialog(game,gui,filename,id):
    "@sig public javax.swing.JPanel load(nova.library.core.Game game, nova.library.gui.GUI gui, java.lang.String filename, java.lang.String id)"
    #((javax.swing.plaf.basic.BasicInternalFrameUI)myInternalFrame.getUI()).setNorthPane(null);

    doc = minidom.parse(filename)
    xmlGUI = doc.getElementsByTagName("gui")[0]
    xmlJDialog = None
    for node in xmlGUI.getElementsByTagName("dialog"):
        if(node.getAttribute("id")==id):
            xmlJDialog = node   
            break
    
    settings = game.getSettings();
    res = Parser.parseDimension(settings.getString(Settings.RESOLUTION))
    w = int(xmlJDialog.getAttribute("width")) if node.hasAttribute("width") else -1
    h = int(xmlJDialog.getAttribute("height")) if node.hasAttribute("height") else -1
    
    
    jdialog = JDialog(owner,(xmlJDialog.getAttribute("title") if xmlJDialog.hasAttribute("title") else ""),(xmlJDialog.getAttribute("modal") if xmlJDialog.hasAttribute("modal") else "true")=="true")
    #jdialog.setUndecorated((xmlJDialog.getAttribute("undecorated") if xmlJDialog.hasAttribute("undecorated") else "true")=="true")
    jdialog.setSize((w if w >= 0 else int(res.getWidth())),(h if h >= 0 else int(res.getHeight())))
    jdialog.setDefaultCloseOperation(JDialog.HIDE_ON_CLOSE)
    jdialog.setContentPane(reloadComponent(game,gui,int(xmlJDialog.getAttribute("id")),getChild("jpanel",xmlJDialog)))
    return jdialog

def compile_dialog(dialog,game,filename,id):
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
    dialog.add(reloadComponent(game,dialog,getChild("jpanel",xmlDialog)))
    
def reloadComponent(game,dialog,node):
    c = None
    text = node.getAttribute("text") if node.hasAttribute("text") else ""
    align = int(node.getAttribute("align")) if node.hasAttribute("align") else 0
        
    #Components
    if node.nodeName=="jpanel":
        c = JPanel()
        c.setBackground(Color.BLACK)
        layout = createLayoutManager(c,node.getAttribute("layout") if node.hasAttribute("layout") else "flow")
        c.setLayout(layout)
        c.setOpaque(False)
        
        if node.getAttribute("opaque"):
            c.setOpaque(node.getAttribute("opaque")=="true")
        
        if node.getAttribute("background"):
            if(node.getAttribute("background")=="orange"):
                c.setBackground(Color.ORANGE)
            elif(node.getAttribute("background")=="green"):
                c.setBackground(Color.GREEN)            
            
        for child in node.childNodes:
            if child.nodeName!="#text":
                if node.getAttribute("layout")=="gridbag":
                    c.add(reloadComponent(game,dialog,child),getGridBagConstraints(game,child))
                else:
                    c.add(reloadComponent(game,dialog,child))
                
    elif node.nodeName=="jlabel":
        c = JLabel(text,align)
    elif node.nodeName=="jbutton":
        c = JButton(text)
        if node.hasAttribute("enabled"): c.setEnabled(node.getAttribute("enabled")=="true");
            
    elif node.nodeName=="settingspanel":
        c = SettingsPanel(game)
        for g in node.childNodes:
            if g.nodeName=="group":
                c.addGroup(int(g.getAttribute("id")),g.getAttribute("label"))
                for h in g.childNodes:
                    if h.nodeName=="heading":
                        c.addHeading(int(g.getAttribute("id")),h.getAttribute("label"))
                        for s in h.childNodes:
                            if s.nodeName=="setting":
                                #<setting id="1" name="DISPLAY_REAL_WORLD_TIME" type="checkbox" label="Show Real-World Time"></setting>
                                if s.getAttribute("items")!="":
                                    c.addSettingWithItems(int(g.getAttribute("id")),int(s.getAttribute("id")),s.getAttribute("label"),s.getAttribute("type"),s.getAttribute("items").split(","))
                                else:
                                    c.addSetting(int(g.getAttribute("id")),int(s.getAttribute("id")),s.getAttribute("label"),s.getAttribute("type"))
                                

        c.finalizeSettingsPanel()
        dialog.registerSettingsPanel(int(node.getAttribute("id")),c)
    
    elif node.nodeName=="logspanel":
        c = LogsPanel(game)
        for g in node.childNodes:
            if g.nodeName=="group":
                c.addLog(int(g.getAttribute("id")),g.getAttribute("label"))                          

        c.finalizeLogsPanel()
        dialog.registerLogsPanel(int(node.getAttribute("id")),c)
    
    elif node.nodeName=="nglcanvas":
        c = NGLCanvas(game,int(getCascadingAttribute(game,node,"width")),int(getCascadingAttribute(game,node,"height")))
        dialog.registerCanvas(int(node.getAttribute("id")),c)
    
    #Layout
    if node.parentNode.getAttribute("layout")=="absolute":
        c.setBounds(getBounds(game,node))
    elif node.parentNode.getAttribute("layout")=="box-y":
        c.setAlignmentX(Component.CENTER_ALIGNMENT);
        if node.hasAttribute("width") and node.hasAttribute("height"):
            c.setPreferredSize(Dimension(int(getCascadingAttribute(game,node,"width")),int(getCascadingAttribute(game,node,"height"))))
        if node.hasAttribute("minWidth") and node.hasAttribute("minHeight"):
            c.setMinimumSize(Dimension(int(node.getAttribute("minWidth")),int(node.getAttribute("minHeight"))))
        if node.hasAttribute("maxWidth") and node.hasAttribute("maxHeight"):
            c.setMaximumSize(Dimension(int(node.getAttribute("maxWidth")),int(node.getAttribute("maxHeight"))))
    elif node.parentNode.getAttribute("layout")=="box-x":
        c.setAlignmentY(Component.CENTER_ALIGNMENT);
        if node.hasAttribute("width") and node.hasAttribute("height"):
            c.setPreferredSize(Dimension(int(getCascadingAttribute(game,node,"width")),int(getCascadingAttribute(game,node,"height"))))
        if node.hasAttribute("minWidth") and node.hasAttribute("minHeight"):
            c.setMinimumSize(Dimension(int(node.getAttribute("minWidth")),int(node.getAttribute("minHeight"))))
        if node.hasAttribute("maxWidth") and node.hasAttribute("maxHeight"):
            c.setMaximumSize(Dimension(int(node.getAttribute("maxWidth")),int(node.getAttribute("maxHeight"))))

    if node.nodeName!="nglcanvas" and node.nodeName!="jpanel" and node.nodeName!="settingspanel": addListeners(game,c,node)
    return c;
    
def createLayoutManager(jpanel,sLayout):
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

def getCascadingAttribute(game,node,attr):
    settings = game.getSettings();
    res = Parser.parseDimension(settings.getString(Settings.RESOLUTION))
    
    if node.hasAttribute(attr):
        return node.getAttribute(attr)
    else:
        if node.nodeName=="dialog":
            if(attr=="width"): return str(int(res.getWidth()))
            elif(attr=="height"): return str(int(res.getHeight()))
        else:
            return getCascadingAttribute(game,node.parentNode,attr)

def getBounds(game,n): return Rectangle((int(n.getAttribute("x")) if n.hasAttribute("x") else 0),(int(n.getAttribute("y")) if n.hasAttribute("y") else 0),int(getCascadingAttribute(game,n,"width")),int(getCascadingAttribute(game,n,"height")))

def getGridBagConstraints(game,node):
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
 
 
 
     
        
