import logging
from pathlib import Path

for lib in ("asyncio", "parso.cache", "parso.cache.pickle"):
    logging.getLogger(lib).setLevel(logging.WARNING)


PACKAGE_ROOT = Path(__file__).parent
