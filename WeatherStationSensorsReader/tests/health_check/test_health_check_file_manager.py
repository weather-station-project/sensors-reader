import json
import os
import unittest
from collections import OrderedDict
from unittest import mock

from health_check.health_check_file_manager import FILE_NAME, register_error_in_health_check_file, register_success_for_class_into_health_check_file, \
    erase_health_check_file, get_error_messages, HEALTH_CHECK_CLASS


class TestHealthCheckFileManager(unittest.TestCase):
    def setUp(self):
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)

    def tearDown(self):
        if os.path.exists(FILE_NAME):
            os.remove(FILE_NAME)

    @mock.patch('health_check.health_check_file_manager.logging')
    def test_when_registering_error_expected_content_should_be_stored(self, mock_logging):
        # arrange
        test_key1 = 'test_key1'
        test_message1 = 'test_message1'
        test_key2 = 'test_key2'
        test_message2 = 'test_message2'

        # act
        register_error_in_health_check_file(key=test_key1, message=test_message1)
        register_error_in_health_check_file(key=test_key2, message=test_message2)

        # assert
        with open(file=FILE_NAME, mode='r') as fs:
            file_content = json.loads(s=fs.read(), object_pairs_hook=OrderedDict)
            self.assertEqual(file_content, {test_key1: test_message1,
                                            test_key2: test_message2})

        mock_logging.debug.assert_any_call(msg=f'[{HEALTH_CHECK_CLASS}] Health check registered with key "{test_key1}" and message "{test_message1}".')
        mock_logging.debug.assert_any_call(msg=f'[{HEALTH_CHECK_CLASS}] Health check registered with key "{test_key2}" and message "{test_message2}".')

    @mock.patch('health_check.health_check_file_manager.logging')
    def test_when_registering_success_expected_content_should_be_stored(self, mock_logging):
        # arrange
        test_key1 = 'test_key1'
        test_key2 = 'test_key2'
        with open(file=FILE_NAME, mode='w') as fw:
            json.dump(obj={test_key1: 'test_message1',
                           test_key2: 'test_message2'}, fp=fw)

        # act
        register_success_for_class_into_health_check_file(class_name=test_key1)

        # assert
        with open(file=FILE_NAME, mode='r') as fs:
            file_content = json.loads(s=fs.read(), object_pairs_hook=OrderedDict)
            self.assertEqual(file_content, {test_key2: 'test_message2'})

        mock_logging.debug.assert_any_call(msg=f'[{HEALTH_CHECK_CLASS}] Health check successful registered for class name "{test_key1}".')

    @mock.patch('health_check.health_check_file_manager.logging')
    def test_when_registering_success_expected_given_non_existing_file_should_not_exist(self, mock_logging):
        register_success_for_class_into_health_check_file(class_name='test')

        # assert
        mock_logging.debug.assert_not_called()
        self.assertFalse(os.path.exists(FILE_NAME))

    @mock.patch('health_check.health_check_file_manager.logging')
    def test_when_registering_success_given_non_existing_class_nothing_be_stored(self, mock_logging):
        # arrange
        test_key1 = 'test_key1'
        test_key2 = 'test_key2'
        with open(file=FILE_NAME, mode='w') as fw:
            json.dump(obj={test_key2: 'test_message2'}, fp=fw)

        # act
        register_success_for_class_into_health_check_file(class_name=test_key1)

        # assert
        with open(file=FILE_NAME, mode='r') as fs:
            file_content = json.loads(s=fs.read(), object_pairs_hook=OrderedDict)
            self.assertEqual(file_content, {test_key2: 'test_message2'})

        mock_logging.debug.assert_not_called()

    def test_when_erasing_health_check_file_it_should_be_erased(self):
        # arrange
        with open(file=FILE_NAME, mode='w') as fw:
            json.dump(obj={'test_key1': 'test_message1'}, fp=fw)

        # act
        erase_health_check_file()

        # assert
        self.assertFalse(os.path.exists(FILE_NAME))

    def test_when_getting_error_messages_given_non_existing_file_empty_array_should_be_returned(self):
        self.assertFalse(get_error_messages())

    def test_when_getting_error_messages_given_existing_file_empty_array_should_be_returned(self):
        # arrange
        test_key1 = 'test_key1'
        test_key2 = 'test_key2'
        with open(file=FILE_NAME, mode='w') as fw:
            json.dump(obj={test_key1: 'test_message1',
                           test_key2: 'test_message2'}, fp=fw)

        # act
        self.assertEqual('\n'.join(['test_message1', 'test_message2']), get_error_messages())


if __name__ == '__main__':
    unittest.main()
