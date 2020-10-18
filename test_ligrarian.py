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


class TestUserInfo:
    """Test user_info returns, prompts for and calls with the right values."""

    @mock.patch('ligrarian.get_setting')
    def test_set_user_info_returned(self, mocked_get):
        """If email and password set then return them."""
        mocked_get.side_effect = ['email', 'password', True]
        values = ligrarian.user_info()
        assert values == ('email', 'password')

    @mock.patch('ligrarian.input')
    @mock.patch('ligrarian.get_setting')
    def test_email_input(self, mocked_get, mocked_in):
        """No email set prompts for it and returns."""
        mocked_get.side_effect = ['', 'pass', False]
        mocked_in.side_effect = ['inputted email', 'y']
        values = ligrarian.user_info()
        assert values == ('inputted email', 'pass')

    @mock.patch('ligrarian.input')
    @mock.patch('ligrarian.get_setting')
    def test_password_input(self, mocked_get, mocked_in):
        """No password set prompts for it and returns."""
        mocked_get.side_effect = ['email', '', False]
        mocked_in.side_effect = ['inputted pass', 'y']
        values = ligrarian.user_info()
        assert values == ('email', 'inputted pass')

    @mock.patch('ligrarian.input')
    @mock.patch('ligrarian.get_setting')
    def test_prompt_true_no_input(self, mocked_get, mocked_in):
        """No input prompt if prompt is set to False."""
        mocked_get.side_effect = ['email', '', False]
        mocked_in.return_value = 'inputted pass'
        ligrarian.user_info()
        mocked_in.assert_called_once()

    @mock.patch('ligrarian.input')
    @mock.patch('ligrarian.get_setting')
    def test_prompt_true_prompt_save(self, mocked_get, mocked_in):
        """Input prompt if prompt set to True."""
        mocked_get.side_effect = ['email', '', True]
        mocked_in.side_effect = ['inputted pass', 'yes']
        ligrarian.user_info()
        last_call = mocked_in.call_args_list[-1][0][0]
        assert "Save" in last_call

    @mock.patch('ligrarian.write_config')
    @mock.patch('ligrarian.input')
    @mock.patch('ligrarian.get_setting')
    def test_save_writes_password(self, mocked_get, mocked_in, mocked_write):
        """Password should be saved is prompted answer is y."""
        mocked_get.side_effect = ['email', '', True]
        mocked_in.side_effect = ['inputted pass', 'y']
        ligrarian.user_info()
        mocked_write.assert_called_once_with('email', 'inputted pass', True)

    @mock.patch('ligrarian.write_config')
    @mock.patch('ligrarian.input')
    @mock.patch('ligrarian.get_setting')
    def test_save_no_does_not_write_password(self, mocked_get,
                                             mocked_in, mocked_write):
        """No password should be saved if prompted answer is n."""
        mocked_get.side_effect = ['email', '', True]
        mocked_in.side_effect = ['inputted pass', 'n', 'n']
        ligrarian.user_info()
        mocked_write.assert_called_once_with('email', '', True)

    @mock.patch('ligrarian.write_config')
    @mock.patch('ligrarian.input')
    @mock.patch('ligrarian.get_setting')
    def test_disable_prompt_y(self, mocked_get, mocked_in, mocked_write):
        """Prompt set to False if disabled prompt answered with y."""
        mocked_get.side_effect = ['email', '', True]
        mocked_in.side_effect = ['inputted pass', 'n', 'y']
        ligrarian.user_info()
        mocked_write.assert_called_once_with('email', '', False)

    @mock.patch('ligrarian.write_config')
    @mock.patch('ligrarian.input')
    @mock.patch('ligrarian.get_setting')
    def test_disable_prompt_n(self, mocked_get, mocked_in, mocked_write):
        """Prompt set to True if disabled prompt answered with n."""
        mocked_get.side_effect = ['email', '', True]
        mocked_in.side_effect = ['inputted pass', 'n', 'n']
        ligrarian.user_info()
        mocked_write.assert_called_once_with('email', '', True)

















