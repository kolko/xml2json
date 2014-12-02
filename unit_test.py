#!/usr/bin/env python
# -*- coding: utf-8 -*-

# TODO: переделать чеки в тестах на сравнение через json
import unittest
from StringIO import StringIO

from xml2json import *


class TestSubtag(unittest.TestCase):
    def test_not_printed(self):
        output = StringIO()
        subtag = SubtagElement(output)
        subtag.end()
        output.seek(0)
        self.assertEqual(output.read(), '')
        output.close()

    def test_empty(self):
        output = StringIO()
        subtag = SubtagElement(output)
        subtag.add()
        subtag.end()
        output.seek(0)
        self.assertEqual(output.read(), ',"subtags":[]')
        output.close()

    def test_simple(self):
        output = StringIO()
        subtag = SubtagElement(output)
        subtag.add()
        subtag.add()
        subtag.add()
        subtag.end()
        output.seek(0)
        self.assertEqual(output.read(), ',"subtags":[,,]')
        output.close()

class TestJsonElement(unittest.TestCase):
    def test_not_printed(self):
        output = StringIO()
        element = JsonElement(output, None, 'test')
        output.seek(0)
        self.assertEqual(output.read(), '')
        output.close()

    def test_simple(self):
        output = StringIO()
        element = JsonElement(output, None, 'test')
        element.start(None, None)
        element.end('test')
        output.seek(0)
        self.assertEqual(output.read(), '{"tag":"test"}')
        output.close()

    def test_wrong_closed_tag(self):
        output = StringIO()
        element = JsonElement(output, None, 'test')
        element.start(None, None)
        self.assertRaises(Exception, element.end, ['not_test'])
        output.close()


if __name__ == '__main__':
    unittest.main()