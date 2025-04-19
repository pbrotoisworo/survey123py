import argparse
from survey123py.form import FormData

def main():
    parser = argparse.ArgumentParser(description="CLI tool for Survey123 form generation.")
    parser.add_argument("-v", "--version", type=str, help="Template version to use (e.g., 3.22).")
    parser.add_argument("-i", "--input", type=str, help="Path to the YAML file containing survey data.")
    parser.add_argument("-o", "--output", type=str, help="Path to save the generated Excel file.")

    args = parser.parse_args()
    args = vars(args)  # Convert Namespace to dict for easier access

    # Load the form data and generate the Excel file
    try:
        survey = FormData(version=args.version)
        survey.load_survey(args.yaml_path)
        survey.save_survey(args.output)
        print(f"Survey123 form successfully generated and saved to {args.output}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()