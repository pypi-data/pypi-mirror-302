import os
import importlib


import cronevents.event_manager


def register_events(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File not found: {file_path}')

    os.environ['REGISTER_CRON_EVENT'] = 'true'
    importlib.reload(cronevents.event_manager)

    module_name = os.path.splitext(os.path.basename(file_path))[0]
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    del module

    os.environ['REGISTER_CRON_EVENT'] = 'false'
    importlib.reload(cronevents.event_manager)

