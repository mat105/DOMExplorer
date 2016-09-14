import xml.dom.minidom
import xml.sax

class DomWriter():

    def push(self, node, attrs, text=""):
        x = self.file.createElement(node)

        if len(text) > 0:
            y = self.file.createTextNode(text)
            x.appendChild(y)

        for k, v in attrs.items():
            x.setAttribute( k, v )

        self.last_node[-1].appendChild( x )

        return x

    def push_child(self, node, attrs, text=""):
        self.last_node.append( self.push(node, attrs, text) )       

    def pop(self):
        if len(self.last_node) > 0:
            self.last_node.pop()

    def show(self):
        file_handle = open("domdata.xml","w")
        file_handle.write( self.file.toprettyxml() )
        file_handle.close()

    def __init__(self):
        self.file = xml.dom.minidom.Document()
        self.last_node = [self.file] # Nodos visitados


class SaxReader(xml.sax.handler.ContentHandler):
    WAITING = 0
    PROPERTIES = 1
    PROPERTY = 2

    def __init__(self):
        self.dom_write = DomWriter()
        self.buffer = []
        
        self.state = SaxReader.WAITING
        self.data = None
        self.attrs = None

    def characters(self, content):
        self.buffer.append(content)

    def startElement(self, name, attrs):
        self.buffer = []

        if self.state == SaxReader.WAITING and name == "rentalProperties":
            self.state = SaxReader.PROPERTIES
            self.dom_write.push_child( name, attrs )
        elif self.state == SaxReader.PROPERTIES and name == "property":
            self.state = SaxReader.PROPERTY
            self.data = {}
            self.attrs = attrs
        elif self.state == SaxReader.PROPERTY:
            self.data[name] = [attrs, ""]

    def endElement(self, name):
        text = ''.join(self.buffer)
        text = text.strip()

        if self.state == SaxReader.PROPERTY: # Termino una propiedad
            if name == "property":
                ats = { "type" : self.data["type"][1], "rent" : self.data["price"][1] }

                self.dom_write.push_child( "property", ats, "" )

                self.dom_write.push( "id", {}, self.attrs["id"] )

                self.dom_write.push_child( "address", {"zipCode" : self.data["zipcode"][1]}, "" )
                self.dom_write.push("street", {}, self.data["street"][1])
                self.dom_write.push("streetNo", {}, self.data["streetNo"][1])
                self.dom_write.push("state", {}, self.data["state"][1])

                self.dom_write.pop()

                self.dom_write.push("numberOfBedrooms", {}, self.data["numberOfBedrooms"][1])
                self.dom_write.push("numberofBathrooms", {}, self.data["numberOfBathrooms"][1])
                self.dom_write.push("garage", {}, self.data["garage"][1])

                self.dom_write.pop()
                
                self.state = SaxReader.PROPERTIES
            else:
                self.data[name][1] = text

        elif self.state != SaxReader.PROPERTY:
            self.dom_write.pop()


def main():
    parser = xml.sax.make_parser()
    handler = SaxReader()

    parser.setContentHandler(handler)
    parser.parse( open( "saxdata.xml" ) )

    handler.dom_write.show()


if __name__ == '__main__':
    main()