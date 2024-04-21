from dataclasses import dataclass, field
from typing import List, Mapping


@dataclass
class StepData:
    step: str
    url: str = ''
    parameters: Mapping[str, str] = field(default_factory=dict)
    action: str = ''
    wait_end: bool = False
    iterations: str = ''
    catch: List[str] = field(default_factory=list)
    log: Mapping[str, str] = field(default_factory=dict)


@dataclass
class Config:
    user: str
    token: str
    logfile: str
    skiptls: str
    output: str
    debug: str
    steps: List[StepData]


def make_config(config):
    config_steps = {}
    for step_name, step_data_list in config['steps'].items():
        step_info_list = []
        for step_data in step_data_list:
            step_info = StepData(
                step=step_name,
                url=step_data.get('url', ''),
                parameters=step_data.get('parameters', {}),
                action=step_data['action'],
                wait_end=step_data.get('wait_end', True),
                iterations=step_data.get('iterations', ''),
                catch=step_data.get('catch', []),
                log=step_data.get('log', {})
            )
            step_info_list.append(step_info)

        config_steps[step_name] = step_info_list

    if config_steps["mock_step"]:
        del config_steps["mock_step"]

    return Config(
        user=config['user'],
        token=config['token'],
        logfile=config.get('logfile', ''),
        skiptls=config.get('skiptls', ''),
        output=config.get('output', ''),
        debug=config.get('debug', ''),
        steps=config_steps
    )
