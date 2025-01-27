import sys
import traceback
from unittest import TestCase

from serialzy.registry import DefaultSerializerRegistry
from tests.rich_env.serializers.utils import serialize_and_deserialize


def throw_exception():
    raise TypeError("test")


class ExceptionSerializationTests(TestCase):
    def setUp(self):
        self.registry = DefaultSerializerRegistry()

    def test_exception_serialization(self):
        original_traceback = None
        exception = None
        try:
            throw_exception()
        except TypeError as e:
            original_traceback = e.__traceback__
            exception = sys.exc_info()

        serializer = self.registry.find_serializer_by_type(TypeError)
        self.assertFalse(serializer.stable())
        self.assertIn('cloudpickle', serializer.meta())

        deserialized = serialize_and_deserialize(serializer, exception)
        self.assertEqual(TypeError, type(deserialized[1]))
        self.assertEqual(("test",), deserialized[1].args)
        current_traceback = traceback.extract_tb(deserialized[2])
        length = len(current_traceback)
        original_extracted = traceback.extract_tb(original_traceback)[-length:]
        self.assertEqual(original_extracted, current_traceback)
