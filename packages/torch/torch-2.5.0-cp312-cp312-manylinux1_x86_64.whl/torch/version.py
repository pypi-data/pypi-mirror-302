from typing import Optional

__all__ = ['__version__', 'debug', 'cuda', 'git_version', 'hip']
__version__ = '2.5.0+cu124'
debug = False
cuda: Optional[str] = '12.4'
git_version = '32f585d9346e316e554c8d9bf7548af9f62141fc'
hip: Optional[str] = None
