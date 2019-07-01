#
# CAMP
#
# Copyright (C) 2017 -- 2019 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#


class About:

    PROGRAM = "CAMP"

    VERSION = "0.5.1"

    COMMIT_HASH = None

    LICENSE = "MIT"

    COPYRIGHT = "Copyright (C) 2017 -- 2019 SINTEF Digital"

    DESCRIPTION = "Amplify your configuration tests!"


    @staticmethod
    def full_version():
        if About.COMMIT_HASH:
            return "%s-git.%s" % (About.VERSION, About.COMMIT_HASH[:7])
        return About.VERSION
