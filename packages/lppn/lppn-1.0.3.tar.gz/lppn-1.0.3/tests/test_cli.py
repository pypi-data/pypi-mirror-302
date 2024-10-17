#!/usr/bin/python3
# -*- coding: utf-8 -*-

import unittest
import sys
import io
from unittest.mock import patch
from contextlib import redirect_stdout
import lppn.cli as cli


class TestCli(unittest.TestCase):
    def setUp(self):
        # known and valid major number
        self.major = 3
        # known and valid minor number
        self.minor = 12
        # known and valid latest patch number
        self.latest_patch = 7

    @patch("lppn.get")
    def test_print_patch(self, mock_lppn_get):
        mock_lppn_get.return_value = self.latest_patch
        sys.argv = ["lppn", "--get", str(self.major), str(self.minor)]
        with redirect_stdout(io.StringIO()) as f:
            cli.parse()
        s = f.getvalue()
        mock_lppn_get.assert_called_once()
        self.assertIsInstance(type(int(s)), type(int))
        self.assertEqual(str(s), f"{self.latest_patch}\n")

    @patch("lppn.get")
    def test_print_full_version(self, mock_lppn_get):
        mock_lppn_get.return_value = self.latest_patch
        sys.argv = [
            "lppn",
            "--full-version",
            "--get",
            str(self.major),
            str(self.minor),
        ]
        with redirect_stdout(io.StringIO()) as f:
            cli.parse()
        s = f.getvalue()
        self.assertEqual(
            str(s), f"{self.major}.{self.minor}.{self.latest_patch}\n"
        )
        mock_lppn_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
