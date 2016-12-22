from xml.dom import minidom

from lib.snips.alert import Log


class Plist(object):
    def __init__(self):
        impl = minidom.getDOMImplementation()
        doct = impl.createDocumentType(
            'plist', '-//Apple//DTD PLIST 1.0//EN',
            'http://www.apple.com/DTDs/PropertyList-1.0.dtd'
        )
        self.tree = impl.createDocument(None, 'plist', doct)
        self.tree.documentElement.setAttribute('version', '1.0')

        self.log = Log.get(__name__, self.__class__.__name__)

    def _append(self, *nodes, parent):
        parent = parent if parent else self.tree.documentElement
        for node in nodes:
            parent.appendChild(node)

    def gen_node(self, name):
        return self.tree.createElement(name)

    def gen_text(self, name, content):
        node = self.gen_node(name)
        self._append(self.tree.createTextNode(str(content)), parent=node)
        return node

    def _raw_pair(self, key, *nodes, parent):
        if key is None:
            self.log.error('empty key: {} for {}', key, nodes)
        self._append(self.gen_text('key', key), *nodes, parent=parent)

    def pair_string(self, key, value, parent):
        node = self.gen_text('string', value)
        self._raw_pair(key, node, parent=parent)

    def pair_integer(self, key, value, parent):
        node = self.gen_text('integer', value)
        self._raw_pair(key, node, parent=parent)

    def pair_bool(self, key, value, parent):
        node = self.gen_node('true' if value else 'false')
        self._raw_pair(key, node, parent=parent)

    def select(self, elem):
        for inst, func in [
                (bool, self.pair_bool),
                (dict, self.pair_dict),
                (int, self.pair_integer),
                (list, self.pair_array),
                (str, self.pair_string),
        ]:
            if isinstance(elem, inst):
                return func
        self.log.warning('uncovered type {} for  {}', type(elem), elem)

    def pair_dict(self, key, values, parent=None):
        node = self.gen_node('dict')
        if key is None:
            self._append(node, parent=parent)
        else:
            self._raw_pair(key, node, parent=parent)
        for elem, content in sorted(values.items()):
            func = self.select(content)
            func(elem, content, parent=node)

    def pair_array(self, key, values, parent):
        node = self.gen_node('array')
        if key is None:
            self._append(node, parent=parent)
        else:
            self._raw_pair(key, node, parent=parent)
        for content in values:
            func = self.select(content)
            func(None, content, parent=node)

    def __call__(self, content):
        self.pair_dict(None, content, parent=None)
        return self.tree.toprettyxml(
            encoding='UTF-8', indent='\t'
        ).decode('UTF-8')
