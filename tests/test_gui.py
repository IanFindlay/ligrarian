import pytest
import unittest.mock as mock

import ligrarian


class TestCreateGUI:
    """Test function creates and returns GUI instance correctly."""

    @mock.patch('ligrarian.tk')
    def test_tk_called(self, mock_tk):
        """tk.Tk() create tkinter instance and should be called."""
        gui_instance = ligrarian.create_gui(mock.MagicMock())
        mock_tk.Tk.assert_called_once()

    @mock.patch('ligrarian.tk')
    def test_gui_instance_created(self, mock_tk):
        """Returned object should be instance of GUI class."""
        gui_instance = ligrarian.create_gui(mock.MagicMock())
        assert isinstance(gui_instance, ligrarian.Gui)


class TestGuiModeDetailsEdits:
    """Test funtion modifies gui.info and returns correctly."""

    def test_mode_true_moves_main_to_url(self):
        """True should lead to info['main'] copied to info['url']."""
        mock_gui = mock.MagicMock()
        mock_gui.mode = True
        mock_gui.info = {'main': 'www'}
        info = ligrarian.gui_mode_details_edits(mock_gui)
        assert info['url'] == 'www'

    def test_mode_false_moves_main_to_search(self):
        """False should lead to info['main'] copied to info['search']."""
        mock_gui = mock.MagicMock()
        mock_gui.mode = False
        mock_gui.info = {'main': 'search string'}
        info = ligrarian.gui_mode_details_edits(mock_gui)
        assert info['search'] == 'search string'

    def test_main_deleted(self):
        """gui.info['main'] should be deleted."""
        mock_gui = mock.MagicMock()
        mock_gui.mode = True
        mock_gui.info = {'main': 'copied then deleted'}
        info = ligrarian.gui_mode_details_edits(mock_gui)
        assert 'main' not in info

    def test_info_dict_returned(self):
        """gui.info should be returned."""
        mock_gui = mock.MagicMock()
        mock_gui.mode = True
        mock_gui.info = {'main': 'copied then deleted'}
        info = ligrarian.gui_mode_details_edits(mock_gui)
        assert info == {'url': 'copied then deleted'}
