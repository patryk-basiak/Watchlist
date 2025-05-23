class EmptyEntry(Exception):
    '''Created for situation when Entry is empty'''
class MovieAlreadyExists(Exception):
    '''Created for situation when Movie with the same attributes already exists'''
class ReviewDoesntExist(Exception):
    '''When review with give attributes doesn't exist'''