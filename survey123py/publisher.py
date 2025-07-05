"""
Survey123 Publisher Module

This module provides functionality to publish Survey123 Excel files directly to ArcGIS Online/Enterprise
using the ArcGIS Python API, enabling full automation without requiring Survey123 Connect.
"""

import os
import tempfile
from pathlib import Path
from typing import Dict, Optional, List, Union
import warnings

try:
    import arcgis
    from arcgis.gis import GIS
    from arcgis.apps.survey123 import SurveyManager, Survey
    ARCGIS_API_AVAILABLE = True
except ImportError:
    ARCGIS_API_AVAILABLE = False
    warnings.warn(
        "ArcGIS Python API not found. Install with: pip install arcgis\n"
        "Publishing functionality will not be available.",
        ImportWarning
    )

from .form import FormData


class Survey123Publisher:
    """
    Publisher class for publishing Survey123 Excel files to ArcGIS Online/Enterprise.
    
    This class integrates with Survey123Py's FormData class to provide end-to-end
    automation from YAML to published Survey123 forms.
    """
    
    def __init__(self, gis: Optional[GIS] = None):
        """
        Initialize the Survey123Publisher.
        
        Parameters
        ----------
        gis : arcgis.gis.GIS, optional
            An authenticated GIS connection. If None, will attempt to connect
            using default credentials or prompt for authentication.
        
        Raises
        ------
        ImportError
            If ArcGIS Python API is not installed
        RuntimeError
            If user doesn't have required privileges
        """
        if not ARCGIS_API_AVAILABLE:
            raise ImportError(
                "ArcGIS Python API is required for publishing functionality. "
                "Install with: pip install arcgis"
            )
        
        self.gis = gis or GIS("home")
        self.survey_manager = SurveyManager(self.gis)
        
        # Check user privileges
        self._check_privileges()
    
    def _check_privileges(self):
        """
        Check if the current user has required privileges for publishing surveys.
        
        Raises
        ------
        RuntimeError
            If user doesn't have required privileges
        """
        user = self.gis.users.me
        
        # Check if user has publishing privileges
        required_privileges = [
            'portal:user:createItem',
            'portal:publisher:publishFeatures',
            'portal:user:shareToPublic'
        ]
        
        user_privileges = user.privileges if hasattr(user, 'privileges') else []
        
        missing_privileges = []
        for privilege in required_privileges:
            if privilege not in user_privileges:
                missing_privileges.append(privilege)
        
        if missing_privileges:
            raise RuntimeError(
                f"User account lacks required privileges for publishing surveys: {missing_privileges}\n"
                f"User role: {user.role}\n"
                f"User privileges: {user_privileges}\n"
                f"Contact your ArcGIS administrator to grant publishing privileges."
            )
        
        # Check if user can create content
        if hasattr(user, 'roleId') and user.roleId == 'iAAAAAAAAAAAAAAA':  # Viewer role
            raise RuntimeError(
                "User has 'Viewer' role which cannot create content. "
                "Need 'Creator' or 'Publisher' role to publish surveys."
            )
        
        print(f"User privilege check passed. Role: {user.role}")
    
    def get_user_info(self) -> Dict:
        """
        Get current user information and privileges.
        
        Returns
        -------
        dict
            User information including role, privileges, and account status
        """
        user = self.gis.users.me
        
        return {
            'username': user.username,
            'role': user.role,
            'privileges': getattr(user, 'privileges', []),
            'roleId': getattr(user, 'roleId', None),
            'level': getattr(user, 'level', None),
            'can_publish': 'portal:publisher:publishFeatures' in getattr(user, 'privileges', []),
            'can_create_items': 'portal:user:createItem' in getattr(user, 'privileges', [])
        }
        
    def create_survey(self, 
                      title: str,
                      folder: Optional[str] = None,
                      tags: Optional[List[str]] = None,
                      summary: Optional[str] = None,
                      description: Optional[str] = None,
                      thumbnail: Optional[str] = None) -> Survey:
        """
        Create a new Survey123 form item in ArcGIS Online/Enterprise.
        
        Parameters
        ----------
        title : str
            Title of the survey
        folder : str, optional
            Folder to store the survey in
        tags : list of str, optional
            Tags to associate with the survey
        summary : str, optional
            Brief summary of the survey
        description : str, optional
            Detailed description of the survey
        thumbnail : str, optional
            Path to thumbnail image file
            
        Returns
        -------
        Survey
            The created Survey object
        """
        create_params = {
            "title": title,
            "folder": folder,
            "tags": tags or [],
            "summary": summary or "",
            "description": description or "",
        }
        
        if thumbnail and os.path.exists(thumbnail):
            create_params["thumbnail"] = thumbnail
            
        return self.survey_manager.create(**create_params)
    
    def publish_from_excel(self,
                          survey: Survey,
                          excel_path: str,
                          media_folder: Optional[str] = None,
                          scripts_folder: Optional[str] = None,
                          create_web_form: bool = True,
                          create_web_map: bool = True,
                          enable_delete_protection: bool = False,
                          enable_sync: bool = False,
                          schema_changes: bool = False,
                          info: Optional[Dict] = None,
                          activate_survey: bool = True) -> Survey:
        """
        Publish a Survey123 form using an Excel file.
        
        Parameters
        ----------
        survey : Survey
            The Survey object to publish to
        excel_path : str
            Path to the Survey123-compatible Excel file
        media_folder : str, optional
            Path to folder containing media files
        scripts_folder : str, optional
            Path to folder containing JavaScript files
        create_web_form : bool, default True
            Whether to create a web form
        create_web_map : bool, default True
            Whether to create a web map
        enable_delete_protection : bool, default False
            Whether to enable delete protection
        enable_sync : bool, default False
            Whether to enable sync capabilities
        schema_changes : bool, default False
            Whether to allow schema changes
        info : dict, optional
            Additional survey configuration
        activate_survey : bool, default True
            Whether to activate the survey for data collection
            
        Returns
        -------
        Survey
            The published Survey object
        """
        if not os.path.exists(excel_path):
            raise FileNotFoundError(f"Excel file not found: {excel_path}")
            
        publish_params = {
            "xlsform": excel_path,
            "create_web_form": create_web_form,
            "create_web_map": create_web_map,
            "enable_delete_protection": enable_delete_protection,
            "enable_sync": enable_sync,
            "schema_changes": schema_changes,
        }
        
        if media_folder and os.path.exists(media_folder):
            publish_params["media"] = media_folder
            
        if scripts_folder and os.path.exists(scripts_folder):
            publish_params["scripts"] = scripts_folder
            
        if info:
            publish_params["info"] = info
            
        return survey.publish(**publish_params)
    
    def publish_from_yaml(self,
                         yaml_path: str,
                         title: str,
                         version: str = "3.22",
                         folder: Optional[str] = None,
                         tags: Optional[List[str]] = None,
                         summary: Optional[str] = None,
                         description: Optional[str] = None,
                         thumbnail: Optional[str] = None,
                         media_folder: Optional[str] = None,
                         scripts_folder: Optional[str] = None,
                         create_web_form: bool = True,
                         create_web_map: bool = True,
                         enable_delete_protection: bool = False,
                         enable_sync: bool = False,
                         schema_changes: bool = False,
                         info: Optional[Dict] = None,
                         keep_excel: bool = False,
                         excel_output_path: Optional[str] = None) -> Survey:
        """
        Complete workflow: Convert YAML to Excel and publish to Survey123.
        
        This method provides end-to-end automation from YAML survey definition
        to published Survey123 form.
        
        Parameters
        ----------
        yaml_path : str
            Path to the YAML survey definition file
        title : str
            Title of the survey
        version : str, default "3.22"
            Survey123 version to use
        folder : str, optional
            Folder to store the survey in
        tags : list of str, optional
            Tags to associate with the survey
        summary : str, optional
            Brief summary of the survey
        description : str, optional
            Detailed description of the survey
        thumbnail : str, optional
            Path to thumbnail image file
        media_folder : str, optional
            Path to folder containing media files
        scripts_folder : str, optional
            Path to folder containing JavaScript files
        create_web_form : bool, default True
            Whether to create a web form
        create_web_map : bool, default True
            Whether to create a web map
        enable_delete_protection : bool, default False
            Whether to enable delete protection
        enable_sync : bool, default False
            Whether to enable sync capabilities
        schema_changes : bool, default False
            Whether to allow schema changes
        info : dict, optional
            Additional survey configuration
        keep_excel : bool, default False
            Whether to keep the intermediate Excel file
        excel_output_path : str, optional
            Custom path for the Excel file (if keep_excel=True)
            
        Returns
        -------
        Survey
            The published Survey object
            
        Examples
        --------
        Basic usage:
        
        >>> from survey123py.publisher import Survey123Publisher
        >>> publisher = Survey123Publisher()
        >>> survey = publisher.publish_from_yaml(
        ...     yaml_path="my_survey.yaml",
        ...     title="Customer Feedback Survey",
        ...     tags=["feedback", "customer"],
        ...     summary="Survey for collecting customer feedback"
        ... )
        
        With custom settings:
        
        >>> survey = publisher.publish_from_yaml(
        ...     yaml_path="my_survey.yaml",
        ...     title="Water Quality Survey",
        ...     folder="Environmental Surveys",
        ...     enable_sync=True,
        ...     info={"queryInfo": {"mode": "manual"}},
        ...     keep_excel=True,
        ...     excel_output_path="water_quality_survey.xlsx"
        ... )
        """
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"YAML file not found: {yaml_path}")
        
        # Step 1: Convert YAML to Excel using Survey123Py
        print("DEBUG1")
        form_data = FormData(version)
        form_data.load_yaml(yaml_path)
        
        # Determine Excel output path
        print("DEBUG1")
        if keep_excel and excel_output_path:
            excel_path = excel_output_path
        elif keep_excel:
            # Use YAML filename with .xlsx extension
            yaml_stem = Path(yaml_path).stem
            excel_path = f"{yaml_stem}_survey123.xlsx"
        else:
            # Use temporary file
            temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
            excel_path = temp_file.name
            temp_file.close()

        print("DEBUG: Saving Excel file to", excel_path)
        print("DEBUG: File exists:", os.path.exists(excel_path))
        
        try:
            # Save Excel file
            form_data.save_survey(excel_path)
            
            # Step 2: Create Survey123 form
            survey = self.create_survey(
                title=title,
                folder=folder,
                tags=tags,
                summary=summary,
                description=description,
                thumbnail=thumbnail
            )
            
            # Step 3: Publish the form
            published_survey = self.publish_from_excel(
                survey=survey,
                excel_path=excel_path,
                media_folder=media_folder,
                scripts_folder=scripts_folder,
                create_web_form=create_web_form,
                create_web_map=create_web_map,
                enable_delete_protection=enable_delete_protection,
                enable_sync=enable_sync,
                schema_changes=schema_changes,
                info=info
            )
            
            return published_survey
            
        finally:
            # Clean up temporary file if not keeping Excel
            if not keep_excel and os.path.exists(excel_path):
                os.unlink(excel_path)
    
    def update_survey(self,
                     survey_id: str,
                     excel_path: Optional[str] = None,
                     yaml_path: Optional[str] = None,
                     version: str = "3.22",
                     media_folder: Optional[str] = None,
                     scripts_folder: Optional[str] = None,
                     schema_changes: bool = True,
                     info: Optional[Dict] = None) -> Survey:
        """
        Update an existing Survey123 form.
        
        Parameters
        ----------
        survey_id : str
            ID of the existing survey to update
        excel_path : str, optional
            Path to updated Excel file
        yaml_path : str, optional
            Path to updated YAML file (alternative to excel_path)
        version : str, default "3.22"
            Survey123 version to use (only used with yaml_path)
        media_folder : str, optional
            Path to folder containing media files
        scripts_folder : str, optional
            Path to folder containing JavaScript files
        schema_changes : bool, default True
            Whether to allow schema changes
        info : dict, optional
            Additional survey configuration
            
        Returns
        -------
        Survey
            The updated Survey object
        """
        if not excel_path and not yaml_path:
            raise ValueError("Either excel_path or yaml_path must be provided")
            
        if excel_path and yaml_path:
            raise ValueError("Provide either excel_path or yaml_path, not both")
            
        # Get existing survey
        survey = self.survey_manager.get(survey_id)
        
        if yaml_path:
            # Convert YAML to Excel first
            form_data = FormData(version)
            form_data.load_yaml(yaml_path)
            
            # Use temporary file for Excel
            temp_file = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
            excel_path = temp_file.name
            temp_file.close()
            
            try:
                form_data.save_survey(excel_path)
                return self.publish_from_excel(
                    survey=survey,
                    excel_path=excel_path,
                    media_folder=media_folder,
                    scripts_folder=scripts_folder,
                    schema_changes=schema_changes,
                    info=info
                )
            finally:
                if os.path.exists(excel_path):
                    os.unlink(excel_path)
        else:
            # Use provided Excel file
            return self.publish_from_excel(
                survey=survey,
                excel_path=excel_path,
                media_folder=media_folder,
                scripts_folder=scripts_folder,
                schema_changes=schema_changes,
                info=info
            )
    
    def get_survey(self, survey_id: str) -> Survey:
        """
        Get a specific Survey123 form by ID.
        
        Parameters
        ----------
        survey_id : str
            ID of the survey to retrieve
            
        Returns
        -------
        Survey
            The Survey object
        """
        return self.survey_manager.get(survey_id)
    
    def delete_survey(self, survey_id: str) -> bool:
        """
        Delete a Survey123 form.
        
        Parameters
        ----------
        survey_id : str
            ID of the survey to delete
            
        Returns
        -------
        bool
            True if deletion was successful
        """
        survey = self.survey_manager.get(survey_id)
        return survey.delete()


# Convenience function for quick publishing
def publish_survey(yaml_path: str,
                  title: str,
                  gis: Optional[GIS] = None,
                  **kwargs) -> Survey:
    """
    Convenience function to quickly publish a YAML survey to Survey123.
    
    Parameters
    ----------
    yaml_path : str
        Path to the YAML survey definition file
    title : str
        Title of the survey
    gis : arcgis.gis.GIS, optional
        Authenticated GIS connection
    **kwargs
        Additional arguments passed to publish_from_yaml
        
    Returns
    -------
    Survey
        The published Survey object
        
    Examples
    --------
    >>> from survey123py.publisher import publish_survey
    >>> survey = publish_survey(
    ...     yaml_path="my_survey.yaml",
    ...     title="Quick Survey",
    ...     tags=["test", "demo"]
    ... )
    """
    publisher = Survey123Publisher(gis)
    return publisher.publish_from_yaml(yaml_path, title, **kwargs)