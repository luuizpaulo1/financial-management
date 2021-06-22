def missing_required_parameters(required_parameters: dict, parsed_args: dict):
    """
    Returns a list of all the required parameters missing from the body of the request.
    :return: list
    """
    missing_parameters = list()
    for key in required_parameters:
        if not parsed_args.get(key):
            missing_parameters.append(key)
    return missing_parameters
