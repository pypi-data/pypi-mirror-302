"""
Client Module
"""
import os
import math
import time
import json

from pathlib import Path
import zipfile
import requests
import configparser


from tqdm import tqdm
from .utils import print_tabular, format_time, validate_coco_format, flatten_directory, subsample_video_to_frames
from .exceptions import CIException, CIInvalidRequest, CIExistingDatasetException

import sys

class CortalInsightClient:
    """
    A class to interact with the Cortal Insight API
    """
    def __init__(self):
        self.base_url = 'https://server.cortalinsight.com'
        self.api_key = None
        self.config_dir = Path.home() / '.cortalinsight'
        self.config_file = 'config.ini'
        self.config_path = self.config_dir / self.config_file
        self.ensure_config_directory_exists()
        self.load_api_key()

    def ensure_config_directory_exists(self):
        """
        Ensure that the .cortalinsight directory and config file exist
        """
        if not self.config_dir.exists():
            print(f"Creating configuration directory at: {self.config_dir}")
            self.config_dir.mkdir()
        if not self.config_path.exists():
            print(f"Creating a new configuration file at: {self.config_path}")
            self.save_api_key('')  # Create an empty config file with placeholder

    def load_api_key(self):
        """
        Load the API key from the configuration file.
        """
        config = configparser.ConfigParser()
        config.read(self.config_path)
        try:
            self.api_key = config['DEFAULT']['API_KEY']
        except KeyError:
            print(f"API key not found in {self.config_path}. Set it with set_api_key().")

    def save_api_key(self, api_key):
        """
        Save the API key to the configuration file.
        """
        config = configparser.ConfigParser()
        config['DEFAULT'] = {'API_KEY': api_key}
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)
        print(f"API key saved to configuration file at: {self.config_path}")

    def set_api_key(self, api_key):
        """
        Manually set the API key and save it to the configuration file
        """
        if not api_key:
            raise CIInvalidRequest("API key is required.", 400)
        self.api_key = api_key
        self.save_api_key(api_key)
        print("API key set and saved successfully.")

    def _request(self, method, headers, path, data=None):
        if not self.api_key:
            raise CIInvalidRequest("API key has not been set.", 401)

        url = f"{self.base_url}{path}"

        try:
            response = requests.request(method, url, headers=headers, json=data, timeout=5)

            if response.status_code == 204:
                return None
            else:
                return response.json()

        except requests.HTTPError as http_err:
            if http_err.response.status_code == 500:
                error_message = "Internal Server Error occurred while making the request."
                raise CIException(error_message, 500)
            else:
                raise CIException(http_err.response.text, http_err.response.status_code)

        except requests.exceptions.RequestException as req_err:
            error_message = str(req_err)
            raise CIException(error_message, 500)

        except Exception as err:
            error_message = str(err)
            raise CIException(error_message, 500)

    def get_dataset_by_id(self, dataset_id):
        """
        GET a dataset by id
        """
        try:
            headers = {'x-api-key': self.api_key }
            response = self._request("GET", headers, f"/datasets/{dataset_id}")
            print(json.dumps(response,indent=4))
            return response

        except CIExistingDatasetException as ci_err:
            print(f"CIException: {ci_err}")
            pass

        except Exception:
            print(f"Unexpected error: Dataset not available")

    def list_datasets(self):
        """
        GET a list of datasets that belong to the user's organization
        """
        headers = {'x-api-key': self.api_key }
        response = self._request("GET", headers, "/datasets/list/1")
        print_tabular(response)
        return response

    def create_dataset(self, dataset_name, task_type, file_type='Images'):
        """
        POST a new dataset
        """
        headers = {
                    'x-api-key': self.api_key ,
                    'Content-Type': 'application/json'}
        data = {
                    "version": "1.0",
                    "dataSetName": str(dataset_name),
                    "task": task_type,
                    "fileType": file_type}
        response = self._request("POST", headers, "/datasets/create", data)

        if 'errors' in response:
            print(response)
            raise Exception
        print(f'Dataset: {dataset_name} created.')
        return

    def delete_dataset(self, dataset_id):
        """
        DELETE a dataset by id
        """
        try:
            headers = {'x-api-key': self.api_key }
            response = self._request("DELETE", headers, f"/datasets/{dataset_id}")
            if 'errors' in response:
                print(response)
                raise Exception
            print(f'Dataset id: {dataset_id} deleted.')
            return response

        except CIExistingDatasetException as ci_err:
            print(f"CIException: {ci_err}")
            pass

        except Exception:
            print(f"Unexpected error: Dataset not available")

    def delete_metadata(self, dataset_id):
        """
        DELETE metadata associated with dataset by id
        """
        try:
            headers = {'x-api-key': self.api_key }
            response = self._request("DELETE", headers, f"/datasets/{dataset_id}/metadata")
            print(f'Metadata for dataset: {dataset_id} deleted.')
            return response

        except CIExistingDatasetException as ci_err:
            print(f"CIException: {ci_err}")
            pass

        except Exception:
            print(f"Unexpected error: Dataset not available")


    def initiate_multipart_upload(self, filename, file_size, dataset_id, file_type):
        """
        INITIATE a multipart upload for images
        """
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': "application/json"}

        content_type = 'application/zip'
        data = { 
                    "dataSetId": str(dataset_id),
                    "filename": filename,
                    "fileSize": file_size,
                    "contentType": content_type,
                    "fileType": file_type
                    
                }

        return self._request("POST", headers, "/files/upload", data)

    def initiate_metadata_multipart_update(self, filename, file_size, dataset_id):
        """
        INITIATE a multipart upload for metadata
        """
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': "application/json"}

        content_type = 'application/json'
        data = {   
                    "filename": filename,
                    "fileSize": file_size,
                    "contentType": content_type
                }

        return self._request("PUT", headers, f"/datasets/{dataset_id}/metadata/update", data)


    def get_presigned_url(self, dataset_id, filename, part_number, upload_id, file_type):
        """
        PRE-SIGNED URL for each part of upload
        """
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': "application/json"}

        data = {
                    "dataSetId": str(dataset_id),
                    "filename": filename,
                    "partNumber": part_number,
                    "uploadId": upload_id,
                    "fileType": file_type
                }

        return self._request("POST", headers, "/files/upload-part", data)

    def complete_upload(self, dataset_id, filename, upload_id, parts, file_type):
        """
        FINISH multi-part upload
        """
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': "application/json"}

        data = {
                    "dataSetId":  str(dataset_id)   ,
                    "filename": filename,
                    "parts": parts,
                    "uploadId": upload_id,
                    "fileType": file_type
                }

        return self._request("POST", headers, "/files/complete-upload", data)


    def upload_part(self, presigned_url, part_data):
        """
        UPLOAD part in multi-part upload
        """
        response = requests.put(presigned_url, data=part_data)
        return response.headers['ETag']

    def zip_directory(self, directory_path, zip_path):
        """
        ZIP IMAGES in directory to prepare for upload
        """
        # Move all files to the main directory first
        flatten_directory(directory_path)

        # Get a list of all files to be zipped for the progress bar
        file_paths = []
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_paths.append(os.path.join(root, file))

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in tqdm(file_paths, desc='Zipping', unit='file'):
                zipf.write(file, os.path.relpath(file, directory_path))
        return zip_path

    def validate_metadata(self, file_path):
        return validate_coco_format(file_path)

    def upload_images_from_dir(self, dataset_id, directory_path):
        """
        UPLOAD IMAGES from directory
        """
        # Zip the directory first
        zip_path = 'images.zip'
        self.zip_directory(directory_path, zip_path)

        complete_response = self.upload_zip_file(dataset_id, zip_path)
        print('Upload completed.')
        return complete_response

    def upload_metadata_file(self, dataset_id, file_path):
        """
        UPLOAD METADATA file
        """

        if not validate_coco_format(file_path):
            print(f'Upload failed Metadata not in correct format.')
            return None


        # Get the file size of the zip
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        max_retries = 3  # Maximum number of retries for each part

        # Initiate multipart upload
        initiate_response = self.initiate_multipart_upload(filename, file_size, dataset_id, file_type='METADATA')

        if initiate_response['method'] == 'PUT':
            print('Uploading...')
            start_time = time.time()
            presigned_url = initiate_response['url']
            with open(file_path, 'rb') as f:
                data = f.read()
            e_tag = self.upload_part(presigned_url, data)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f'Metadata upload completed in {format_time(elapsed_time)}.')
            return e_tag

        upload_id = initiate_response['uploadId']
        print('Init metadata multi-part upload')
        # Calculate how many parts we'll need
        part_size = 50 * 1024 * 1024  # 50MB per part
        total_parts = math.ceil(file_size / part_size)

        # Store the ETags for each part
        parts = []

        start_time = time.time()
        with open(file_path, 'rb') as f:
            for part_number in tqdm(range(1, total_parts + 1), desc='Uploading', unit='part'):
                for attempt in range(max_retries):
                    try:
                        # Calculate the byte range of the part
                        start_byte = (part_number - 1) * part_size
                        end_byte = min(start_byte + part_size, file_size)
                        f.seek(start_byte)
                        part_data = f.read(end_byte - start_byte)

                        # Get the presigned URL
                        presigned_url_response = self.get_presigned_url(dataset_id,
                                                        filename, part_number, upload_id, file_type='METADATA')
                        presigned_url = presigned_url_response['url']

                        # Uploading part
                        e_tag = self.upload_part(presigned_url, part_data)
                        parts.append({'ETag': e_tag, 'PartNumber': part_number})
                        break
                    
                    except Exception as e:
                        print(f"Attempt {attempt + 1} for part {part_number} failed: {e}")
                        if attempt < max_retries - 1:
                            print("Retrying part...")
                            time.sleep(3 ** attempt)  # Exponential backoff
                        else:
                            print(f"Maximum retry attempts reached for part {part_number}. Upload failure")
                            return None

        # Complete the upload
        complete_response = self.complete_upload(dataset_id, filename, upload_id, parts, file_type='METADATA')
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Metadata upload completed in {format_time(elapsed_time)}.')
        return complete_response


    def update_metadata_file(self, dataset_id, file_path):
        """
        UPLOAD METADATA file
        """

        # Get the file size of the zip
        file_size = os.path.getsize(file_path)
        filename = os.path.basename(file_path)
        max_retries = 3  # Maximum number of retries for each part

        # Initiate multipart upload
        initiate_response = self.initiate_metadata_multipart_update(filename, file_size, dataset_id)

        if initiate_response['method'] == 'PUT':
            print('Uploading...')
            start_time = time.time()
            presigned_url = initiate_response['url']
            with open(file_path, 'rb') as f:
                data = f.read()
            e_tag = self.upload_part(presigned_url, data)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f'Metadata upload completed in {format_time(elapsed_time)}.')
            return e_tag

        upload_id = initiate_response['uploadId']
        print('Init metadata multi-part upload')
        # Calculate how many parts we'll need
        part_size = 50 * 1024 * 1024  # 50MB per part
        total_parts = math.ceil(file_size / part_size)

        # Store the ETags for each part
        parts = []

        start_time = time.time()
        with open(file_path, 'rb') as f:
            for part_number in tqdm(range(1, total_parts + 1), desc='Uploading', unit='part'):
                for attempt in range(max_retries):
                    try:
                        # Calculate the byte range of the part
                        start_byte = (part_number - 1) * part_size
                        end_byte = min(start_byte + part_size, file_size)
                        f.seek(start_byte)
                        part_data = f.read(end_byte - start_byte)

                        # Get the presigned URL
                        presigned_url_response = self.get_presigned_url(dataset_id,
                                                        filename, part_number, upload_id, file_type='METADATA')
                        presigned_url = presigned_url_response['url']

                        # Uploading part
                        e_tag = self.upload_part(presigned_url, part_data)
                        parts.append({'ETag': e_tag, 'PartNumber': part_number})
                        break
                    
                    except Exception as e:
                        print(f"Attempt {attempt + 1} for part {part_number} failed: {e}")
                        if attempt < max_retries - 1:
                            print("Retrying part...")
                            time.sleep(3 ** attempt)  # Exponential backoff
                        else:
                            print(f"Maximum retry attempts reached for part {part_number}. Upload failure")
                            return None

        # Complete the upload
        complete_response = self.complete_upload(dataset_id, filename, upload_id, parts, file_type='METADATA')
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Metadata upload completed in {format_time(elapsed_time)}.')
        return complete_response

    def upload_video(self, dataset_id, file_path, sub_sample_rate):
        """
        UPLOAD VIDEO FILE from 
        """

        print('Subsampling video frames...')
        subsample_video_to_frames(file_path, sub_sample_rate=sub_sample_rate)

        directory_path = os.path.abspath('video_output')

        self.upload_images_from_dir(dataset_id, directory_path)
        sys.exit()
        print('Video upload completed.')



    def upload_images_and_metadata(self, dataset_id, directory_path, file_path):
        """
        UPLOAD IMAGES & METADATA from directory
        """
        # Zip the directory first
        zip_path = 'images.zip'
        self.zip_directory(directory_path, zip_path)

        complete_response = self.upload_zip_file(dataset_id, zip_path)
        print('Image upload completed.')
        

        complete_response = upload_metadata_file(self, dataset_id, file_path)
        print('Metadata upload completed.')
        return complete_response
        
    def upload_zip_file(self, dataset_id, zip_path):
        """
        UPLOAD ZIP from directory
        """

        # Get the file size of the zip
        file_size = os.path.getsize(zip_path)
        filename = os.path.basename(zip_path)

        max_retries = 3  # Maximum number of retries for each part

        # Initiate multipart upload
        initiate_response = self.initiate_multipart_upload(filename, file_size, dataset_id, file_type='IMAGES')

        if initiate_response['method'] == 'PUT':
            print('Uploading...')
            start_time = time.time()
            presigned_url = initiate_response['url']
            with open(zip_path, 'rb') as f:
                data = f.read()
            e_tag = self.upload_part(presigned_url, data)
            end_time = time.time()
            elapsed_time = end_time - start_time
            print(f'Upload completed in {format_time(elapsed_time)}.')
            return e_tag

        upload_id = initiate_response['uploadId']
        print('Init multi-part upload')
        # Calculate how many parts we'll need
        part_size = 50 * 1024 * 1024  # 50MB per part
        total_parts = math.ceil(file_size / part_size)

        # Store the ETags for each part
        parts = []

        start_time = time.time()
        with open(zip_path, 'rb') as f:
            for part_number in tqdm(range(1, total_parts + 1), desc='Uploading', unit='part'):
                for attempt in range(max_retries):
                    try:
                        # Calculate the byte range of the part
                        start_byte = (part_number - 1) * part_size
                        end_byte = min(start_byte + part_size, file_size)
                        f.seek(start_byte)
                        part_data = f.read(end_byte - start_byte)

                        # Get the presigned URL
                        presigned_url_response = self.get_presigned_url(dataset_id,
                                                        filename, part_number, upload_id, file_type='IMAGES')
                        presigned_url = presigned_url_response['url']

                        # Uploading part
                        e_tag = self.upload_part(presigned_url, part_data)
                        parts.append({'ETag': e_tag, 'PartNumber': part_number})
                        break
                    
                    except Exception as e:
                        print(f"Attempt {attempt + 1} for part {part_number} failed: {e}")
                        if attempt < max_retries - 1:
                            print("Retrying part...")
                            time.sleep(3 ** attempt)  # Exponential backoff
                        else:
                            print(f"Maximum retry attempts reached for part {part_number}. Upload failure")
                            return None

        # Complete the upload
        complete_response = self.complete_upload(dataset_id, filename, upload_id, parts, file_type='IMAGES')
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f'Upload completed in {format_time(elapsed_time)}.')
        return complete_response

    def curate(self, dataset_id):
        print('Sending trigger to curate from dataset...')
        ## TO-DO
        
        print("Trigger sent.")

