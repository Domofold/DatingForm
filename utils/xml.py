from io import BytesIO
import xml.etree.ElementTree as ET


class Xml:
    def __init__(self):
        pass

    @staticmethod
    def formToXmlBytes(data):
        root = ET.Element("Forms")
        dateform = ET.Element("form")

        ET.SubElement(dateform, "name", text=data.name)
        ET.SubElement(dateform, "age", text=str(data.age))
        ET.SubElement(dateform, "gender", text=data.gender)
        ET.SubElement(dateform, "dwelling_place", text=data.dwelling_place)
        ET.SubElement(dateform, "hobbies", text=data.hobbies)
        ET.SubElement(dateform, "diet", text=data.diet)
        ET.SubElement(dateform, "email", text=data.email)

        root.append(dateform)
        xml_str = ET.tostring(root, encoding="utf-8", method="xml")
        xml_bytes = BytesIO(xml_str)

        return xml_bytes
