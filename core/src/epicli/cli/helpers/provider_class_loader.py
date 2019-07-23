import importlib


def provider_class_loader(provider, class_name):
    try:
        return getattr(importlib.import_module('cli.engine.' + provider.lower() + '.' + class_name), class_name)
    except:
        raise Exception('No ' + class_name + ' for ' + provider)
