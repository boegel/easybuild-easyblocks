##
# Copyright 2009-2016 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# http://github.com/hpcugent/easybuild
#
# EasyBuild is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation v2.
#
# EasyBuild is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with EasyBuild.  If not, see <http://www.gnu.org/licenses/>.
##
"""
EasyBuild support for building and installing CLCGenomicsWorkbench, implemented as an easyblock

@author: Kenneth Hoste (HPC-UGent)
"""
from easybuild.easyblocks.generic.binary import Binary
from easybuild.tools.run import run_cmd_qa


class EB_CLCGenomicsWorkbench(Binary):
    """Support for building/installing CLCGenomicsWorkbench."""

    def install_step(self):
        """Custom install procedure for CLCGenomicsWorkbench."""

        qa = {
            r"OK [o, Enter], Cancel [c]": '',
        }

        std_qa = {
            r"\[Enter\]": '',
            r"I accept the agreement\nYes \[1\], No \[2\]": '1',
            r"Where should CLC Genomics Workbench be installed\?\n.*": self.installdir,
            r"already exists\. Would you like to install to that directory anyway\?\nYes \[y, Enter\], No \[n\]": 'y',
            r"Create symlinks\?\nYes \[y, Enter\], No \[n\]": 'n',
            r"Create a desktop icon\?\nYes \[y, Enter\], No \[n\]": 'n',
            r"Create a Quick Launch icon\?\nYes \[y, Enter\], No \[n\]": 'n',
            r"Use this Workbench to open clc:// URLs\?\nYes \[y, Enter\], No \[n\]": 'n',
            r"Run CLC Genomics Workbench\?\nYes \[y, Enter\], No \[n\]": 'n',
        }

        run_cmd_qa('./%s' % self.src[0]['name'], qa, std_qa=std_qa, log_all=True, simple=True)

    def sanity_check_step(self):
        """Custom sanity check for CLCGenomicsWorkbench."""
        custom_paths = {
            'files': ['clcgenomicswb%s' % self.version.split('.')[0], 'CLCWorkbench.jar'],
            'dirs': ['api', 'data', 'exec', 'lib'],
        }
        super(EB_CLCGenomicsWorkbench, self).sanity_check_step(custom_paths=custom_paths)
