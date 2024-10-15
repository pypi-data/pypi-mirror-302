# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

from . import _utilities
import typing
# Export this package's modules as members:
from .cluster import *
from .get_cluster import *
from .get_organization import *
from .get_organizations import *
from .get_project import *
from .organization import *
from .project import *
from .provider import *
from ._inputs import *
from . import outputs

# Make subpackages available:
if typing.TYPE_CHECKING:
    import komminarlabs_cratedb.config as __config
    config = __config
else:
    config = _utilities.lazy_import('komminarlabs_cratedb.config')

_utilities.register(
    resource_modules="""
[
 {
  "pkg": "cratedb",
  "mod": "index/cluster",
  "fqn": "komminarlabs_cratedb",
  "classes": {
   "cratedb:index/cluster:Cluster": "Cluster"
  }
 },
 {
  "pkg": "cratedb",
  "mod": "index/organization",
  "fqn": "komminarlabs_cratedb",
  "classes": {
   "cratedb:index/organization:Organization": "Organization"
  }
 },
 {
  "pkg": "cratedb",
  "mod": "index/project",
  "fqn": "komminarlabs_cratedb",
  "classes": {
   "cratedb:index/project:Project": "Project"
  }
 }
]
""",
    resource_packages="""
[
 {
  "pkg": "cratedb",
  "token": "pulumi:providers:cratedb",
  "fqn": "komminarlabs_cratedb",
  "class": "Provider"
 }
]
"""
)
