import requests
import json
import uuid
import base64

def get_project_structure():
    access_token = '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'
    api_url = f'https://api.github.com/repos/MohyiddineDilmi/air-borne/contents'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        # Extract the project structure from the response JSON
        contents = response.json()
        files = []
        
        for item in contents:
            if item['type'] == 'dir':
                # If the item is a directory, recursively retrieve the files within it
                files.extend(get_files_from_directory(item, headers))
            else:
                # If the item is a file, check if it has a JavaScript or CSS extension
                if has_supported_extension(item['name']):
                    file_item = {
                        "id": str(uuid.uuid4()),
                        "name": item['name'],
                        "path": item['path'],
                        "type": "functional",  # You can modify the type as per your needs
                        "dependencies": [],  # Add any required dependencies
                        "dependents": [],  # Add any required dependents
                        "fileSize": item['size'],
                        "description": None,
                        "parent": None,
                        "usesHooks": False,  # Set to True if the file uses hooks
                        "hooksUsed": get_hooks_used(item['path'], headers)
                    }
                    files.append(file_item)
        
        return json.dumps(files)
    else:
        # Handle the case when the repository cannot be accessed
        return None

def get_files_from_directory(directory, headers):
    """
    Recursively retrieves the files within a directory.
    """
    files = []
    
    api_url = directory['url']
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        contents = response.json()
        
        for item in contents:
            if item['type'] == 'dir':
                # If the item is a subdirectory, recursively retrieve the files within it
                files.extend(get_files_from_directory(item, headers))
            else:
                # If the item is a file, check if it has a JavaScript or CSS extension
                if has_supported_extension(item['name']):
                    file_item = {
                        "id": str(uuid.uuid4()),
                        "name": item['name'],
                        "path": item['path'],
                        "type": "functional",  # You can modify the type as per your needs
                        "dependencies": [],  # Add any required dependencies
                        "dependents": [],  # Add any required dependents
                        "fileSize": item['size'],
                        "description": None,
                        "parent": directory['name'],
                        "usesHooks": False,  # Set to True if the file uses hooks
                        "hooksUsed": get_hooks_used(item['path'], headers)
                    }
                    files.append(file_item)
    
    return files

def has_supported_extension(filename):
    """
    Checks if the given filename has a supported extension.
    """
    supported_extensions = ['.js', '.jsx', '.ts', '.tsx', '.css']
    return any(filename.endswith(ext) for ext in supported_extensions)

def get_hooks_used(file_path, headers):
    api_url = f"https://api.github.com/repos/MohyiddineDilmi/air-borne/contents/{file_path}"
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        file_content = base64.b64decode(response.json()['content']).decode('utf-8')
        hooks_used = extract_hooks_used(file_content)
        
        return {
            "hooksUsed": hooks_used,
            "usesHooks": len(hooks_used) > 0  # Update usesHooks value to True if there are hooks used
        }
    
    return {
        "hooksUsed": [],
        "usesHooks": False
    }

def extract_hooks_used(file_content):
    # Extract hooks used from the file content using a regular expression or any other method
    
    # Example implementation using regex
    import re
    pattern = r'use[A-Z][a-zA-Z]*\('
    hooks_used = re.findall(pattern, file_content)
    
    # Remove duplicates and remove the opening parentheses "("
    hooks_used = list(set([hook.rstrip('(') for hook in hooks_used]))
    
    return hooks_used

