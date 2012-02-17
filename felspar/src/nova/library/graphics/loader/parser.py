'''
Created on Feb 16, 2012

@author: Patrick
'''
from java.awt import Dimension
class Parser(object):
    
    def parseDimension(self,text):
        a = text.split("x");
        return Dimension(int(a[0].strip()),int(a[1].strip()));