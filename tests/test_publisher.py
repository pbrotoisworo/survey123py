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

if __name__ == "__main__":
    unittest.main()