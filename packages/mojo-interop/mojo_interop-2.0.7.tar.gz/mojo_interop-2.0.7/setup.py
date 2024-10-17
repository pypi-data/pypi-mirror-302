# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'source/packages'}

packages = \
['mojo',
 'mojo.factories',
 'mojo.interop.clients',
 'mojo.interop.clients.linux',
 'mojo.interop.clients.linux.ext',
 'mojo.interop.clients.osx',
 'mojo.interop.clients.windows',
 'mojo.interop.clusters',
 'mojo.interop.clusters.raspberrypi',
 'mojo.interop.protocols',
 'mojo.interop.protocols.dns',
 'mojo.interop.protocols.power.dlipower',
 'mojo.interop.protocols.rest',
 'mojo.interop.protocols.serial',
 'mojo.interop.protocols.ssh',
 'mojo.interop.protocols.tasker',
 'mojo.interop.protocols.tasker.examples',
 'mojo.interop.protocols.upnp',
 'mojo.interop.protocols.upnp.content',
 'mojo.interop.protocols.upnp.devices',
 'mojo.interop.protocols.upnp.extensions',
 'mojo.interop.protocols.upnp.extensions.dynamic',
 'mojo.interop.protocols.upnp.extensions.dynamic.embeddeddevices',
 'mojo.interop.protocols.upnp.extensions.dynamic.rootdevices',
 'mojo.interop.protocols.upnp.extensions.dynamic.services',
 'mojo.interop.protocols.upnp.extensions.standard.embeddeddevices',
 'mojo.interop.protocols.upnp.extensions.standard.rootdevices',
 'mojo.interop.protocols.upnp.extensions.standard.services',
 'mojo.interop.protocols.upnp.extensions.standard.services.UPnP',
 'mojo.interop.protocols.upnp.generator',
 'mojo.interop.protocols.upnp.generator.dynamic',
 'mojo.interop.protocols.upnp.services',
 'mojo.interop.protocols.upnp.xml',
 'mojo.interop.services',
 'mojo.interop.services.vmware',
 'mojo.interop.services.vmware.datastructures',
 'mojo.interop.services.vmware.datastructures.model',
 'mojo.interop.services.vmware.datastructures.specs',
 'mojo.interop.services.vmware.metasphere',
 'mojo.interop.services.vmware.vsphere',
 'mojo.interop.services.vmware.vsphere.ext',
 'mojo.interop.testing']

package_data = \
{'': ['*'], 'mojo.interop.protocols.tasker': ['linux/*']}

install_requires = \
['mojo-config>=2.0.0,<2.1.0',
 'mojo-credentials>=2.0.0,<2.1.0',
 'mojo-errors>=2.0.0,<2.1.0',
 'mojo-landscaping>=2.0.0,<2.1.0',
 'mojo-networking>=2.0.0,<2.1.0',
 'mojo-results>=2.0.0,<2.1.0',
 'mojo-runtime>=2.0.0,<2.1.0',
 'mojo-testplus>=2.0.1,<2.1.0',
 'mojo-xmodules>=2.0.0,<2.1.0',
 'pexpect>=4.8.0,<5.0.0',
 'psutil>=5.9.6,<6.0.0',
 'rpyc>=6.0.0,<7.0.0']

setup_kwargs = {
    'name': 'mojo-interop',
    'version': '2.0.7',
    'description': 'Automation Mojo Interop Extensions',
    'long_description': "===============================\nAutomation Mojo Interop Package\n===============================\n\nThis *Automation Mojo Interop Package* contains interop extensions that add interop functionality to\nthe test environment *Landscape* object for a variety of platform clients, clusters, and protocols.\n\n=================\nCode Organization\n=================\n* .vscode - Common tasks\n* development - This is where the runtime environment scripts are located\n* repository-setup - Scripts for homing your repository and to your checkout and machine setup\n* userguide - Where you put your user guide\n* source/packages - Put your root folder here 'source/packages/(root-module-folder)'\n* workspaces - This is where you add VSCode workspaces templates and where workspaces show up when homed.\n  \n==========\nReferences\n==========\n\n- `User Guide <userguide/userguide.rst>`\n- `Coding Standards <userguide/10-00-coding-standards.rst>`\n",
    'author': 'Myron Walker',
    'author_email': 'myron.walker@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://automationmojo.com',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
