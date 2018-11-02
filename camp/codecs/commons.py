#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#




class Codec(object):


    def load_model_from(self, stream):
        raise NotImplementedError()


    def save_model(self, model, stream):
        raise NotImplementedError()


    def load_configuration_from(self, model, stream):
        raise NotImplementedError()


    def save_configuration(self, configuration, stream):
        raise NotImplementedError()
