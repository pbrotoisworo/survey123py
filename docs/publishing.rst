Publishing Surveys
==================

Survey123Py now supports publishing surveys directly to ArcGIS Online or ArcGIS Enterprise using the ArcGIS Python API. This enables complete automation from YAML definition to published Survey123 form without requiring Survey123 Connect or Excel.

Installation
------------

To use publishing functionality, you need to install the ArcGIS Python API:

.. code-block:: bash

    pip install arcgis

Quick Start
-----------

**Command Line Interface**

Publish a survey directly from YAML:

.. code-block:: bash

    python main.py publish -i my_survey.yaml -t "Customer Feedback Survey"

**Python API**

.. code-block:: python

    from survey123py.publisher import publish_survey
    
    # Quick publish
    survey = publish_survey(
        yaml_path="my_survey.yaml",
        title="Customer Feedback Survey",
        tags=["feedback", "customer"]
    )
    
    print(f"Survey published! URL: {survey.url}")

Authentication
--------------

The publisher uses the ArcGIS Python API's authentication system. You can authenticate in several ways:

**1. Default Authentication (Recommended)**

.. code-block:: python

    from survey123py.publisher import Survey123Publisher
    
    # Uses default ArcGIS Pro or stored credentials
    publisher = Survey123Publisher()

**2. Interactive Authentication**

.. code-block:: python

    from arcgis.gis import GIS
    from survey123py.publisher import Survey123Publisher
    
    # Prompts for username/password
    gis = GIS("https://your-organization.maps.arcgis.com", "your_username")
    publisher = Survey123Publisher(gis)

**3. Token-based Authentication**

.. code-block:: python

    from arcgis.gis import GIS
    from survey123py.publisher import Survey123Publisher
    
    gis = GIS("https://your-organization.maps.arcgis.com", token="your_token")
    publisher = Survey123Publisher(gis)

CLI Commands
------------

Generate Excel Only
~~~~~~~~~~~~~~~~~~~~

Generate Excel file without publishing (original functionality):

.. code-block:: bash

    python main.py generate -i survey.yaml -o survey.xlsx -v 3.22

Publish Survey
~~~~~~~~~~~~~~

Publish survey directly to ArcGIS Online/Enterprise:

.. code-block:: bash

    python main.py publish -i survey.yaml -t "My Survey" [OPTIONS]

**Required Arguments:**

- ``-i, --input``: Path to YAML file
- ``-t, --title``: Survey title

**Optional Arguments:**

- ``-v, --version``: Template version (default: 3.22)
- ``-f, --folder``: Folder to store survey
- ``--tags``: Space-separated tags
- ``-s, --summary``: Brief summary
- ``-d, --description``: Detailed description
- ``--thumbnail``: Path to thumbnail image
- ``--media-folder``: Path to media files
- ``--scripts-folder``: Path to JavaScript files
- ``--no-web-form``: Don't create web form
- ``--no-web-map``: Don't create web map
- ``--enable-delete-protection``: Enable delete protection
- ``--enable-sync``: Enable sync capabilities
- ``--schema-changes``: Allow schema changes
- ``--keep-excel``: Keep intermediate Excel file
- ``--excel-output``: Path for Excel file (with --keep-excel)

**Example:**

.. code-block:: bash

    python main.py publish \
        -i customer_survey.yaml \
        -t "Customer Feedback Survey" \
        -f "Customer Surveys" \
        --tags feedback customer service \
        -s "Survey for collecting customer feedback" \
        --enable-sync \
        --keep-excel \
        --excel-output customer_survey.xlsx

Update Survey
~~~~~~~~~~~~~

Update an existing survey:

.. code-block:: bash

    python main.py update -s SURVEY_ID -i updated_survey.yaml

**Arguments:**

- ``-s, --survey-id``: ID of existing survey
- ``-i, --input``: Path to updated YAML file
- ``-v, --version``: Template version (default: 3.22)
- ``--media-folder``: Path to media files
- ``--scripts-folder``: Path to JavaScript files
- ``--no-schema-changes``: Don't allow schema changes


Python API
-----------

Publisher Class
~~~~~~~~~~~~~~~

The ``Survey123Publisher`` class provides full control over survey publishing:

.. code-block:: python

    from survey123py.publisher import Survey123Publisher
    
    # Initialize publisher
    publisher = Survey123Publisher()
    
    # Publish from YAML (complete workflow)
    survey = publisher.publish_from_yaml(
        yaml_path="survey.yaml",
        title="My Survey",
        folder="Surveys",
        tags=["test", "demo"],
        summary="A test survey",
        create_web_form=True,
        create_web_map=True,
        enable_sync=True
    )
    
    print(f"Published survey: {survey.id}")

Step-by-Step Publishing
~~~~~~~~~~~~~~~~~~~~~~~

For more control, you can separate the steps:

.. code-block:: python

    from survey123py.publisher import Survey123Publisher
    from survey123py.form import FormData
    
    publisher = Survey123Publisher()
    
    # Step 1: Create Excel from YAML
    form_data = FormData("3.22")
    form_data.load_yaml("survey.yaml")
    form_data.save_survey("survey.xlsx")
    
    # Step 2: Create survey item
    survey = publisher.create_survey(
        title="My Survey",
        folder="Test Surveys",
        tags=["test"]
    )
    
    # Step 3: Publish Excel to survey
    published_survey = publisher.publish_from_excel(
        survey=survey,
        excel_path="survey.xlsx",
        create_web_form=True,
        create_web_map=True
    )

Survey Management
~~~~~~~~~~~~~~~~~

.. code-block:: python

    from survey123py.publisher import Survey123Publisher
    
    publisher = Survey123Publisher()
    
    # Get specific survey
    survey = publisher.get_survey("survey_id_here")
    print(f"Survey: {survey.title}")
    
    # Update existing survey
    updated_survey = publisher.update_survey(
        survey_id="survey_id_here",
        yaml_path="updated_survey.yaml",
        schema_changes=True
    )
    
    # Delete survey
    success = publisher.delete_survey("survey_id_here")
    print(f"Deleted: {success}")

Advanced Configuration
----------------------

Survey Settings
~~~~~~~~~~~~~~~

You can pass additional configuration through the ``info`` parameter:

.. code-block:: python

    info = {
        "queryInfo": {
            "mode": "manual",  # or "automatic"
            "editEnabled": True,
            "copyEnabled": False
        },
        "displayInfo": {
            "showIntro": True,
            "showOutro": True
        }
    }
    
    survey = publisher.publish_from_yaml(
        yaml_path="survey.yaml",
        title="My Survey",
        info=info
    )

Media and Scripts
~~~~~~~~~~~~~~~~~

Include media files and JavaScript:

.. code-block:: python

    survey = publisher.publish_from_yaml(
        yaml_path="survey.yaml",
        title="Survey with Media",
        media_folder="./media",        # Folder with images, audio
        scripts_folder="./scripts"     # Folder with .js files
    )

Sync and Offline Support
~~~~~~~~~~~~~~~~~~~~~~~~

Enable sync for offline data collection:

.. code-block:: python

    survey = publisher.publish_from_yaml(
        yaml_path="survey.yaml",
        title="Offline Survey",
        enable_sync=True,
        enable_delete_protection=True
    )

Examples
--------

Complete Example
~~~~~~~~~~~~~~~~

.. code-block:: python

    from survey123py.publisher import Survey123Publisher
    from arcgis.gis import GIS
    
    # Connect to ArcGIS Online
    gis = GIS("https://myorg.maps.arcgis.com", "username", "password")
    publisher = Survey123Publisher(gis)
    
    # Publish comprehensive survey
    survey = publisher.publish_from_yaml(
        yaml_path="environmental_survey.yaml",
        title="Environmental Impact Survey",
        folder="Environmental Studies",
        tags=["environmental", "impact", "survey", "2024"],
        summary="Survey for assessing environmental impact of development projects",
        description="This survey collects data on environmental factors including air quality, water quality, noise levels, and wildlife observations.",
        thumbnail="environmental_thumbnail.jpg",
        media_folder="./survey_media",
        scripts_folder="./survey_scripts",
        create_web_form=True,
        create_web_map=True,
        enable_sync=True,
        enable_delete_protection=True,
        keep_excel=True,
        excel_output_path="environmental_survey.xlsx"
    )
    
    print(f"Survey published successfully!")
    print(f"Survey ID: {survey.id}")
    print(f"Survey Title: {survey.title}")
    print(f"Survey URL: {survey.url}")
    print(f"Web Form URL: {survey.web_form_url}")

Batch Publishing
~~~~~~~~~~~~~~~~

.. code-block:: python

    import os
    from survey123py.publisher import Survey123Publisher
    
    publisher = Survey123Publisher()
    
    # Publish multiple surveys from a directory
    yaml_dir = "./surveys"
    for filename in os.listdir(yaml_dir):
        if filename.endswith(".yaml"):
            yaml_path = os.path.join(yaml_dir, filename)
            survey_name = filename.replace(".yaml", "")
            
            try:
                survey = publisher.publish_from_yaml(
                    yaml_path=yaml_path,
                    title=survey_name.replace("_", " ").title(),
                    folder="Batch Surveys",
                    tags=["batch", "automated"]
                )
                print(f"Published: {survey.title}")
            except Exception as e:
                print(f"Failed to publish {filename}: {e}")

Error Handling
--------------

Common Issues
~~~~~~~~~~~~~

**1. Authentication Errors**

.. code-block:: python

    try:
        publisher = Survey123Publisher()
    except Exception as e:
        print(f"Authentication failed: {e}")
        # Try interactive login
        from arcgis.gis import GIS
        gis = GIS("https://your-org.maps.arcgis.com")
        publisher = Survey123Publisher(gis)

**2. Schema Validation Errors**

.. code-block:: python

    try:
        survey = publisher.publish_from_yaml(
            yaml_path="survey.yaml",
            title="My Survey"
        )
    except Exception as e:
        if "schema" in str(e).lower():
            print("Schema validation failed. Trying with schema_changes=True")
            survey = publisher.publish_from_yaml(
                yaml_path="survey.yaml",
                title="My Survey",
                schema_changes=True
            )
        else:
            raise

**3. Missing ArcGIS API**

.. code-block:: python

    try:
        from survey123py.publisher import Survey123Publisher
        publisher = Survey123Publisher()
    except ImportError:
        print("ArcGIS Python API not installed.")
        print("Install with: pip install arcgis")

Best Practices
--------------

1. **Test with Generate First**: Always test your YAML with the ``generate`` command before publishing
2. **Use Descriptive Titles**: Survey titles should be clear and descriptive
3. **Organize with Folders**: Use folders to organize related surveys
4. **Add Comprehensive Tags**: Tags help with discovery and organization
5. **Include Thumbnails**: Custom thumbnails make surveys more recognizable
6. **Enable Sync for Field Work**: Use ``enable_sync=True`` for offline data collection
7. **Keep Excel Files**: Use ``keep_excel=True`` for debugging and backup
8. **Handle Errors Gracefully**: Always wrap publishing code in try-except blocks

Troubleshooting
---------------

**Survey123 Connect Integration**

While this publishing functionality bypasses Survey123 Connect, you can still:

- Open published surveys in Survey123 Connect for visual editing
- Export from Survey123 Connect and convert back to YAML
- Use hybrid workflows combining both approaches

**Performance Considerations**

- Large surveys with many media files may take longer to publish
- Batch publishing should include delays between operations
- Consider using schema_changes=False for faster updates when structure hasn't changed

**Permissions**

Ensure your ArcGIS account has:

- Content creation privileges
- Survey123 license
- Appropriate sharing permissions for your organization