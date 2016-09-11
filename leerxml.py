import xml.dom.minidom


class DOMExplorer():

    def id_transform(self, kind):
        if kind == xml.dom.minidom.Node.ELEMENT_NODE:
            return 0
        elif kind == xml.dom.minidom.Node.COMMENT_NODE:
            return 1
        
        return -1

    def show(self):
        root = self.file.childNodes
        data = ["Nodo: ", "Comentario: "]

        lis = []
        lis.extend(root)

        while len(lis) > 0:
            node = lis.pop()
            add = []
            #add.extend(node.attributes)
            add.extend(node.childNodes)
            add.reverse()

            lis.extend(add)

            #print(node)

            id = self.id_transform(node.nodeType)
            if id>=0:
                print( data[id], node.localName or node.nodeValue )

                if id == 0 and node.hasAttributes():
                    for k, v in node.attributes.items():
                        print("Atributo: ", k, " valor: ", v )





    def __init__(self, name):
        self.file = xml.dom.minidom.parse(name)


def main():
    DOMExplorer("datos.xml").show()

main()