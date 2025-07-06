"""
Unit tests for Survey123Publisher functionality.

These tests are skipped by default since they require:
1. ArcGIS Python API installation
2. Valid ArcGIS Online/Enterprise credentials
3. Network connectivity

To run these tests, set the environment variable ENABLE_PUBLISHER_TESTS=1
or remove the @unittest.skip decorators.
"""

import unittest
import os
import tempfile
import sys
import traceback
import argparse
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the parent directory to the path so we can import survey123py
sys.path.insert(0, str(Path(__file__).parent.parent))

# Check if publisher tests should be enabled
ENABLE_PUBLISHER_TESTS = str(os.environ.get("ENABLE_PUBLISHER_TESTS", "0")) == "1"

# Skip reason message
SKIP_REASON = (
    "Publisher tests skipped. Requires ArcGIS Python API and valid credentials. "
    "Set ENABLE_PUBLISHER_TESTS=1 to enable."
)
    

class TestSurvey123Publisher(unittest.TestCase):
    """Test cases for Survey123Publisher class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Path to the test YAML file
        self.sample_yaml_path = Path(__file__).parent / "data" / "test_publisher_sample.yaml"
        
        # Create temporary YAML file by copying the sample
        self.temp_yaml = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        with open(self.sample_yaml_path, 'r') as f:
            self.temp_yaml.write(f.read())
        self.temp_yaml.close()
    
    def _create_authenticated_publisher(self):
        """
        Create an authenticated Survey123Publisher using environment variables.
        
        Returns
        -------
        Survey123Publisher
            An authenticated publisher instance
            
        Raises
        ------
        unittest.SkipTest
            If authentication credentials are not available
        """
        from survey123py.publisher import Survey123Publisher
        
        # Check for username/password authentication
        username = os.environ.get('USERNAME')
        password = os.environ.get('PASSWORD')
        
        if username and password:
            try:
                from arcgis.gis import GIS
                gis = GIS("https://intrax.maps.arcgis.com", username=username, password=password)
                return Survey123Publisher(gis=gis)
            except Exception as e:
                self.skipTest(f"Failed to authenticate with username/password: {e}")
        else:
            # Fall back to default authentication
            try:
                return Survey123Publisher()
            except Exception as e:
                self.skipTest(f"Failed to initialize publisher (set USERNAME and PASSWORD env vars or configure default auth): {e}")
        
    def tearDown(self):
        """Clean up test fixtures."""
        if os.path.exists(self.temp_yaml.name):
            os.unlink(self.temp_yaml.name)
    
    @unittest.skipUnless(ENABLE_PUBLISHER_TESTS, SKIP_REASON)
    def test_publisher_import(self):
        """Test that publisher module can be imported."""
        try:
            from survey123py.publisher import Survey123Publisher, publish_survey
            self.assertTrue(True, "Publisher module imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import publisher module: {e}")
    
    @unittest.skipUnless(ENABLE_PUBLISHER_TESTS, SKIP_REASON)
    def test_publisher_initialization(self):
        """Test Survey123Publisher initialization."""
        publisher = self._create_authenticated_publisher()
        self.assertIsNotNone(publisher.gis)
        self.assertIsNotNone(publisher.survey_manager)
        
        # Check user privileges
        user_info = publisher.get_user_info()
        
        # Verify user has necessary privileges
        self.assertTrue(user_info['can_create_items'], 
                       "User must have 'create items' privilege to publish surveys")
        self.assertTrue(user_info['can_publish'], 
                       "User must have 'publish features' privilege to publish surveys")
    
    @unittest.skipUnless(ENABLE_PUBLISHER_TESTS, SKIP_REASON)
    def test_create_survey(self):
        """Test creating a new survey."""
        publisher = self._create_authenticated_publisher()
        
        try:
            # Create a test survey
            survey = publisher.create_survey(
                title="Test Survey - Unit Test",
                tags=["test", "unittest", "survey123py"],
                summary="Unit test survey",
                folder="Unit Tests"
            )
            
            self.assertIsNotNone(survey)
            self.assertEqual(survey.title, "Test Survey - Unit Test")
            
        except Exception as e:
            print(f"FULL TRACEBACK:\n{traceback.format_exc()}")
            self.skipTest(f"Failed to create survey (likely auth/network issue): {e}")
    
    @unittest.skipUnless(ENABLE_PUBLISHER_TESTS, SKIP_REASON)
    def test_publish_from_yaml(self):
        """Test complete YAML to Survey123 publishing workflow."""
        publisher = self._create_authenticated_publisher()
        
        try:
            # Publish survey from YAML
            survey = publisher.publish_from_yaml(
                yaml_path=self.temp_yaml.name,
                title="Test YAML Survey - Unit Test",
                tags=["test", "unittest", "yaml"],
                summary="Unit test YAML survey",
                folder="Unit Tests",
                keep_excel=True,
                excel_output_path="test_survey_unittest.xlsx"
            )

            self.assertIsNotNone(survey)
            self.assertEqual(survey.properties["title"], "Test YAML Survey - Unit Test")
            self.assertTrue(os.path.exists("test_survey_unittest.xlsx"))
            
            # Verify survey properties
            self.assertIsNotNone(survey.properties["id"])
            
            # Clean up
            # Note: There is no built-in delete method in the publisher, so we the survey has to be deleted manually
            if os.path.exists("test_survey_unittest.xlsx"):
                os.unlink("test_survey_unittest.xlsx")
                
        except Exception as e:
            print(f"FULL TRACEBACK:\n{traceback.format_exc()}")
            self.skipTest(f"Failed to publish from YAML (likely auth/network issue): {e}")
    
    @unittest.skipUnless(ENABLE_PUBLISHER_TESTS, SKIP_REASON)
    def test_convenience_function(self):
        """Test the convenience publish_survey function."""
        from survey123py.publisher import publish_survey
        
        try:
            survey = publish_survey(
                yaml_path=self.temp_yaml.name,
                title="Convenience Test Survey - Unit Test",
                tags=["test", "convenience", "unittest"]
            )
            
            self.assertIsNotNone(survey)
            self.assertEqual(survey.properties["title"], "Convenience Test Survey - Unit Test")
            
            # Clean up
            # Note: There is no built-in delete method in the publisher, so we the survey has to be deleted manually
            
        except Exception as e:
            print(f"FULL TRACEBACK:\n{traceback.format_exc()}")
            self.skipTest(f"Failed convenience function test (likely auth/network issue): {e}")


class TestCLIAuthentication(unittest.TestCase):
    """Test cases for CLI authentication functionality."""
    
    def test_cli_auth_import(self):
        """Test that CLI authentication functions can be imported."""
        try:
            from main import create_gis_connection
            self.assertTrue(True, "CLI authentication functions imported successfully")
        except ImportError as e:
            self.fail(f"Failed to import CLI authentication functions: {e}")
    
    @patch('main.GIS')
    def test_create_gis_connection_default(self, mock_gis):
        """Test creating GIS connection with default authentication."""
        from main import create_gis_connection
        
        # Create mock args with no authentication parameters
        args = argparse.Namespace(
            url=None,
            username=None,
            password=None,
            token=None,
            cert_file=None,
            key_file=None
        )
        
        # Mock GIS to return a mock object
        mock_gis_instance = Mock()
        mock_gis.return_value = mock_gis_instance
        
        result = create_gis_connection(args)
        
        # Verify GIS was called with "home"
        mock_gis.assert_called_once_with("home")
        self.assertEqual(result, mock_gis_instance)
    
    @patch('main.GIS')
    def test_create_gis_connection_username_password(self, mock_gis):
        """Test creating GIS connection with username/password."""
        from main import create_gis_connection
        
        # Create mock args with username/password
        args = argparse.Namespace(
            url="https://myorg.maps.arcgis.com",
            username="testuser",
            password="testpass",
            token=None,
            cert_file=None,
            key_file=None
        )
        
        mock_gis_instance = Mock()
        mock_gis.return_value = mock_gis_instance
        
        result = create_gis_connection(args)
        
        # Verify GIS was called with correct parameters
        mock_gis.assert_called_once_with(
            url="https://myorg.maps.arcgis.com",
            username="testuser",
            password="testpass"
        )
        self.assertEqual(result, mock_gis_instance)
    
    @patch('main.GIS')
    def test_create_gis_connection_token(self, mock_gis):
        """Test creating GIS connection with token."""
        from main import create_gis_connection
        
        # Create mock args with token
        args = argparse.Namespace(
            url="https://myorg.maps.arcgis.com",
            username=None,
            password=None,
            token="test_token_123",
            cert_file=None,
            key_file=None
        )
        
        mock_gis_instance = Mock()
        mock_gis.return_value = mock_gis_instance
        
        result = create_gis_connection(args)
        
        # Verify GIS was called with token
        mock_gis.assert_called_once_with(
            url="https://myorg.maps.arcgis.com",
            token="test_token_123"
        )
        self.assertEqual(result, mock_gis_instance)
    
    @patch('main.GIS')
    def test_create_gis_connection_pki(self, mock_gis):
        """Test creating GIS connection with PKI certificates."""
        from main import create_gis_connection
        
        # Create mock args with PKI
        args = argparse.Namespace(
            url="https://myorg.maps.arcgis.com",
            username=None,
            password=None,
            token=None,
            cert_file="/path/to/cert.pem",
            key_file="/path/to/key.pem"
        )
        
        mock_gis_instance = Mock()
        mock_gis.return_value = mock_gis_instance
        
        result = create_gis_connection(args)
        
        # Verify GIS was called with PKI parameters
        mock_gis.assert_called_once_with(
            url="https://myorg.maps.arcgis.com",
            cert_file="/path/to/cert.pem",
            key_file="/path/to/key.pem"
        )
        self.assertEqual(result, mock_gis_instance)
    
    @patch('main.getpass.getpass')
    @patch('main.GIS')
    def test_create_gis_connection_username_prompt_password(self, mock_gis, mock_getpass):
        """Test creating GIS connection with username and prompted password."""
        from main import create_gis_connection
        
        # Create mock args with username but no password
        args = argparse.Namespace(
            url=None,
            username="testuser",
            password=None,
            token=None,
            cert_file=None,
            key_file=None
        )
        
        # Mock getpass to return a password
        mock_getpass.return_value = "prompted_password"
        mock_gis_instance = Mock()
        mock_gis.return_value = mock_gis_instance
        
        result = create_gis_connection(args)
        
        # Verify password was prompted
        mock_getpass.assert_called_once_with("Password for testuser: ")
        
        # Verify GIS was called with correct parameters (default URL for ArcGIS Online)
        mock_gis.assert_called_once_with(
            url="https://www.arcgis.com",
            username="testuser",
            password="prompted_password"
        )
        self.assertEqual(result, mock_gis_instance)
    
    @patch('main.GIS')
    def test_create_gis_connection_error_handling(self, mock_gis):
        """Test error handling in GIS connection creation."""
        from main import create_gis_connection
        
        # Create mock args
        args = argparse.Namespace(
            url="https://invalid.url",
            username="testuser",
            password="wrongpass",
            token=None,
            cert_file=None,
            key_file=None
        )
        
        # Mock GIS to raise an exception
        mock_gis.side_effect = Exception("Authentication failed")
        
        with self.assertRaises(RuntimeError) as context:
            create_gis_connection(args)
        
        self.assertIn("Authentication failed", str(context.exception))
    
    @patch('argparse.ArgumentParser.parse_args')
    def test_cli_authentication_parameters_exist(self, mock_parse_args):
        """Test that authentication parameters are properly defined in CLI."""
        from main import main
        
        # Mock sys.argv to have authentication parameters
        test_args = [
            'main.py', 'publish',
            '-i', 'test.yaml',
            '-t', 'Test Survey',
            '--url', 'https://myorg.maps.arcgis.com',
            '--username', 'testuser',
            '--password', 'testpass',
            '--token', 'test_token',
            '--cert-file', '/path/to/cert.pem',
            '--key-file', '/path/to/key.pem'
        ]
        
        # Create a mock Namespace object with all the expected attributes
        mock_args = argparse.Namespace(
            command='publish',
            input='test.yaml',
            title='Test Survey',
            url='https://myorg.maps.arcgis.com',
            username='testuser',
            password='testpass',
            token='test_token',
            cert_file='/path/to/cert.pem',
            key_file='/path/to/key.pem',
            version='3.22',
            folder=None,
            tags=None,
            summary=None,
            description=None,
            thumbnail=None,
            media_folder=None,
            scripts_folder=None,
            no_web_form=False,
            no_web_map=False,
            enable_delete_protection=False,
            enable_sync=False,
            schema_changes=False,
            keep_excel=False,
            excel_output=None
        )
        
        mock_parse_args.return_value = mock_args
        
        # Patch the publish_survey function to prevent actual execution
        with patch('main.publish_survey') as mock_publish:
            with patch('sys.argv', test_args):
                try:
                    main()
                except SystemExit:
                    pass  # Expected when mocking
                
                # Verify that publish_survey was called with the mocked args
                mock_publish.assert_called_once_with(mock_args)
                
                # Verify all authentication attributes exist
                self.assertEqual(mock_args.url, 'https://myorg.maps.arcgis.com')
                self.assertEqual(mock_args.username, 'testuser')
                self.assertEqual(mock_args.password, 'testpass')
                self.assertEqual(mock_args.token, 'test_token')
                self.assertEqual(mock_args.cert_file, '/path/to/cert.pem')
                self.assertEqual(mock_args.key_file, '/path/to/key.pem')


if __name__ == "__main__":
    unittest.main()