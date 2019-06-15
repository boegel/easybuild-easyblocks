##
# This file is an EasyBuild reciPY as per https://github.com/easybuilders/easybuild
#
# Copyright:: Copyright 2012-2019 Uni.Lu/LCSB, NTUA
# Authors::   Fotis Georgatos <fotis@cern.ch>, Kenneth Hoste
# License::   MIT/GPL
# $Id$
#
# This work implements a part of the HPCBIOS project and is a component of the policy:
# http://hpcbios.readthedocs.org/en/latest/
##
"""
EasyBuild support for Chapel, implemented as an easyblock

@author: Fotis Georgatos (Uni.Lu)
@author: Kenneth Hoste (Ghent University)
"""
import os

from easybuild.easyblocks.generic.configuremake import ConfigureMake
from easybuild.tools.modules import get_software_root
from easybuild.tools.run import run_cmd
from easybuild.tools.systemtools import get_cpu_architecture


class EB_Chapel(ConfigureMake):
    """Support for building Chapel."""

    def __init__(self, *args, **kwargs):
        """Initialize Chapel-specific variables."""
        super(EB_Chapel, self).__init__(*args, **kwargs)
        self.build_in_installdir = True
        self.setup_script = os.path.join('util', 'setchplenv.bash')

    def extract_step(self):
        """Extract Chapel source tarball, strip off top-level component."""
        self.cfg['unpack_options'] = '--strip-components 1'

        super(EB_Chapel, self).extract_step()

    def configure_step(self):
        """No configure step for Chapel."""
        self.cfg['prebuildopts'] = "source %s && " % os.path.join(self.installdir, self.setup_script)

        # Chapel requires clang/AST/GlobalDecl.h (so it needs Clang rather than only LLVM)
        if get_software_root('Clang'):
            self.cfg.update('prebuildopts', "export CHPL_LLVM=system && ")

        if get_software_root('GMP'):
            self.cfg.update('prebuildopts', "export CHPL_GMP=system && ")

    def test_step(self):
        """Run Chapel tests."""
        self.cfg.update('pretestopts', self.cfg['prebuildopts'])
        run_cmd("%s CHPL_CHECK_DEBUG=1 make check %s" % (self.cfg['pretestopts'], self.cfg['testopts']))

    def install_step(self):
        """Installation of Chapel has already been done as part of the build procedure"""
        pass

    def sanity_check_step(self):
        """Custom sanity check for Chapel."""

        custom_paths = {
            'files': ['bin/linux64-%s/chpl' % get_cpu_architecture(), self.setup_script],
            'dirs': [],
        }

        hello = os.path.join(self.builddir, 'hello')
        custom_commands = [' && '.join([
            "chpl -o %s %s" % (hello, os.path.join('$EBROOTCHAPEL', 'examples', 'hello.chpl')),
            hello,
        ])]

        super(EB_Chapel, self).sanity_check_step(custom_paths=custom_paths, custom_commands=custom_commands)

    def make_module_req_guess(self):
        """
        A dictionary of possible directories to look for; this is needed since bin/linux64 of chapel is non standard
        """
        return {
            'MANPATH': ['man'],
            'PATH': ['bin/linux64-%s' % get_cpu_architecture()],
        }

    def make_module_extra(self):
        """
        Extra Chapel-specific environment variables to set.
        """
        txt = super(EB_Chapel, self).make_module_extra()

        txt += self.module_generator.set_environment('CHPL_HOME', self.installdir)

        return txt
