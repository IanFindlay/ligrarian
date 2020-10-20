#!/usr/bin/env python3

import pytest
import unittest.mock as mock

import ligrarian


class TestCreateDriver:
    """Test function creates appropriate driver and message.

    Testing of the webdriver object is done via capturing the call arguments
    to a mocked webdriver. A call with no arguments is indicative of the
    default, non-headless webdriver.
    """

    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_driver(self, mocked_driver):
        """Headless False should create non-headless (no call args) driver."""
        ligrarian.create_driver(False)
        assert mocked_driver.call_args == ''

    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_headless_driver(self, mocked_driver):
        """Headless True should create headless (call args) driver."""
        ligrarian.create_driver(True)
        assert mocked_driver.call_args != ''

    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_driver_message(self, mocked_driver, capsys):
        """Headless False should print non-headless message."""
        ligrarian.create_driver(False)
        captured_stdout = capsys.readouterr()[0]
        assert "headless" not in captured_stdout

    @mock.patch('ligrarian.webdriver.Firefox')
    def test_create_driver_headless_message(self, mocked_driver, capsys):
        """Headless True should print headless message."""
        ligrarian.create_driver(True)
        captured_stdout = capsys.readouterr()[0]
        assert "headless" in captured_stdout


class TestRetrieveSettings:
    """Test function opens .ini and retrieves and processes values right."""

    @mock.patch('ligrarian.configparser.ConfigParser')
    def test_retrieve_reads(self, mock_parser):
        """Should read settings.ini."""
        ligrarian.retrieve_settings()
        mock_parser.return_value.read.assert_called_once_with('settings.ini')

    @mock.patch('ligrarian.configparser.ConfigParser')
    def test_returns_string_values(self, mock_parser):
        """Should return a string value."""
        mock_parser.return_value.sections.return_value = ['test']
        mock_parser.return_value.items.return_value = [('key', 'value')]
        settings = ligrarian.retrieve_settings()
        assert settings == {'key': 'value'}

    @mock.patch('ligrarian.configparser.ConfigParser')
    def test_returns_boolean_values(self, mock_parser):
        """Should return a boolean value if key is prompt or headless."""
        mock_parser.return_value.sections.return_value = ['test']
        mock_parser.return_value.items.return_value = [('prompt', 'True')]
        settings = ligrarian.retrieve_settings()
        assert settings == {'prompt': True}


class TestCheckAndPromptForEmailPassword:
    """Test function returns, prompts for and calls with the right values."""

    @mock.patch('ligrarian.input')
    def test_no_email_input_if_set(self, mock_input):
        """If email set don't prompt for it."""
        mock_settings = {'email': 'email', 'password': '', 'prompt': True}
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call('Email: ') not in mock_input.call_args_list

    @mock.patch('ligrarian.input')
    def test_input_for_email_if_not_set(self, mock_input):
        """If email is not set then prompt for it."""
        mock_settings = {'email': '', 'password': 'pass', 'prompt': True}
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call('Email: ') in mock_input.call_args_list

    @mock.patch('ligrarian.input')
    def test_inputted_email_saved_to_settings_dict(self, mock_input):
        """Inputted email saved to settings dict."""
        mock_settings = {'email': '', 'password': 'pass', 'prompt': True}
        mock_input.return_value = 'inputted email'
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock_settings['email'] == 'inputted email'

    @mock.patch('ligrarian.input')
    def test_no_password_input_if_set(self, mock_input):
        """If password set don't prompt for it."""
        mock_settings = {'email': '', 'password': 'pass', 'prompt': True}
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call('Password: ') not in mock_input.call_args_list

    @mock.patch('ligrarian.input')
    def test_password_input_if_set(self, mock_input):
        """If password is not set then prompt for it."""
        mock_settings = {'email': 'email', 'password': '', 'prompt': True}
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call('Password: ') in mock_input.call_args_list

    @mock.patch('ligrarian.input')
    def test_no_save_input_if_prompt_false(self, mock_input):
        """If password is not set and prompt False then no 'Save' input."""
        mock_settings = {'email': '', 'password': '', 'prompt': False}
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call(
                'Save Password?(y/n): ') not in mock_input.call_args_list

    @mock.patch('ligrarian.input')
    def test_save_input_if_prompt_true(self, mock_input):
        """If password is not set and prompt True then 'Save' input."""
        mock_settings = {'email': '', 'password': '', 'prompt': True}
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call('Save Password?(y/n): ') in mock_input.call_args_list

    @mock.patch('ligrarian.input')
    def test_password_saved_if_save_y(self, mock_input):
        """Password saved to settings dictionary if 'Save' 'y'."""
        mock_settings = {'email': 'email', 'password': '', 'prompt': True}
        mock_input.side_effect = ['inputted pass', 'y']
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock_settings['password'] == 'inputted pass'

    @mock.patch('ligrarian.input')
    def test_password_not_saved_if_save_n(self, mock_input):
        """Password not saved to settings dictionary if 'Save' 'n'."""
        mock_settings = {'email': 'email', 'password': '', 'prompt': True}
        mock_input.side_effect = ['inputted pass', 'n', 'n']
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock_settings['password'] == ''

    @mock.patch('ligrarian.input')
    def test_prompt_set_to_true_if_disable_y(self, mock_input):
        """Prompt saved as False if disable y."""
        mock_settings = {'email': 'email', 'password': '', 'prompt': True}
        mock_input.side_effect = ['inputted pass', 'n', 'y']
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock_settings['prompt'] == False

    @mock.patch('ligrarian.input')
    def test_prompt_set_to_false_if_disable_n(self, mock_input):
        """Prompt saved as True if disable n."""
        mock_settings = {'email': 'email', 'password': '', 'prompt': True}
        mock_input.side_effect = ['inputted pass', 'n', 'n']
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock_settings['prompt'] == True


class TestWriteInitialConfig:
    """Test function writes config correctly and to the correct file."""

    @mock.patch('ligrarian.open')
    def test_initial_config_opens_settings_file(self, mock_open):
        """Should open settings.ini in write mode."""
        ligrarian.write_initial_config()
        mock_open.assert_called_once_with('settings.ini', 'w')

    @mock.patch('ligrarian.open', new_callable=mock.mock_open())
    def test_initial_config_write(self, mock_open_settings):
        """Should write default config to file.

        ConfigParser writes line by line so checking that a middle call is
        as expected indicats the entire file has been written as desired.
        """
        ligrarian.write_initial_config()
        written_config = mock_open_settings.return_value.__enter__().write
        written_middle = written_config.call_args_list[7][0][0]
        assert written_middle == "headless = False\n"


class TestWriteConfig:
    """Test function writes arguments to correct file."""

    @mock.patch('ligrarian.open')
    def test_write_config_opens_settings_file(self, mock_open):
        """Should open settings.ini in write mode."""
        ligrarian.write_initial_config()
        mock_open.assert_called_once_with('settings.ini', 'w')

    @mock.patch('ligrarian.configparser.ConfigParser')
    @mock.patch('ligrarian.open')
    def test_write_config_email(self, mock_open, mock_parser):
        """ConfigParser.set should be called with argument email."""
        ligrarian.write_config("argument email", "password", "prompt")
        mock_parser.return_value.set.assert_any_call(
                "user", "email", "argument email"
        )

    @mock.patch('ligrarian.configparser.ConfigParser')
    @mock.patch('ligrarian.open')
    def test_write_config_password(self, mock_open, mock_parser):
        """ConfigParser.set should be called with argument password."""
        ligrarian.write_config("email", "argument pass", "prompt")
        mock_parser.return_value.set.assert_any_call(
                "user", "password", "argument pass"
        )

    @mock.patch('ligrarian.configparser.ConfigParser')
    @mock.patch('ligrarian.open')
    def test_write_config_prompt(self, mock_open, mock_parser):
        """ConfigParser.set should be called with argument prompt."""
        ligrarian.write_config("email", "password", "argument prompt")
        mock_parser.return_value.set.assert_any_call(
                "settings", "prompt", "argument prompt"
        )


class TestCategoryAndGenre:
    """Test function returns right category, genre tuple."""

    def test_category_and_genre_nonfiction(self):
        """Nonfiction in shelves should lead to Nonfiction category return."""
        assert ligrarian.category_and_genre(
                ["Genre", "Nonfiction"]) == ("Nonfiction", "Genre")

    def test_category_and_genre_fiction(self):
        """No Nonfiction in shelves should lead to Fiction category return."""
        assert ligrarian.category_and_genre(
                ["No Category", "Genre"]) == ("Fiction", "No Category")

