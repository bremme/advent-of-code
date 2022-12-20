import logging

for lib in ("asyncio", "parso.cache", "parso.cache.pickle"):
    logging.getLogger(lib).setLevel(logging.WARNING)
