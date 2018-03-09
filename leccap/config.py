from builtins import object
import os
import json

"""
Simple JSON based config manager

@Version: 2.0
"""
class ConfigParser(object):

    def __init__(self):
        """
        Read config dict from file
        """
        self._json_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(self._json_path) as f:
            self._config = json.load(f)
    
    def get(self, key):
        """
        Get a value from the json config using dot accessor
        
        Arguments:
            key {str} -- Key
        
        Returns:
            mixed -- value for the key
        """
        return self._get(self._config, key.split('.'))
    
    def set(self, key, value):
        """
        Set a value to the config
        
        Arguments:
            key {str} -- Key
            value {str|number|list|dict} -- Value
        """
        self._set(self._config, key.split('.'), value)
    
    def save(self):
        """
        Dump back to the file
        """
        with open(self._json_path, 'w') as f:
            json.dump(self._config, f)

    """
    Helpers
    """
    def _get(self, config, keys):
        curr_key = keys[0]
        if len(keys) == 1:
            return config[curr_key]
        if not self._is_list(config[curr_key]) and not self._is_dict(config[curr_key]):
            raise ValueError("Cannot access object that is not list nor dict!")
        return self._get(config[curr_key], keys[1:])
    
    def _set(self, config, keys, value):
        curr_key = keys[0]
        if len(keys) == 1:
            config[curr_key] = value
        else:
            if curr_key not in config:
                raise ValueError("Key not exists!")
            self._set(config[curr_key], keys[1:], value)
    
    def _is_list(self, obj):
        return isinstance(obj, list)
    
    def _is_dict(self, obj):
        return isinstance(obj, dict)
