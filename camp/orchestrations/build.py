#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



import yaml
import sys, getopt, os
import copy
import re
from jsonpath_rw import jsonpath, parse

from os.path import join



class Service:
    def __init__(self, name=None, image=None, depends_on=[], attribute=dict()):
        self.name = name
        self.image = image
        self.depends_on = depends_on
        self.attribute = attribute


class Compose:

    def __init__(self, services=[]):
        self.services = services

    def get(self, name):
        try:
            res, =(service for service in self.services if service.name == name)
            return res
        except ValueError:
            return None

    def __contains__(self, name):
        return any(service.name == name for service in self.services)


def load_ampresult(ampresult):
    composes = []
    for comp in ampresult['composes'].values():
        services = []
        for srvname, srv in comp['services'].iteritems():
            services.append(Service(srvname, srv['image'], srv.get('depends_on', []), srv.get('attribute', dict())))
        composes.append(Compose(services))

    return composes


def extract(reference, watching):
    compose = Compose();
    services = reference['services']
    for s in services:
        if s in watching:
            sd = services[s]
            depends = [d for d in sd.get('depends_on', []) if d in watching]
            compose.services.append(Service(s, sd['image'], depends))
    return compose


def threewaycomp(reference, original, changed):
    result = copy.deepcopy(reference)
    refservices = result['services']
    toremove = []
    for srvname in refservices:
        osrv = original.get(srvname)
        csrv = changed.get(srvname)
        if osrv is None:
            continue
        if csrv is None:
            toremove.append(srvname)
            continue
        if osrv.image != csrv.image:
            refservices[srvname]['image'] = csrv.image
        refdeps = refservices[srvname].get('depends_on', [])
        toremovedep = [x for x in refdeps if (x in osrv.depends_on) and (x not in csrv.depends_on)]
        for trd in toremovedep:
            refdeps.remove(trd)
        refdeps.extend(x for x in csrv.depends_on if (x not in osrv.depends_on))
        if refdeps:
            refservices[srvname]['depends_on'] = refdeps
    for tr in toremove:
        refservices.pop(tr)

    for csrv in changed.services:
        if csrv.name not in original:
            refservices[csrv.name] = {'image': csrv.image, 'depends_on': csrv.depends_on}

    return result


def generate(seedfile, workingdir, amp_result_file):
    name = os.path.basename(seedfile)
    with open(seedfile, 'r') as stream:
        reference = yaml.load(stream)
    with open(amp_result_file, 'r') as stream:
        amp_result = yaml.load(stream)

    seed = extract(reference, amp_result['watching'])

    amplified = load_ampresult(amp_result);

    outputs = [threewaycomp(reference, seed, amp) for amp in amplified]

    for output, i in zip(outputs, range(1, 1000)):
        str = yaml.dump(output, default_flow_style=False)
        root = output
        while True:
            searcher = re.search(r'\&\((.*)\)\&', str, re.M | re.I)
            if not searcher:
                break;
            placeholder = searcher.group()
            immvalues = []
            for path in searcher.group(1).split('|'):
                for j in range(0,len(immvalues)):
                    path = path.replace('@%d' % j, immvalues[j])
                result = parse(path).find(root)[0].value
                print result
                immvalues.append(result)
            value = immvalues[-1]
            print value
            str = str.replace(placeholder, value)
        if not os.path.exists("%s/compose%d"%(workingdir, i)):
            os.makedirs("%s/compose%d"%(workingdir, i))
        stream = open('%s/compose%d/docker-compose.yml'%(workingdir, i), 'w')
        stream.write(str)
        stream.close()

    if not os.path.isfile("%s/variables.yml" % workingdir):
        print "No variables.yml, sipping variable resolution!"
        return

    resol = dict()
    products = []
    resol['products'] = products
    with open("%s/variables.yml" % workingdir, 'r') as stream:
        variables = yaml.load(stream)
    def resolve_var(value):
        return next(v for v in variables if value in variables[v])
    for amp, i in zip(amplified, range(1, 1000)):
        product = dict()
        products.append({'compose%d' % i: product})
        product['product_dir'] = "%s/compose%d" % (workingdir, i)
        varvalues = []
        valvalues = []
        product['realization'] = {
            'path': "%s/variables.yml" % workingdir,
            'variables': varvalues,
            'values': valvalues
        }
        for srv in amp.services:
            for k, v in srv.attribute.iteritems():
                varvalues.append({resolve_var(k):k})
                valvalues.append({k: v})
    with open("%s/resolmodel.yml"%workingdir, 'w') as stream:
        yaml.dump(resol, stream)
        stream.close()



class Builder(object):

    def build(self, working_directory):
        seed = join(working_directory, "docker-compose", "docker-compose.yml")
        input_file = join(working_directory, "out", "ampcompose.yml")
        generate(seed, working_directory, input_file)
