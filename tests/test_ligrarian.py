#!/usr/bin/env python3

"""Tests the functions in ligrarian not related to GUI, sheet or goodreads."""

import unittest.mock as mock

import ligrarian


@mock.patch('ligrarian.configparser.ConfigParser')
class TestRetrieveSettings:
    """Test function opens .ini and retrieves and processes values right."""

    def test_retrieve_reads(self, mock_parser):
        """Should read settings.ini."""
        ligrarian.retrieve_settings()
        mock_parser.return_value.read.assert_called_once_with('settings.ini')

    def test_returns_string_values(self, mock_parser):
        """Should return a string value."""
        mock_parser.return_value.sections.return_value = ['test']
        mock_parser.return_value.items.return_value = [('key', 'value')]
        settings = ligrarian.retrieve_settings()
        assert settings == {'key': 'value'}

    def test_returns_boolean_values(self, mock_parser):
        """Should return a boolean value if key is prompt or headless."""
        mock_parser.return_value.sections.return_value = ['test']
        mock_parser.return_value.items.return_value = [('prompt', 'True')]
        settings = ligrarian.retrieve_settings()
        assert settings == {'prompt': True}


class TestGetDateString:
    """Function gets, modifies and returns correct date."""

    def test_today_returned(self):
        """Same as strftime datetime.datetime.now()."""
        formatted_now = ligrarian.dt.strftime(ligrarian.dt.now(), '%d/%m/%Y')
        assert ligrarian.get_date_str() == formatted_now

    def test_yesterday_returned(self):
        """Same as strftime of datetime.datetime.now() - timedelta(1) ."""
        yesterdays_date = ligrarian.dt.now() - ligrarian.timedelta(1)
        formatted_date = ligrarian.dt.strftime(yesterdays_date, '%d/%m/%Y')
        assert ligrarian.get_date_str(yesterday=True) == formatted_date


@mock.patch('ligrarian.input')
class TestCheckAndPromptForEmailPassword:
    """Test function returns, prompts for and calls with the right values."""

    def create_mock_settings(self, **kwargs):
        """Modify copy of settings dictionary via kwargs then return it."""
        default = {'email': 'email', 'password': None, 'prompt': True}
        modified_settings = default.copy()
        for setting, value in kwargs.items():
            modified_settings[setting] = value
        return modified_settings

    def test_no_email_input_if_set(self, mock_input):
        """If email set don't prompt for it."""
        mock_settings = self.create_mock_settings()
        self.create_mock_settings(password='pass')
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call('Email: ') not in mock_input.call_args_list

    def test_input_for_email_if_not_set(self, mock_input):
        """If email is not set then prompt for it."""
        mock_settings = self.create_mock_settings(email=None, password='pass')
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call('Email: ') in mock_input.call_args_list

    def test_inputted_email_saved_to_settings_dict(self, mock_input):
        """Inputted email saved to settings dict."""
        mock_settings = self.create_mock_settings(email=None, password='pass')
        mock_input.return_value = 'inputted email'
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock_settings['email'] == 'inputted email'

    def test_no_password_input_if_set(self, mock_input):
        """If password set don't prompt for it."""
        mock_settings = self.create_mock_settings(password='pass')
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call('Password: ') not in mock_input.call_args_list

    def test_password_input_if_set(self, mock_input):
        """If password is not set then prompt for it."""
        mock_settings = self.create_mock_settings()
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call('Password: ') in mock_input.call_args_list

    def test_no_save_input_if_prompt_false(self, mock_input):
        """If password is not set and prompt False then no 'Save' input."""
        mock_settings = self.create_mock_settings(password=None, prompt=False)
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call(
                'Save Password?(y/n): ') not in mock_input.call_args_list

    def test_save_input_if_prompt_true(self, mock_input):
        """If password is not set and prompt True then 'Save' input."""
        mock_settings = self.create_mock_settings()
        mock_settings = {'email': '', 'password': '', 'prompt': True}
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock.call('Save Password?(y/n): ') in mock_input.call_args_list

    def test_password_saved_if_save_y(self, mock_input):
        """Password saved to settings dictionary if 'Save' 'y'."""
        mock_settings = self.create_mock_settings()
        mock_input.side_effect = ['inputted pass', 'y']
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock_settings['password'] == 'inputted pass'

    def test_password_not_saved_if_save_n(self, mock_input):
        """Password not saved to settings dictionary if 'Save' 'n'."""
        mock_settings = self.create_mock_settings()
        mock_input.side_effect = ['inputted pass', 'n', 'n']
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock_settings['password'] is None

    def test_prompt_set_to_true_if_disable_y(self, mock_input):
        """Prompt saved as False if disable y."""
        mock_settings = self.create_mock_settings()
        mock_input.side_effect = ['inputted pass', 'n', 'y']
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock_settings['prompt'] is False

    def test_prompt_set_to_false_if_disable_n(self, mock_input):
        """Prompt saved as True if disable n."""
        mock_settings = self.create_mock_settings()
        mock_input.side_effect = ['inputted pass', 'n', 'n']
        ligrarian.check_and_prompt_for_email_password(mock_settings)
        assert mock_settings['prompt'] is True


@mock.patch('ligrarian.open', new_callable=mock.mock_open())
class TestWriteInitialConfig:
    """Test function writes config correctly and to the correct file."""

    def test_initial_config_opens_settings_file(self, mock_open):
        """Should open settings.ini in write mode."""
        ligrarian.write_initial_config()
        mock_open.assert_called_once_with('settings.ini', 'w')

    def test_initial_config_write(self, mock_open_settings):
        """Should write default config to file.

        ConfigParser writes line by line so checking that a middle call is
        as expected indicats the entire file has been written as desired.
        """
        ligrarian.write_initial_config()
        written_config = mock_open_settings.return_value.__enter__().write
        written_middle = written_config.call_args_list[7][0][0]
        assert written_middle == "headless = False\n"


@mock.patch('ligrarian.configparser.ConfigParser')
@mock.patch('ligrarian.open')
class TestWriteConfig:
    """Test function writes arguments to correct file."""

    def test_write_config_opens_settings_file(self, mock_open, mock_parser):
        """Should open settings.ini in write mode."""
        ligrarian.write_initial_config()
        mock_open.assert_called_once_with('settings.ini', 'w')

    def test_write_config_email(self, mock_open, mock_parser):
        """ConfigParser.set should be called with argument email."""
        ligrarian.write_config("argument email", "password", "prompt")
        mock_parser.return_value.set.assert_any_call(
                "user", "email", "argument email"
        )

    def test_write_config_password(self, mock_open, mock_parser):
        """ConfigParser.set should be called with argument password."""
        ligrarian.write_config("email", "argument pass", "prompt")
        mock_parser.return_value.set.assert_any_call(
                "user", "password", "argument pass"
        )

    def test_write_config_prompt(self, mock_open, mock_parser):
        """ConfigParser.set should be called with argument prompt."""
        ligrarian.write_config("email", "password", "argument prompt")
        mock_parser.return_value.set.assert_any_call(
                "settings", "prompt", "argument prompt"
        )
