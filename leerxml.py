import xml.dom.minidom


class DOMExplorer():

    def show(self):
        root = self.file.childNodes

        lis = []
        lis.extend(root)

        while len(lis) > 0:
            node = lis.pop()
            add = []
            add.extend(node.childNodes)
            add.reverse()

            lis.extend(add)

            if node.nodeType == xml.dom.minidom.Node.ELEMENT_NODE:
                print( "Nodo: ", node.nodeName)
                if node.hasAttributes():
                    for k, v in node.attributes.items():
                        print("Atributo: ", k, " valor: ", v )
            elif node.nodeType == xml.dom.minidom.Node.COMMENT_NODE:
                print( "Comentario: ", node.nodeValue )
            elif node.nodeType == xml.dom.minidom.Node.TEXT_NODE:
                if len(str(node.nodeValue).rstrip()) > 0:
                    print( "Texto: ", node.nodeValue )


    def __init__(self, name):
        self.file = xml.dom.minidom.parse(name)


def main():
    DOMExplorer("datos.xml").show()

main()