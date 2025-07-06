import argparse
import sys
import getpass
from survey123py.form import FormData

def main():
    parser = argparse.ArgumentParser(description="CLI tool for Survey123 form generation and publishing.")
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command (existing functionality)
    generate_parser = subparsers.add_parser('generate', help='Generate Excel file from YAML')
    generate_parser.add_argument("-v", "--version", type=str, default="3.22", help="Template version to use (e.g., 3.22).")
    generate_parser.add_argument("-i", "--input", type=str, required=True, help="Path to the YAML file containing survey data.")
    generate_parser.add_argument("-o", "--output", type=str, required=True, help="Path to save the generated Excel file.")
    
    # Publish command (new functionality)
    publish_parser = subparsers.add_parser('publish', help='Publish survey directly to ArcGIS Online/Enterprise')
    publish_parser.add_argument("-i", "--input", type=str, required=True, help="Path to the YAML file containing survey data.")
    publish_parser.add_argument("-t", "--title", type=str, required=True, help="Title of the survey.")
    publish_parser.add_argument("-v", "--version", type=str, default="3.22", help="Template version to use (e.g., 3.22).")
    publish_parser.add_argument("-f", "--folder", type=str, help="Folder to store the survey in.")
    publish_parser.add_argument("--tags", type=str, nargs='*', help="Tags to associate with the survey.")
    publish_parser.add_argument("-s", "--summary", type=str, help="Brief summary of the survey.")
    publish_parser.add_argument("-d", "--description", type=str, help="Detailed description of the survey.")
    publish_parser.add_argument("--thumbnail", type=str, help="Path to thumbnail image file.")
    publish_parser.add_argument("--media-folder", type=str, help="Path to folder containing media files.")
    publish_parser.add_argument("--scripts-folder", type=str, help="Path to folder containing JavaScript files.")
    publish_parser.add_argument("--no-web-form", action="store_true", help="Don't create a web form.")
    publish_parser.add_argument("--no-web-map", action="store_true", help="Don't create a web map.")
    publish_parser.add_argument("--enable-delete-protection", action="store_true", help="Enable delete protection.")
    publish_parser.add_argument("--enable-sync", action="store_true", help="Enable sync capabilities.")
    publish_parser.add_argument("--schema-changes", action="store_true", help="Allow schema changes.")
    publish_parser.add_argument("--keep-excel", action="store_true", help="Keep the intermediate Excel file.")
    publish_parser.add_argument("--excel-output", type=str, help="Path for the Excel file (if --keep-excel is used).")
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update an existing survey')
    update_parser.add_argument("-s", "--survey-id", type=str, required=True, help="ID of the existing survey to update.")
    update_parser.add_argument("-i", "--input", type=str, required=True, help="Path to the YAML file containing updated survey data.")
    update_parser.add_argument("-v", "--version", type=str, default="3.22", help="Template version to use (e.g., 3.22).")
    update_parser.add_argument("--media-folder", type=str, help="Path to folder containing media files.")
    update_parser.add_argument("--scripts-folder", type=str, help="Path to folder containing JavaScript files.")
    update_parser.add_argument("--no-schema-changes", action="store_true", help="Don't allow schema changes.")
    
    # Shared authentication arguments - add to both publish and update parsers
    def add_auth_arguments(parser):
        """Add authentication arguments to a parser."""
        auth_group = parser.add_argument_group('authentication options')
        auth_group.add_argument("--url", type=str, help="ArcGIS Online/Enterprise URL (e.g., https://myorg.maps.arcgis.com)")
        auth_group.add_argument("--username", type=str, help="ArcGIS username")
        auth_group.add_argument("--password", type=str, help="ArcGIS password")
        auth_group.add_argument("--token", type=str, help="ArcGIS access token")
        auth_group.add_argument("--cert-file", type=str, help="Certificate file for PKI authentication")
        auth_group.add_argument("--key-file", type=str, help="Key file for PKI authentication")
    
    # Convert command (Excel to YAML)
    convert_parser = subparsers.add_parser('convert', help='Convert Excel file to YAML format')
    convert_parser.add_argument("-i", "--input", type=str, required=True, help="Path to the Excel file to convert.")
    convert_parser.add_argument("-o", "--output", type=str, required=True, help="Path to save the generated YAML file.")
    convert_parser.add_argument("-v", "--version", type=str, default="3.22", help="Survey123 version to use (e.g., 3.22).")
    convert_parser.add_argument("--validate", action="store_true", help="Validate conversion by converting back to Excel.")
    
    # Add authentication to both publish and update commands
    add_auth_arguments(publish_parser)
    add_auth_arguments(update_parser)
    
    
    # If no command specified, show help
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()

    # Handle different commands
    if args.command == 'generate':
        generate_excel(args)
    elif args.command == 'publish':
        publish_survey(args)
    elif args.command == 'update':
        update_survey(args)
    elif args.command == 'convert':
        convert_excel_to_yaml(args)

def create_gis_connection(args):
    """Create a GIS connection based on authentication arguments."""
    try:
        from arcgis.gis import GIS
        
        # If no authentication parameters provided, use default
        if not any([args.url, args.username, args.password, args.token, args.cert_file]):
            return GIS("home")
        
        # Build GIS connection parameters
        gis_args = {}
        
        # Set URL (default to ArcGIS Online if not provided)
        if args.url:
            gis_args['url'] = args.url
        elif args.username or args.password or args.token:
            gis_args['url'] = "https://www.arcgis.com"
        
        # Handle different authentication methods
        if args.token:
            # Token authentication
            gis_args['token'] = args.token
        elif args.cert_file:
            # PKI authentication
            gis_args['cert_file'] = args.cert_file
            if args.key_file:
                gis_args['key_file'] = args.key_file
        elif args.username:
            # Username/password authentication
            gis_args['username'] = args.username
            if args.password:
                gis_args['password'] = args.password
            else:
                # Prompt for password if username provided but password not
                gis_args['password'] = getpass.getpass(f"Password for {args.username}: ")
        
        return GIS(**gis_args)
        
    except ImportError:
        raise ImportError("ArcGIS Python API is required for authentication. Install with: pip install arcgis")
    except Exception as e:
        raise RuntimeError(f"Authentication failed: {e}")

def generate_excel(args):
    """Generate Excel file from YAML."""
    try:
        survey = FormData(version=args.version)
        survey.load_yaml(args.input)  # Fixed: was args.yaml_path
        survey.save_survey(args.output)
        print(f"Survey123 form successfully generated and saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def convert_excel_to_yaml(args):
    """Convert Excel file to YAML format."""
    try:
        from survey123py.converter import ExcelToYamlConverter
        
        converter = ExcelToYamlConverter(args.version)
        
        print(f"Converting Excel file '{args.input}' to YAML...")
        yaml_data = converter.convert_excel_to_yaml(args.input, args.output)
        
        print(f"✓ Successfully converted to '{args.output}'")
        
        # Show summary
        survey_count = len(yaml_data.get('survey', []))
        choices_count = len(yaml_data.get('choices', []))
        settings_count = len(yaml_data.get('settings', {}))
        
        print(f"  - Survey questions: {survey_count}")
        print(f"  - Choice options: {choices_count}")
        print(f"  - Settings: {settings_count}")
        
        # Validate conversion if requested
        if args.validate:
            print("\nValidating conversion...")
            validation_results = converter.validate_conversion(args.input, args.output)
            
            if validation_results['success']:
                print("✓ Validation passed - conversion is accurate")
            else:
                print("⚠ Validation warnings:")
                for sheet, issue in validation_results['differences'].items():
                    print(f"  - {sheet}: {issue}")
                
                for warning in validation_results['warnings']:
                    print(f"  - {warning}")
        
    except ImportError as e:
        print(f"Error: Missing required dependencies: {e}")
        print("Install with: pip install pandas openpyxl")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def publish_survey(args):
    """Publish survey directly to ArcGIS Online/Enterprise."""
    try:
        from survey123py.publisher import Survey123Publisher
        
        # Create GIS connection with authentication
        gis = create_gis_connection(args)
        publisher = Survey123Publisher(gis)
        
        # Prepare arguments
        publish_args = {
            'yaml_path': args.input,
            'title': args.title,
            'version': args.version,
            'folder': args.folder,
            'tags': args.tags,
            'summary': args.summary,
            'description': args.description,
            'thumbnail': args.thumbnail,
            'media_folder': args.media_folder,
            'scripts_folder': args.scripts_folder,
            'create_web_form': not args.no_web_form,
            'create_web_map': not args.no_web_map,
            'enable_delete_protection': args.enable_delete_protection,
            'enable_sync': args.enable_sync,
            'schema_changes': args.schema_changes,
            'keep_excel': args.keep_excel,
            'excel_output_path': args.excel_output,
        }
        
        # Remove None values
        publish_args = {k: v for k, v in publish_args.items() if v is not None}
        
        survey = publisher.publish_from_yaml(**publish_args)
        
        print(f"Survey123 form successfully published!")
        print(f"Survey ID: {survey.id}")
        print(f"Survey Title: {survey.title}")
        print(f"Survey URL: {survey.url}")
        
    except ImportError:
        print("Error: ArcGIS Python API is required for publishing functionality.")
        print("Install with: pip install arcgis")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def convert_excel_to_yaml(args):
    """Convert Excel file to YAML format."""
    try:
        from survey123py.converter import ExcelToYamlConverter
        
        converter = ExcelToYamlConverter(args.version)
        
        print(f"Converting Excel file '{args.input}' to YAML...")
        yaml_data = converter.convert_excel_to_yaml(args.input, args.output)
        
        print(f"✓ Successfully converted to '{args.output}'")
        
        # Show summary
        survey_count = len(yaml_data.get('survey', []))
        choices_count = len(yaml_data.get('choices', []))
        settings_count = len(yaml_data.get('settings', {}))
        
        print(f"  - Survey questions: {survey_count}")
        print(f"  - Choice options: {choices_count}")
        print(f"  - Settings: {settings_count}")
        
        # Validate conversion if requested
        if args.validate:
            print("\nValidating conversion...")
            validation_results = converter.validate_conversion(args.input, args.output)
            
            if validation_results['success']:
                print("✓ Validation passed - conversion is accurate")
            else:
                print("⚠ Validation warnings:")
                for sheet, issue in validation_results['differences'].items():
                    print(f"  - {sheet}: {issue}")
                
                for warning in validation_results['warnings']:
                    print(f"  - {warning}")
        
    except ImportError as e:
        print(f"Error: Missing required dependencies: {e}")
        print("Install with: pip install pandas openpyxl")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def update_survey(args):
    """Update an existing survey."""
    try:
        from survey123py.publisher import Survey123Publisher
        
        # Create GIS connection with authentication
        gis = create_gis_connection(args)
        publisher = Survey123Publisher(gis)
        
        survey = publisher.update_survey(
            survey_id=args.survey_id,
            yaml_path=args.input,
            version=args.version,
            media_folder=args.media_folder,
            scripts_folder=args.scripts_folder,
            schema_changes=not args.no_schema_changes
        )
        
        print(f"Survey123 form successfully updated!")
        print(f"Survey ID: {survey.id}")
        print(f"Survey Title: {survey.title}")
        
    except ImportError:
        print("Error: ArcGIS Python API is required for update functionality.")
        print("Install with: pip install arcgis")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def convert_excel_to_yaml(args):
    """Convert Excel file to YAML format."""
    try:
        from survey123py.converter import ExcelToYamlConverter
        
        converter = ExcelToYamlConverter(args.version)
        
        print(f"Converting Excel file '{args.input}' to YAML...")
        yaml_data = converter.convert_excel_to_yaml(args.input, args.output)
        
        print(f"✓ Successfully converted to '{args.output}'")
        
        # Show summary
        survey_count = len(yaml_data.get('survey', []))
        choices_count = len(yaml_data.get('choices', []))
        settings_count = len(yaml_data.get('settings', {}))
        
        print(f"  - Survey questions: {survey_count}")
        print(f"  - Choice options: {choices_count}")
        print(f"  - Settings: {settings_count}")
        
        # Validate conversion if requested
        if args.validate:
            print("\nValidating conversion...")
            validation_results = converter.validate_conversion(args.input, args.output)
            
            if validation_results['success']:
                print("✓ Validation passed - conversion is accurate")
            else:
                print("⚠ Validation warnings:")
                for sheet, issue in validation_results['differences'].items():
                    print(f"  - {sheet}: {issue}")
                
                for warning in validation_results['warnings']:
                    print(f"  - {warning}")
        
    except ImportError as e:
        print(f"Error: Missing required dependencies: {e}")
        print("Install with: pip install pandas openpyxl")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()