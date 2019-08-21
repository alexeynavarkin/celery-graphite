import logging


logger = logging.getLogger('extract')


def extract(to_dict: dict, from_dict: dict):
    for key in to_dict.keys():
        extracted_val = from_dict.get(key)
        logger.debug(f'Getting {key}.')
        if extracted_val:
            logger.debug(f'Extracted from config {key} = {extracted_val}.')
            to_dict[key] = extracted_val
