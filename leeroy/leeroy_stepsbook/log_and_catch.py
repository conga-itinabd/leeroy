import re


# get logs
def string_splitter(template_of_log):
    pattern = r'(\*{5}|#(\*{4}|(\*{3}#)|(#\*{3})))'
    match = re.search(pattern, template_of_log)

    if match:
        start, end = match.span()
        substring = template_of_log[:start]
        signs = template_of_log[start:end]
        substring2 = template_of_log[end:]
        return substring, signs, substring2
    else:
        return '', '', ''


def finder(text, substring, substring2):
    start = text.find(substring)
    end = text.find(substring2, start + len(substring2))

    if start != -1 and end != -1:
        return text[start:end + len(substring2)]
    else:
        return None


def get_log(text, template_of_log):
    substring, signs, substring2 = string_splitter(template_of_log)
    log = finder(text, substring, substring2)
    try:
        if signs == '*****':
            return log
        elif signs == '#****':
            return log.replace(substring, '')
        elif signs == '****#':
            return log.replace[:len(log) - len(substring2)]
        elif signs == '#***#':
            log = log.replace(substring, '')
            return log.replace[:len(log) - len(substring2)]
    except:
        return "unable to retrieve log"


def get_step_logs(text, step_logs_dict):
    logs = {}
    for log_name, template_of_log in step_logs_dict.items():
        log = get_log(text, template_of_log)
        logs[log_name] = log
    return logs


# get catches
def get_step_catches(text, step_catches_array):
    catches = {}
    for catch in step_catches_array:
        count_of_catches = text.count(catch)
        catches[catch] = count_of_catches
    return catches


# put logs and catches
def status_templater(input_string):
    pattern = r'\(\( (\w+)\.(\w+)\.(\w+) \)\)'
    match = re.search(pattern, input_string)
    if match:
        template = match.group(0)
        status_type = match.group(1)
        step_name = match.group(2)
        want = match.group(3)
        return template, status_type, step_name, want
    else:
        return None, None, None, None


def step_changer(step, all_statuses):
    if isinstance(step, dict):
        for key, value in step.items():
            step[key] = step_changer(value, all_statuses)
        return step
    elif isinstance(step, list):
        return [step_changer(item, all_statuses) for item in step]
    elif isinstance(step, str):
        template, status_type, step_name, want = status_templater(step)
        if template:
            while template and (
                status_type == 'log' or status_type == 'catch'
            ):

                template, status_type, step_name, want = status_templater(step)
                if template:
                    if (
                        step_name in all_statuses
                        and status_type in all_statuses[step_name]
                        and want in all_statuses[step_name][status_type]
                    ):
                        new_substr = all_statuses[step_name][status_type][want]
                    else:
                        new_substr = '(( Error. There is no such log/catch ))'
                    step = step.replace(template, str(new_substr))
                    (
                        template, status_type, step_name, want
                    ) = status_templater(step)

                else:
                    break

    return step
