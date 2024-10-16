# ----------------------------------------------------------------------
# | Buckets
# ----------------------------------------------------------------------
from more_itertools import bucket

# ----------------------------------------------------------------------
# | Dictionary Bucket
# ----------------------------------------------------------------------
def _int_dict_bucket(dictionary: dict[str, int]):
    """Create a bucket for integer dictionary."""
    return bucket(dictionary.items(), key=lambda item: item[1])

def _int_dict_bucket_list(bucket_obj, value: int):
    """Return the list of keys for a given value in the bucket."""
    return [key for key, _ in bucket_obj[value]]

def _str_dict_bucket(dictionary: dict[str, str]):
    """Create a bucket for string dictionary."""
    return bucket(dictionary.items(), key=lambda item: item[1])

def _str_dict_bucket_list(bucket_obj, value: str):
    """Return the list of keys for a given value in the bucket."""
    return [key for key, _ in bucket_obj[value]]

# ----------------------------------------------------------------------
# | Dictionary Bucket Class
# ----------------------------------------------------------------------
class DictionaryBucket:
    def __init__(self, dictionary: dict[str, str | int]):
        """Initialize the bucket based on the dictionary type."""
        self.bucket = None
        self.dictionary = dictionary

        if all(isinstance(value, str) for value in dictionary.values()):
            self.bucket = _str_dict_bucket(dictionary)
        elif all(isinstance(value, int) for value in dictionary.values()):
            self.bucket = _int_dict_bucket(dictionary)
        else:
            raise ValueError(
                "Dictionary must have uniform value types (either all int or all str)."
            )

    def get(self, value: str | int):
        """Return the list of keys that match the given value."""
        if isinstance(value, str):
            return _str_dict_bucket_list(self.bucket, value)
        if isinstance(value, int):
            return _int_dict_bucket_list(self.bucket, value)
        raise ValueError("Value must be of type str or int.")

DictBukt = DictionaryBucket

# ----------------------------------------------------------------------
# Example usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    dict_buckets1 = DictionaryBucket({"hello": 1, "goodbye": 0, "hi": 1, "hey": 1})
    dict_buckets2 = DictBukt({"red": 0, "yellow": 1, "orange": 0.5, "purple": 0.75})
    print(dict_buckets1.get(0))
    print(dict_buckets1.get(1))
    print(dict_buckets2.get(0))
    print(dict_buckets2.get(1))
