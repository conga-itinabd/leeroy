import re
import yaml
import sys


def zero_step(file_content):
    steps_line = file_content.find('steps:')
    next_line_index = file_content.find('\n', steps_line + len('steps:'))
    spaces_count = 0
    if next_line_index != -1:
        next_line = file_content[next_line_index + 1:]
        spaces_count = len(next_line) - len(next_line.lstrip())

    spaces = ' ' * spaces_count
    insert_text = f'{spaces}mock_step:\n{2*spaces}' + \
    '- action: mock for first step comment availability\n'
    fc = file_content[:next_line_index + 1]
    return fc + insert_text + file_content[next_line_index + 1:]


def put_values(values, config):

    def replace_values(text, values):
        pat = r'{{\s*([^{}\s]+)\s*}}'

        def replace(match):
            k = match.group(1).strip()
            v = get_nested_value(values, k)
            return str(v) if v is not None else match.group(0)
        result_text = re.sub(pat, replace, text)
        return result_text

    def get_nested_value(data, keys):
        keys_list = keys.split('.')
        try:
            for key in keys_list:
                data = data[key]
            return data
        except (KeyError, TypeError):
            return None

    with open(values, 'r') as f:
        values_data = yaml.safe_load(f)
    with open(config, 'r') as f:
        config_text = f.read()
        config_text = zero_step(config_text)

    result_text = replace_values(config_text, values_data)
    try:
        yaml_config = yaml.safe_load(result_text)
        yaml_config.update(values_data['cfg'])
    except Exception as e:
        print(
            'something went wrong with values\nvalues:'
            '\n' + result_text + '\nerror:'
        )
        print(e)
        sys.exit()
    return yaml_config
