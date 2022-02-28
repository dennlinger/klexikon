"""
Simple tests to verify correctness of processing for Huggingface datasets
"""

import unittest

from klexikon.processing.create_datasets_json_files import remove_empty_sections, remove_last_line_if_empty


class ProcessingTest(unittest.TestCase):

    def test_remove_empty_sections(self):
        test_lines = [
            "Article summary."
            "",
            "== Subsection",
            "",
            "Actual paragraph in the subsection",
            "",
            "== Empty Subsection",
            "",
            "== New Subsection",
            "",
            "Actual content in this subsection again",
            "",
            "= New Section",
            "",
            "== Subsubsection",
            "",
            "This one should also stay."
        ]

        expected_result = [
            "Article summary."
            "",
            "== Subsection",
            "",
            "Actual paragraph in the subsection",
            "",
            "== New Subsection",
            "",
            "Actual content in this subsection again",
            "",
            "= New Section",
            "",
            "== Subsubsection",
            "",
            "This one should also stay."
        ]

        self.assertEqual(remove_empty_sections(test_lines), expected_result)

    def test_remove_last_line_if_empty(self):
        test_lines = [
            "== Test Section",
            "",
            "Some text there.",
            ""
        ]

        expected_result = [
            "== Test Section",
            "",
            "Some text there."
        ]

        self.assertEqual(remove_last_line_if_empty(test_lines), expected_result)
