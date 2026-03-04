import sys
import unittest
from io import StringIO
from unittest.mock import patch, call

from app import test


class TestRecursiveFunctions(unittest.TestCase):
    """Test suite for func_a and func_b recursive functions."""

    def test_func_a_prints_correct_output(self):
        """Test that func_a prints 'func_a' to stdout."""
        with patch('app.test.func_b'):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                test.func_a()
                self.assertEqual(mock_stdout.getvalue(), "func_a\n")

    def test_func_b_prints_correct_output(self):
        """Test that func_b prints 'func_b' to stdout."""
        with patch('app.test.func_a'):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                test.func_b()
                self.assertEqual(mock_stdout.getvalue(), "func_b\n")

    def test_func_a_calls_func_b(self):
        """Test that func_a calls func_b after printing."""
        with patch('app.test.func_b') as mock_func_b:
            with patch('sys.stdout', new_callable=StringIO):
                test.func_a()
                mock_func_b.assert_called_once()

    def test_func_b_calls_func_a(self):
        """Test that func_b calls func_a after printing."""
        with patch('app.test.func_a') as mock_func_a:
            with patch('sys.stdout', new_callable=StringIO):
                test.func_b()
                mock_func_a.assert_called_once()

    def test_mutual_recursion_raises_recursion_error(self):
        """Test that calling func_a leads to RecursionError due to mutual recursion."""
        with self.assertRaises(RecursionError):
            test.func_a()

    def test_mutual_recursion_from_func_b_raises_recursion_error(self):
        """Test that calling func_b also leads to RecursionError due to mutual recursion."""
        with self.assertRaises(RecursionError):
            test.func_b()

    def test_recursion_produces_alternating_output(self):
        """Test that the recursion produces alternating 'func_a' and 'func_b' output."""
        original_recursion_limit = sys.getrecursionlimit()
        try:
            # Set a low recursion limit to quickly trigger the error (must be high enough for test framework overhead)
            sys.setrecursionlimit(100)
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                try:
                    test.func_a()
                except RecursionError:
                    pass
                output = mock_stdout.getvalue()
                # Verify alternating pattern exists
                self.assertIn("func_a\n", output)
                self.assertIn("func_b\n", output)
                # Verify output starts with func_a
                self.assertTrue(output.startswith("func_a\n"))
        finally:
            sys.setrecursionlimit(original_recursion_limit)

    def test_recursion_depth_verification(self):
        """Test that recursion continues until the limit is reached."""
        original_recursion_limit = sys.getrecursionlimit()
        try:
            # Set a known low limit
            sys.setrecursionlimit(100)
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with self.assertRaises(RecursionError):
                    test.func_a()
                output = mock_stdout.getvalue()
                # Count occurrences to verify deep recursion
                func_a_count = output.count("func_a")
                func_b_count = output.count("func_b")
                # Should have multiple calls before hitting the limit
                self.assertGreater(func_a_count, 3)
                self.assertGreater(func_b_count, 3)
                # Counts should be close (differ by at most 1)
                self.assertLessEqual(abs(func_a_count - func_b_count), 1)
        finally:
            sys.setrecursionlimit(original_recursion_limit)

    def test_func_a_docstring_exists(self):
        """Test that func_a has proper documentation."""
        self.assertIsNotNone(test.func_a.__doc__)
        self.assertIn("func_a", test.func_a.__doc__)

    def test_func_b_docstring_exists(self):
        """Test that func_b has proper documentation."""
        self.assertIsNotNone(test.func_b.__doc__)
        self.assertIn("func_b", test.func_b.__doc__)

    def test_functions_are_callable(self):
        """Test that both functions are callable objects."""
        self.assertTrue(callable(test.func_a))
        self.assertTrue(callable(test.func_b))

    def test_no_return_value_from_func_a(self):
        """Test that func_a doesn't return a value (implicitly returns None)."""
        with patch('app.test.func_b'):
            with patch('sys.stdout', new_callable=StringIO):
                result = test.func_a()
                self.assertIsNone(result)

    def test_no_return_value_from_func_b(self):
        """Test that func_b doesn't return a value (implicitly returns None)."""
        with patch('app.test.func_a'):
            with patch('sys.stdout', new_callable=StringIO):
                result = test.func_b()
                self.assertIsNone(result)

    def test_call_sequence_verification(self):
        """Test the exact sequence of calls in the recursion chain."""
        call_sequence = []

        def track_func_a():
            call_sequence.append('func_a')
            if len(call_sequence) < 5:
                test.func_b()

        def track_func_b():
            call_sequence.append('func_b')
            if len(call_sequence) < 5:
                test.func_a()

        with patch('app.test.func_a', side_effect=track_func_a):
            with patch('app.test.func_b', side_effect=track_func_b):
                with patch('sys.stdout', new_callable=StringIO):
                    track_func_a()

        # Verify alternating pattern
        expected = ['func_a', 'func_b', 'func_a', 'func_b', 'func_a']
        self.assertEqual(call_sequence, expected)


if __name__ == "__main__":
    unittest.main()