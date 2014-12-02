#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from lxml import etree
import json


class JsonElement(object):
    def __init__(self, output, parent, tag_name, attrs, text):
        self.output = output
        self.parent = parent
        self.tag_name = tag_name
        self._prepare_print(attrs, text)
        self.has_subtags = False

    def _prepare_print(self, attrs, text):
        if not self.parent:
            self.output.write('{"tags":[')

        self.output.write('{"tag":')
        json.dump(self.tag_name, self.output)
        if attrs:
            self.output.write(',"attrs":')
            json.dump(dict(attrs), self.output)
        if text and text.strip():
            self.output.write(',"text":')
            json.dump(text, self.output)

    def end(self, tag_name):
        assert tag_name == self.tag_name, u'Закрылся не тот тег, что ожидался. Выключили валидацию xml?'
        self._finalize_print()

    def _finalize_print(self):
        if self.has_subtags:
            self.output.write(']')
        self.output.write('}')
        if not self.parent:
            #print start
            self.output.write(']}')

    def new_subtag(self):
        if not self.has_subtags:
            self.output.write(',"subtags":[')
            self.has_subtags = True
        else:
            self.output.write(',')


def parser(output, obj, event, elem):
    if event == 'start':
        if obj:
            obj.new_subtag()
        new_obj = JsonElement(output, obj, elem.tag, elem.attrib, elem.text)
    elif event == 'end':
        obj.end(elem.tag)
        new_obj = obj.parent
    else:
        raise Exception("No such event emplemented {0}".format(event))
    return new_obj

def process_file(input, output):
    context = etree.iterparse(input, events=('end', 'start'))
    cur_object = None
    for event, elem in context:

        cur_object = parser(output, cur_object, event, elem)

        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]

    del context

if __name__ == '__main__':
    process_file(sys.stdin, sys.stdout)