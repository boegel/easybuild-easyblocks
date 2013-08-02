##
# Copyright 2009-2013 Ghent University
#
# This file is part of EasyBuild,
# originally created by the HPC team of Ghent University (http://ugent.be/hpc/en),
# with support of Ghent University (http://ugent.be/hpc),
# the Flemish Supercomputer Centre (VSC) (https://vscentrum.be/nl/en),
# the Hercules foundation (http://www.herculesstichting.be/in_English)
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
EasyBuild support for building and installing fastahack, implemented as an easyblock

@author: Stijn De Weirdt (Ghent University)
@author: Dries Verdegem (Ghent University)
@author: Kenneth Hoste (Ghent University)
@author: Pieter De Baets (Ghent University)
@author: Jens Timmerman (Ghent University)
"""

import os
import shutil

from easybuild.easyblocks.generic.configuremake import ConfigureMake

class EB_fastahack(ConfigureMake):
    """Support for building/installing fastahack."""

    def configure_step(self):
        """No configure step for fastahack."""
        pass

    def install_step(self):
        """Install fastahack by copying binaries."""
        bindir = os.path.join(self.installdir, 'bin')
        os.makedirs(bindir)

        for exe in ['fastahack']:
            src = os.path.join(self.cfg['start_dir'], exe)
            dst = os.path.join(bindir, exe)
            try:
                shutil.copy2(src, dst)
                self.log.info("Successfully copied %s to %s" % (src, dst))
            except OSError, err:
                self.log.error("Failed to copy %s to %s: %s" % (src, dst, err))

    def sanity_check_step(self):
        """Custom sanity check for fastahack."""
        custom_paths = {
            'files': ["bin/%s" % self.name.lower()],
            'dirs': [],
        }
        super(EB_fastahack, self).sanity_check_step(custom_paths=custom_paths)
