# ----------------------------------------------------------------------
# | Build Version
# ----------------------------------------------------------------------
from dataclasses import dataclass
import random
from typing import Any, Generic, TypeVar


B = TypeVar('B')

class Build(Generic[B], type):
    _instances: dict[str, B] = {}

    def __init__(
        cls,
        name: str,
        bases: tuple[type, ...],
        attrs: dict[str, Any],
    ) -> None:
        super().__init__(name, bases, attrs)

    def __call__(
        cls,
        *args: Any,
        **kwargs: Any
    ) -> B:
        build = args[0] if args else kwargs.get('build')
        if build is None:
            raise ValueError("A 'build' value must be provided.")

        if build not in cls._instances:
            cls._instances[build] = super().__call__(*args, **kwargs)
        return cls._instances[build]

WORDS = [
    "apple", "archer", "balance", "baker", "battle", "beacon", "cabinet", "candy", "castle", 
    "clover", "dancer", "danger", "diamond", "dream", "eagle", "element", "elbow", "engine", 
    "flower", "flame", "forest", "freedom", "gallery", "gallon", "globe", "grape", "hammer", 
    "happy", "hunter", "horizon", "insect", "island", "ivory", "jacket", "joker", "journal", 
    "jungle", "kingdom", "kitten", "koala", "ladder", "lemon", "library", "lumber", "magic", 
    "medley", "melody", "monarch", "nation", "navel", "network", "notion", "octave", "ocean", 
    "optical", "orange", "painter", "piano", "planet", "plasma", "queen", "quality", "quartz", 
    "quiver", "reptile", "ribbon", "robot", "rocket", "sable", "shadow", "silver", "station", 
    "tiger", "tablet", "ticket", "texture", "umbrella", "unicorn", "united", "upgrade", "valley", 
    "venture", "victor", "vivid", "wander", "warrior", "whale", "window", "wolf", "yellow", 
    "youth", "zealous", "zebra", "zodiac"
]

@dataclass
class Version(metaclass=Build):
    build: str
    name: str = None

    def dict(self) -> str:
        """."""
        return self.__dict__

    def __str__(self) -> str:
        """."""
        return self.build

    def __repr__(self) -> str:
        """."""
        return self.name

    def __post_init__(self):
        if self.name is None:
            self.name = self._generate_name()

    @staticmethod
    def _generate_name() -> str:
        """Generates a name with three random words separated by hyphens."""
        return "-".join(random.sample(WORDS, 3))

def build_name(version: Version, print_name: bool = False, print_before: str = None) -> str:
    """Returns the build number of a Version object"""
    if not print_name:
        return repr(version)
    if print_before:
        print(f'{print_before}{repr(version)}')
    else:
        print(repr(version))
    return None

def ver(version: Version, print_build: bool = False, print_before: str = None) -> str:
    """Returns the build number of a Version object"""
    if not print_build:
        return str(version)
    if print_before:
        print(f'{print_before}{version}')
    else:
        print(version)
    return None

# ----------------------------------------------------------------------
# | Example Usage
# ----------------------------------------------------------------------
if __name__ == "__main__":
    _v_ = Version('3.9.0')
    print(repr(_v_), _v_)
