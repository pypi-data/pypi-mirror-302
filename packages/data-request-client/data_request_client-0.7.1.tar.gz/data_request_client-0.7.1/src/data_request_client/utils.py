import re


def extract_fields(json_obj, regex_list):
    def match_field(field_path):
        # If any regex matches, the field should be filtered out
        return any(re.match(regex, field_path) for regex in regex_list)

    def extract_recursive(obj, current_path=''):
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                new_path = f"{current_path}.{key}" if current_path else key
                if not match_field(new_path):  # Allow everything unless it matches a regex
                    if isinstance(value, (dict, list)):
                        extracted = extract_recursive(value, new_path)
                        if extracted:
                            result[key] = extracted
                    else:
                        result[key] = value
                elif isinstance(value, (dict, list)):
                    extracted = extract_recursive(value, new_path)
                    if extracted:
                        result[key] = extracted
            return result if result else None
        elif isinstance(obj, list):
            result = []
            for i, item in enumerate(obj):
                new_path = f"{current_path}[{i}]"
                extracted = extract_recursive(item, new_path)
                if extracted:
                    result.append(extracted)
            return result if result else None
        else:
            return obj if not match_field(current_path) else None

    return extract_recursive(json_obj)
