import os
import yaml
from bundle.logger import logger

YAML_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)))


def get_sources_from_yaml():
    with open(YAML_PATH + '/log_sources.yaml') as f:
        try:
            data = yaml.safe_load(f)
            return data
        except yaml.YAMLError as err:
            logger.exception(err, "Cannot read YAML configuration")
