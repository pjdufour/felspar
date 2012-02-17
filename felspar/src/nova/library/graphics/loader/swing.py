'''
Created on Feb 16, 2012

@author: Patrick
'''
from nova.library.graphics.loader.loader import FelsparLoader

from java.awt import Color

class JButton(object):

    def load(self,game,dialog,node,text,align):
        c = JButton(text)
        if node.hasAttribute("enabled"): c.setEnabled(node.getAttribute("enabled")=="true");
        return c


class JLabel(object):

    def load(self,game,dialog,node,text,align):
        c = JLabel(text,align)
        return c
        
        
class JPanel(object):
    
    def load(self,game,dialog,node,text,align):
        c = JPanel()
        c.setBackground(Color.BLACK)
        layout = FelsparLoader.createLayoutManager(c,node.getAttribute("layout") if node.hasAttribute("layout") else "flow")
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
                    c.add(FelsparLoader.compileComponent(game,dialog,child),FelsparLoader.getGridBagConstraints(game,child))
                else:
                    c.add(FelsparLoader.compileComponent(game,dialog,child))
                    
        return c
    







                    
                    