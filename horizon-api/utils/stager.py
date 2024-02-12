import random
import string

def generate_stager(length, software_name):
    """
    Generates a stager executable of the specified length for the specified software.
    """
    stager = f"{software_name}_stager_" + ''.join(random.choices(string.ascii_letters + string.digits, k=length)) + ".exe"
    return stager
