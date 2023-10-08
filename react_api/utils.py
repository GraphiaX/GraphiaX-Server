import requests
import json
import uuid
import base64
import re
import os

repo_content_url = ''

def get_project_structure(repo_url):
    # access_token = 'your_github_token_here'
    # access_token = os.getenv("GITHUB_API_KEY")
    access_token = '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'
    print(repo_url)
    api_url = f'{repo_url}'
    global repo_content_url
    repo_content_url = api_url
    # api_url = f'https://api.github.com/repos/MohyiddineDilmi/air-borne/contents'
    api_url = f'{repo_url}'
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
                        "dependencies": get_dependencies(item['path'], headers),  # Add any required dependencies
                        "dependents": [],  # Add any required dependents
                        "fileSize": item['size'],
                        "description": None,
                        "parent": None,
                        "usesHooks": False,  # Set to True if the file uses hooks
                        "hooksUsed": get_hooks_used(item['path'], headers)
                    }
                    files.append(file_item)
        return json.dumps(get_network_structure(files))
        # return json.dumps(files)
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
                        "dependencies": get_dependencies(item['path'], headers),  # Add any required dependencies
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
    supported_extensions = ['.js', '.jsx', '.ts', '.tsx']
    return any(filename.endswith(ext) for ext in supported_extensions)

def get_hooks_used(file_path, headers):
    api_url = f"{repo_content_url}/{file_path}"
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
    # Extract hooks used from the file content
    import re
    pattern = r'use[A-Z][a-zA-Z]*\('
    hooks_used = re.findall(pattern, file_content)
    
    # Remove duplicates and remove the opening parentheses "("
    hooks_used = list(set([hook.rstrip('(') for hook in hooks_used]))
    
    return hooks_used

def get_dependencies(file_path, headers):
    
    # Retrieves the dependencies of a file by parsing the content.
    
    api_url = f"{repo_content_url}/{file_path}"
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        file_content = base64.b64decode(response.json()['content']).decode('utf-8')
        dependencies = extract_dependencies(file_content)
        return dependencies
    
    return []

def extract_dependencies(file_content):
    # Extract dependencies by reading the lines with import statements
    dependencies = []
    lines = file_content.split('\n')
    for line in lines:
        # if "import" not in line and line.strip() != "" :
        #     print ("ok!")
        #     break 
        if re.match(r"^\s*import\s.*\sfrom\s*['\"].*['\"];\s*$", line):
            parts = re.findall(r"[^\s{},]+", line)
            module_path = parts[-1].strip("\";'")
            for module_name in parts[1:-2]:
                if module_name != "from":
                    dependencies.append({"name": module_name, "path": module_path})
        elif re.match(r"^\s*import\s+([^\s,]+)\s*$", line):
            module_name = re.match(r"^\s*import\s+([^\s,]+)\s*$", line).group(1)
            dependencies.append({"name": module_name, "path": "./"})
        elif re.match(r"^\s*import\s+{(.*)}\s+from\s*['\"].*['\"];\s*$", line):
            parts = re.findall(r"[^\s{},]+", line)
            module_path = parts[-1].strip("\";'")
            for module_name in parts[1:-2]:
                if module_name != "from":
                    dependencies.append({"name": module_name, "path": module_path})
        elif re.match(r"^\s*import\s*['\"](.*)['\"];\s*$", line):
            module_name = re.match(r"^\s*import\s*['\"](.*)['\"];\s*$", line).group(1)
            dependencies.append({"name": module_name, "path": "./"})
    return dependencies

def get_network_structure(file):
        data = file

        nodes = [{"id": item["id"], "label": item["name"] + "\nPath: " + item["path"]} for item in data]
        nodes.append({
            "id": "0",
            "group": "mints",
            "color": {
                "border": "#25aaaa",
                "background": "#25c5df"
            },
            "shape": "circle"
        })
        edges = []
        for item in data:
            if "App.js" in item["name"]:
                edge = {"from": "0", "to": item["id"]}
                edges.append(edge)
            dependencies = item.get("dependencies", [])
            for dependency in dependencies:
                for item_search in data:
                    if dependency["name"] == item_search["name"].rsplit(".", 1)[0]:
                        edge = {"from": item["id"], "to": item_search["id"]}
                        edges.append(edge)
        result = {"nodes": nodes, "edges": edges}
        return result





