# ----------------------------------------------------------------------
# | Typing Changes in Python 3.13
# ----------------------------------------------------------------------
from typing import Generic, TypeGuard, TypeVar, TypedDict, ReadOnly, reveal_type
from warnings import deprecated


# ----------------------------------------------------------------------
# | Deprecated decorator
# ----------------------------------------------------------------------
@deprecated('Use reimplemented_function instead')
def deprecated_function() -> None: ...

def reimplemented_function() -> None:
    deprecated_function()

# ----------------------------------------------------------------------
# | Default Context TypeVar for App
# ----------------------------------------------------------------------
class Context: ...
class CustomContext: ...

T = TypeVar('T', default=Context)

class App(Generic[T]):
    context: T

# ----------------------------------------------------------------------
# | User TypedDict *ReadOnly id*
# ----------------------------------------------------------------------
class User(TypedDict):
    id: ReadOnly[int]
    name: str
    email_address: str

# ----------------------------------------------------------------------
# | TypeGuard for object instances
# ----------------------------------------------------------------------
class Configuration:
    def initialize(self) -> None:
        print("Initializing!")

class Application:
    def start(self) -> None:
        print("Starting Application!")

def _is_config(obj: object) -> TypeGuard[Configuration]:
    return isinstance(obj, Configuration)

def _init(mode: Configuration | Application) -> None:
    if _is_config(mode): # significant, limits to only Configuration
        return mode.initialize()
    else:
        return mode.start()

# ----------------------------------------------------------------------
# | Example usage 
# ----------------------------------------------------------------------
if __name__ == "__main__":
    # Use the `reimplemented_function` to test deprecation warnings 
    # reimplemented_function()
    app = App()
    user: User = {
        "id": 1,
        "name": "Alex",
        "email_address": "alex@aode.space",
    }
    _init(Configuration())
