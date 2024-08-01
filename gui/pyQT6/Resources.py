import os
import xml.etree.ElementTree as ET


class Resources:
    def __init__(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        xml_path = os.path.join(script_dir, "resources.xml")
        tree = ET.parse(xml_path)
        root = tree.getroot()
        self.strings = {element.get("name"): element.text for element in root.findall("string")}

    def getString(self,str):
        return self.strings.get(str)
    
    def getString(self,str1,str2):
        return self.strings.get(str1,str2)
        
R = Resources()
