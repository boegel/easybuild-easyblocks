##
# Copyright 2019-2020 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://www.vscentrum.be),
# Flemish Research Foundation (FWO) (http://www.fwo.be/en)
# and the Department of Economy, Science and Innovation (EWI) (http://www.ewi-vlaanderen.be/en).
#
# https://github.com/easybuilders/easybuild
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
EasyBuild support for building and installing GAUSS, implemented as an easyblock
"""
import os

import easybuild.tools.environment as env
from easybuild.framework.easyblock import EasyBlock
from easybuild.tools.run import run_cmd_qa


class EB_GAUSS(EasyBlock):
    """Support for building/installing GAUSS."""

    def __init__(self, *args, **kwargs):
        """Constructor for GAUSS easyblock."""
        super(EB_GAUSS, self).__init__(*args, **kwargs)

        self.build_in_installdir = True

        self.subdir = 'gauss' + self.version

    def configure_step(self):
        """No custom configuration procedure for GAUSS."""
        pass

    def build_step(self):
        """No custom build procedure for GAUSS."""
        pass

    def install_step(self):
        """Custom install procedure for GAUSS."""

        # ginstall script uses 'more LICENSE' to display the license text to be read/approved
        # this causes trouble with run_cmd_qa
        # nasty hack: pass -V option to 'more' command via $MORE to make it print its version and exit
        env.setvar('MORE', '-V')

        qa = {
            # default implies single-user installation
            "Choose installation type: [D]efault, [M]ulti-User [Q]uit:": 'D',
            "Press Enter to continue... ": '',
            "Do you understand and accept the license agreement? [ yes/no ]": 'yes',
        }
        run_cmd_qa('./ginstall', qa, log_all=True, simple=True, log_ok=True, maxhits=5)

    def sanity_check_step(self):
        """Custom sanity check for GAUSS."""

        custom_paths = {
            'files': [os.path.join(self.subdir, 'gauss'), os.path.join(self.subdir, 'tgauss')],
            'dirs': [os.path.join(self.subdir, 'bin')],
        }
        super(EB_GAUSS, self).sanity_check_step(custom_paths=custom_paths)

    def make_module_req_guess(self):
        """Custom guesses for paths in generated module file for GAUSS."""
        return {
            'PATH': self.subdir,
            # yes, .so files for libraries are located in 'bin', not 'lib'... 0_o
            'LD_LIBRARY_PATH': os.path.join(self.subdir, 'bin'),
        }
