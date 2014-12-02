#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from lxml import etree
import json


class SubtagElement(object):
    __slots__ = ['output', 'has_subtags']
    def __init__(self, output):
        self.output = output
        self.has_subtags = False

    def add(self):
        if not self.has_subtags:
            self.output.write(',"subtags":[')
            self.has_subtags = True
        else:
            self.output.write(',')

    def end(self):
        if self.has_subtags:
            self.output.write(']')


class JsonElement(object):
    __slots__ = ['output', 'parent', 'tag_name', 'subtags']
    def __init__(self, output, parent, tag_name):
        self.output = output
        self.parent = parent
        self.tag_name = tag_name
        self.subtags = SubtagElement(output)

    def start(self, attrs, text):
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
        self.subtags.end()
        self.output.write('}')

    def new_subtag(self):
        self.subtags.add()


def parser_open(output, obj, elem):
    if obj:
        obj.new_subtag()
    new_obj = JsonElement(output, obj, elem.tag)
    new_obj.start(elem.attrib, elem.text)
    return new_obj

def parser_end(output, obj, elem):
    obj.end(elem.tag)
    return obj.parent

def parser(output, obj, event, elem):
    if event == 'start':
        return parser_open(output, obj, elem)
    elif event == 'end':
        return parser_end(output, obj, elem)

def print_json_skelet_open(output):
    output.write('{"tags":[')

def print_json_skelet_close(output):
    output.write(']}')

def process_file(input, output):
    context = etree.iterparse(input, events=('end', 'start'))
    print_json_skelet_open(output)
    cur_object = None
    for event, elem in context:
        cur_object = parser(output, cur_object, event, elem)
        elem.clear()
        while elem.getprevious() is not None:
            del elem.getparent()[0]
    print_json_skelet_close(output)

if __name__ == '__main__':
    # TODO: подумать над fileinput
    process_file(sys.stdin, sys.stdout)