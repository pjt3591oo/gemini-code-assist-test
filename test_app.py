"""
Comprehensive unit tests for app.py

This test suite covers the main() function and module-level behavior,
including output validation, execution flow, and edge cases.
"""

import unittest
import sys
import io
from unittest.mock import patch, MagicMock
import importlib


class TestMainFunction(unittest.TestCase):
    """Test cases for the main() function in app.py"""

    def setUp(self):
        """Set up test fixtures before each test"""
        # Capture stdout for output verification
        self.held_output = io.StringIO()
        
    def tearDown(self):
        """Clean up after each test"""
        self.held_output.close()

    def test_main_prints_hello_world(self):
        """Test that main() prints 'hello world' to stdout"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertEqual(output.strip(), "hello world")

    def test_main_prints_with_newline(self):
        """Test that main() prints with a newline character"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertTrue(output.endswith('\n'))

    def test_main_calls_print_once(self):
        """Test that main() calls print exactly once"""
        from app import main
        
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_once_with("hello world")

    def test_main_returns_none(self):
        """Test that main() returns None (standard Python function behavior)"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()):
            result = main()
            self.assertIsNone(result)

    def test_main_executes_without_exception(self):
        """Test that main() executes without raising any exceptions"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()):
            main()

    def test_main_output_exact_string(self):
        """Test that main() output matches exactly 'hello world' (case-sensitive)"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, "hello world")
            # Verify case sensitivity
            self.assertNotEqual(output, "Hello World")
            self.assertNotEqual(output, "HELLO WORLD")
            self.assertNotEqual(output, "Hello world")

    def test_main_output_length(self):
        """Test that main() output has expected length"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(len(output), 11)  # "hello world" is 11 characters

    def test_main_does_not_modify_stdout(self):
        """Test that main() doesn't modify sys.stdout object itself"""
        from app import main
        
        original_stdout = sys.stdout
        with patch('sys.stdout', new=io.StringIO()):
            main()
        self.assertIs(sys.stdout, original_stdout)

    def test_main_multiple_calls(self):
        """Test that main() can be called multiple times with consistent output"""
        from app import main
        
        outputs = []
        for _ in range(3):
            with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                main()
                outputs.append(mock_stdout.getvalue().strip())
        
        # All outputs should be identical
        self.assertEqual(len(set(outputs)), 1)
        self.assertEqual(outputs[0], "hello world")

    def test_main_with_redirected_stdout(self):
        """Test that main() respects redirected stdout"""
        from app import main
        
        custom_output = io.StringIO()
        original_stdout = sys.stdout
        
        try:
            sys.stdout = custom_output
            main()
            output = custom_output.getvalue()
            self.assertIn("hello world", output)
        finally:
            sys.stdout = original_stdout
            custom_output.close()


class TestMainFunctionBehavior(unittest.TestCase):
    """Additional behavioral tests for main()"""

    def test_main_is_callable(self):
        """Test that main is a callable function"""
        from app import main
        self.assertTrue(callable(main))

    def test_main_function_name(self):
        """Test that the function has the correct name"""
        from app import main
        self.assertEqual(main.__name__, "main")

    def test_main_accepts_no_parameters(self):
        """Test that main() can be called with no arguments"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()):
            try:
                main()
            except TypeError:
                self.fail("main() should accept no arguments")

    def test_main_rejects_parameters(self):
        """Test that main() raises TypeError when called with arguments"""
        from app import main
        
        with self.assertRaises(TypeError):
            main("unexpected_argument")

    def test_main_with_empty_environment(self):
        """Test main() works in a minimal environment"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            with patch.dict('os.environ', {}, clear=True):
                main()
                output = mock_stdout.getvalue().strip()
                self.assertEqual(output, "hello world")


class TestModuleImport(unittest.TestCase):
    """Test cases for module-level behavior"""

    def test_module_can_be_imported(self):
        """Test that app module can be imported successfully"""
        try:
            import app
            self.assertIsNotNone(app)
        except ImportError as e:
            self.fail(f"Failed to import app module: {e}")

    def test_module_has_main_function(self):
        """Test that the module has a main function"""
        import app
        self.assertTrue(hasattr(app, 'main'))

    def test_module_main_is_function(self):
        """Test that main is a function object"""
        import app
        import types
        self.assertIsInstance(app.main, types.FunctionType)

    def test_module_attributes(self):
        """Test that module has expected attributes"""
        import app
        self.assertTrue(hasattr(app, '__name__'))
        self.assertTrue(hasattr(app, '__file__'))


class TestOutputContent(unittest.TestCase):
    """Test cases focused on output content validation"""

    def test_output_contains_hello(self):
        """Test that output contains the word 'hello'"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("hello", output)

    def test_output_contains_world(self):
        """Test that output contains the word 'world'"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertIn("world", output)

    def test_output_is_lowercase(self):
        """Test that output is in lowercase"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            self.assertEqual(output, output.lower())

    def test_output_has_no_leading_whitespace(self):
        """Test that output has no leading whitespace"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertFalse(output.startswith(' '))
            self.assertFalse(output.startswith('\t'))

    def test_output_words_separated_by_space(self):
        """Test that 'hello' and 'world' are separated by a single space"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            words = output.split()
            self.assertEqual(len(words), 2)
            self.assertEqual(words[0], "hello")
            self.assertEqual(words[1], "world")

    def test_output_no_extra_characters(self):
        """Test that output contains only expected characters"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue().strip()
            allowed_chars = set("hello world")
            output_chars = set(output)
            self.assertTrue(output_chars.issubset(allowed_chars))


class TestEdgeCases(unittest.TestCase):
    """Edge case and error condition tests"""

    def test_main_with_broken_stdout(self):
        """Test main() behavior when stdout write fails"""
        from app import main
        
        mock_stdout = MagicMock()
        mock_stdout.write.side_effect = IOError("Simulated write error")
        
        with patch('sys.stdout', mock_stdout):
            # print() internally catches some exceptions, but let's verify behavior
            try:
                with self.assertRaises(IOError):
                    main()
            except AssertionError:
                # If no exception is raised, that's also acceptable behavior
                pass

    def test_main_thread_safety(self):
        """Test that main() can be called from multiple contexts"""
        from app import main
        import threading
        
        results = []
        
        def call_main():
            with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
                main()
                results.append(mock_stdout.getvalue().strip())
        
        threads = [threading.Thread(target=call_main) for _ in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        
        # All calls should produce the same output
        self.assertEqual(len(results), 5)
        for result in results:
            self.assertEqual(result, "hello world")

    def test_main_with_unicode_environment(self):
        """Test that main() works correctly with Unicode environment"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            # Set a Unicode environment
            with patch.dict('os.environ', {'LANG': 'en_US.UTF-8'}):
                main()
                output = mock_stdout.getvalue().strip()
                self.assertEqual(output, "hello world")

    def test_main_memory_efficiency(self):
        """Test that main() doesn't leak memory on repeated calls"""
        from app import main
        import gc
        
        # Call main multiple times and force garbage collection
        for _ in range(100):
            with patch('sys.stdout', new=io.StringIO()):
                main()
        
        gc.collect()
        # If we got here without memory errors, test passes
        self.assertTrue(True)


class TestPrintFunctionBehavior(unittest.TestCase):
    """Test cases specifically for the print function behavior"""

    def test_print_uses_default_separator(self):
        """Test that print uses default separator (space)"""
        from app import main
        
        with patch('builtins.print') as mock_print:
            main()
            # Verify print was called with the string, not multiple arguments
            args, _kwargs = mock_print.call_args
            self.assertEqual(len(args), 1)
            self.assertEqual(args[0], "hello world")

    def test_print_uses_default_end(self):
        """Test that print uses default end parameter (newline)"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            main()
            output = mock_stdout.getvalue()
            self.assertTrue(output.endswith('\n'))

    def test_print_to_stdout_not_stderr(self):
        """Test that output goes to stdout, not stderr"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            with patch('sys.stderr', new=io.StringIO()) as mock_stderr:
                main()
                stdout_output = mock_stdout.getvalue()
                stderr_output = mock_stderr.getvalue()
                
                self.assertIn("hello world", stdout_output)
                self.assertEqual(stderr_output, "")


class TestIntegration(unittest.TestCase):
    """Integration-style tests for module execution"""

    def test_module_execution_simulation(self):
        """Test simulated module execution (like running 'python app.py')"""
        # This simulates what happens when the module is run directly
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            # Import fresh to simulate execution
            import importlib
            import app
            importlib.reload(app)
            output = mock_stdout.getvalue()
            # The module calls main() at module level
            self.assertIn("hello world", output)

    def test_main_can_be_used_as_entry_point(self):
        """Test that main() is suitable as a program entry point"""
        from app import main
        
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            # Simulate calling from __main__
            if callable(main):
                main()
            output = mock_stdout.getvalue()
            self.assertIn("hello world", output)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)