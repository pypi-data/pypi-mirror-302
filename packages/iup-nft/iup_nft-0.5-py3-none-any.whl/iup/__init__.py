import importlib_metadata

metadata = importlib_metadata.metadata("iup-nft")

__version__ = metadata['version']
