"""
Main Module 
"""
import argparse
import sys
from cortalinsight.api import CortalInsightClient
from cortalinsight.exceptions import CIException, CIInvalidRequest


__version__ = '0.1.5'

class VerticalHelpFormatter(argparse.HelpFormatter):
    def __init__(self, prog, max_help_position=40, width=100):
        super().__init__(prog, max_help_position=max_help_position, width=width)

    def _format_action_invocation(self, action):
        """
        Format the display of each argument vertically.
        """
        parts = []

        if action.option_strings:
            parts.extend(action.option_strings)
        if action.nargs != 0:
            default = self._get_default_metavar_for_optional(action) if action.option_strings else self._get_default_metavar_for_positional(action)
            parts.append(self._format_args(action, default))
        
        return '\n'.join(parts)

    def _split_lines(self, text, width):
        """
        Override the method to prevent line wrapping based on width.
        """
        return text.splitlines()

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # Custom error message
        print(f"Custom error message: {message}")
        sys.exit(1)

def setup_arg_parser():
    """
    Set up and return the argument parser
    """
    parser = CustomArgumentParser(
        description="Cortal Insight CLI Tool",
        formatter_class=VerticalHelpFormatter,
        add_help=False
    )
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message')

    subparsers = parser.add_subparsers(dest='command', required=True, title='Available commands')

    # Subparser for each command
    subparsers.add_parser('setup', help='Setup your API key')
    subparsers.add_parser('list_datasets', help='Get all datasets')

    get_parser = subparsers.add_parser('get_dataset', help='Get a dataset by ID')
    get_parser.add_argument('id', type=str, help='Dataset ID')

    create_parser = subparsers.add_parser('create_dataset', help='Create a dataset')
    create_parser.add_argument('name', type=str, help='Name of the new dataset')
    create_parser.add_argument('--file_type', type=str, help='File type in dataset', default='Images')

    delete_parser = subparsers.add_parser('delete_dataset', help='Delete a dataset')
    delete_parser.add_argument('id', type=str, help='Dataset ID to delete')

    delete_metadata_parser = subparsers.add_parser('delete_metadata', help='Delete metdata of a dataset')
    delete_metadata_parser.add_argument('id', type=str, help='Dataset ID to delete')

    upload_parser = subparsers.add_parser('upload_images_from_dir', help='Upload images from directory')
    upload_parser.add_argument('id', type=str, help='Dataset ID to ingest data')
    upload_parser.add_argument('directory_path', type=str, help='Directory to upload images from')

    upload_video_parser = subparsers.add_parser('upload_video', help='Upload video file')
    upload_video_parser.add_argument('id', type=str, help='Dataset ID to ingest data')
    upload_video_parser.add_argument('file_path', type=str, help='File to upload video from')
    upload_video_parser.add_argument('--sub_sample_rate', type=int, help='Interval for subsampling', default=15)

    upload_metadata_parser = subparsers.add_parser('upload_metadata', help='Upload metadata file')
    upload_metadata_parser.add_argument('id', type=str, help='Dataset ID to ingest metadata')
    upload_metadata_parser.add_argument('file_path', type=str, help='File to upload metadata from')

    update_metadata_parser = subparsers.add_parser('update_metadata', help='Update metadata file')
    update_metadata_parser.add_argument('id', type=str, help='Dataset ID to update metadata')
    update_metadata_parser.add_argument('file_path', type=str, help='File to upload metadata from')

    update_images_and_metadata_parser = subparsers.add_parser('upload_images_and_metadata', help='Update metadata file')
    update_images_and_metadata_parser.add_argument('id', type=str, help='Dataset ID to update metadata')
    update_images_and_metadata_parser.add_argument('directory_path', type=str, help='Directory to upload images from')
    update_images_and_metadata_parser.add_argument('file_path', type=str, help='File to upload metadata from')

    upload_zip_parser = subparsers.add_parser('upload_zip', help='Upload zip from directory')
    upload_zip_parser.add_argument('id', type=str, help='Dataset ID to ingest data')
    upload_zip_parser.add_argument('zip_path', type=str, help='Directory to upload images from')

    curate_parser = subparsers.add_parser('curate', help='Curate ingested dataset')
    curate_parser.add_argument('id', type=str, help='Dataset ID to ingest data')

    validate_parser = subparsers.add_parser('validate_metadata', help='Validate metadata format')
    validate_parser.add_argument('file_path', type=str, help='File to validate metadata from')
    return parser

def process_commands(args, ci_api):
    """
    Process the given command
    """

    try:
        if args.command == 'setup':
            setup_api_key(ci_api)
        elif args.command == 'get_dataset':
            response = ci_api.get_dataset_by_id(args.id)
        elif args.command == 'list_datasets':
            response = ci_api.list_datasets()
        elif args.command == 'create_dataset':
            task_type = input_task_type()
            response = ci_api.create_dataset(args.name, task_type, args.file_type)
        elif args.command == 'delete_dataset':
            response = ci_api.delete_dataset(args.id)
        elif args.command == 'delete_metadata':
            response = ci_api.delete_metadata(args.id)
        elif args.command == 'upload_images_from_dir':
            response = ci_api.upload_images_from_dir(args.id, args.directory_path)
        elif args.command == 'upload_video':
            response = ci_api.upload_video(args.id, args.file_path, args.sub_sample_rate)
        elif args.command == 'upload_metadata':
            response = ci_api.upload_metadata_file(args.id, args.file_path)
        elif args.command == 'update_metadata':
            response = ci_api.update_metadata_file(args.id, args.file_path)
        elif args.command == 'upload_zip':
            response = ci_api.upload_zip_file(args.id, args.zip_path)
        elif args.command == 'upload_images_and_metadata':
            response = ci_api.upload_images_and_metadata(args.id, args.directory_path, args.file_path)
        elif args.command == 'validate_metadata':
            response = ci_api.validate_metadata(args.file_path)
        elif args.command == 'curate':
            response = ci_api.curate(args.id)
        else:
            raise Exception(f"Unknown command: {args.command}", 400)
            sys.exit(1)

    except (CIException, CIInvalidRequest) as e:
        print(f"API error occurred: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


def setup_api_key(api_client):
    api_key = input("Please enter your API key: ")
    api_client.set_api_key(api_key)
    print("API key has been set up successfully.")

def input_task_type():
    """
    Prompt for the task type
    """
    task_type = input("Please choose task type: (1 - Classification / 2 - Object detection)\nEnter choice: ")
    task_map = {'1': 'classification', '2': 'detection'}
    if task_type in task_map:
        return task_map[task_type]
    else:
        raise ValueError("Invalid choice. Please enter 1 for Classification or 2 for Object detection.")


def main():
    parser = setup_arg_parser()

    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(1)

    ci_api = CortalInsightClient()
    process_commands(args, ci_api)

if __name__ == '__main__':
    main()
