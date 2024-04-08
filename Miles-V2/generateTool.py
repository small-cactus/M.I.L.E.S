import inspect
import json
import os
import plugin  # Make sure plugin.py is accessible and correctly formatted

def parse_docstring(docstring):
    """
    Extracts the function description, parameter descriptions, required parameters, and if it's a main function.
    """
    parts = docstring.split("\n\n")
    description = parts[0].replace("Description: ", "").strip() if parts else ""
    is_main_function = False

    param_descriptions = {}
    required_params = []

    for part in parts[1:]:  # Skip the first part as it's the general description
        part = part.strip()
        if "Main Function: Yes" in part:
            is_main_function = True
        elif part.startswith("Parameter Description for {"):
            param_info = part[len("Parameter Description for {"):].rsplit("}", 1)
            if len(param_info) == 2:
                param_name, param_desc = param_info
                param_descriptions[param_name] = param_desc[2:]  # Skip the ": " at the beginning
        elif part.startswith("Required Parameters: {"):
            required_params = [param.strip() for param in part[len("Required Parameters: {"):].rstrip("}").split(",")]

    return description, param_descriptions, required_params, is_main_function

def type_hint_to_json_type(type_hint):
    """
    Converts a Python type hint to a JSON schema data type.
    """
    type_mappings = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",  # Example of how to handle a list type hint
        dict: "object"  # Added mapping for dictionaries
        # Extend this dict to map more Python types to JSON types.
    }
    return type_mappings.get(type_hint, "string")  # Default to string if type not explicitly mapped.

def generate_tool_config(module):
    tool_configs = []
    
    for name, obj in inspect.getmembers(module):
        if inspect.isfunction(obj) and inspect.getmodule(obj) == module:
            docstring = inspect.getdoc(obj) or ""
            description, param_descriptions, required_params, is_main_function = parse_docstring(docstring)
            
            # Only generate tool configuration for functions marked as main
            if is_main_function:
                parameters = {}
                signature = inspect.signature(obj)
                for param_name, param in signature.parameters.items():
                    param_type = type_hint_to_json_type(param.annotation)
                    parameters[param_name] = {
                        "type": param_type,
                        "description": param_descriptions.get(param_name, "")
                    }

                tool_config = {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": description,
                        "parameters": {
                            "type": "object",
                            "properties": parameters,
                            "required": required_params
                        }
                    }
                }
                tool_configs.append(tool_config)
    
    return tool_configs

tool_list = generate_tool_config(plugin)

current_working_directory = os.getcwd()  # Get the current working directory
output_path = os.path.join(current_working_directory, 'plugin_tool_list.json')  # Construct the file path

# Write the tool list to a file in the current working directory
with open(output_path, 'w') as f:
    json.dump(tool_list, f, indent=4)  # Dump the tool list into the file with pretty formatting

print(f"Tool list JSON has been saved to {output_path}")
