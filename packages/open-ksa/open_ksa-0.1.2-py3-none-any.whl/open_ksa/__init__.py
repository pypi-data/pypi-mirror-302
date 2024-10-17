# open_ksa/__init__.py
from setuptools_scm import get_version

__version__ = get_version()
from urllib.parse import urlparse, quote
from .download_file import download_file
from .get_dataset_resource import get_dataset_resource
from .get_dataset_resources import get_dataset_resources
from .get_org_resources import get_org_resources
from .ssl_adapter import SSLAdapter, SingletonSession
from .organizations import organizations