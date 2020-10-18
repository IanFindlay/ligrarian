#!/usr/bin/env python3

import unittest.mock as mock
import pytest

import ligrarian


class TestCreateDriver:
    """Test the create_driver function.

    Testing of the webdriver object is done via capturing the call arguments
    to a mocked webdriver. A call with no arguments is indicative of the
    default, non-headless webdriver.
    """

    @mock.patch('ligrarian.get_setting')
    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_driver(self, mocked_driver, mocked_get):
        """Test that headless False results in non-headless driver."""
        mocked_get.return_value = False
        ligrarian.create_driver()
        assert mocked_driver.call_args == ''

    @mock.patch('ligrarian.get_setting')
    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_headless_driver(self, mocked_driver, mocked_get):
        """Test that headless True results in headless driver."""
        mocked_get.return_value = True
        ligrarian.create_driver()
        assert mocked_driver.call_args != ''

    @mock.patch('ligrarian.get_setting')
    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_driver_message(self, mocked_driver, mocked_get, capsys):
        """Test that headless False results in non-headless message."""
        mocked_get.return_value = False
        ligrarian.create_driver()
        captured_stdout = capsys.readouterr()[0]
        assert "headless" not in captured_stdout

    @mock.patch('ligrarian.get_setting')
    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_driver_headless_message(self, mocked_driver,
                                            mocked_get, capsys):
        """Test that headless setting results in headless message."""
        mocked_get.return_value = True
        ligrarian.create_driver()
        captured_stdout = capsys.readouterr()[0]
        assert "headless" in captured_stdout


class TestGetSetting:
    """Test that get_setting calls .get or .getboolean correctly."""

    @mock.patch('configparser.ConfigParser.get')
    def test_get_setting(self, mocked_config):
        ligrarian.get_setting('test', 'arbitrary')
        assert mocked_config.called

    @mock.patch('configparser.ConfigParser.getboolean')
    def test_get_setting_boolean(self, mocked_config):
        ligrarian.get_setting('test', 'arbitrary', boolean=True)
        assert mocked_config.called


















