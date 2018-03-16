"""
    Hui Song: hui.song@sintef.no
"""

import yaml
import sys, getopt, os
import copy
import re
from jsonpath_rw import jsonpath, parse


HELPTEXT = 'composegen.py -i <inputfile> -d <working dir> (optional)'

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



def mock_amplifier(seed):

    ampresult_atos=[
        Compose([
            Service('mysql', 'supersede/mysql'),
            Service('be', 'supersede/be', ['mysql'])
        ]),
        Compose([
            Service('mysql', 'supersede/mysql:old'),
            Service('be', 'supersede/be', ['mysql'])
        ]),
        Compose([
            Service('mysql', 'supersede/mysql'),
            Service('postgres', 'supersede/postgres'),
            Service('be', 'supersede/be:postgres', ['postgres'])
        ])
    ]

    ampresult_xwiki = [
        Compose([
            Service('postgres', 'postgres:10'),
            Service('web', 'xwiki:postgres-tomcat', ['postgres'])
        ])
    ]
    return ampresult_xwiki


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
        stream = open('%s/compose%d/docker-compose.yml'%(workingdir, i), 'w')
        stream.write(str)
        stream.close()
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





def main(argv):
    inputfile = ''
    workingdir = ''
    try:
        opts, args = getopt.getopt(argv,"hi:d:",["ifile=","dir="])
    except getopt.GetoptError:
        print HELPTEXT
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print HELPTEXT
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-d", "--dir"):
            workingdir = arg

    if workingdir == '':
        workingdir = os.path.dirname(inputfile)

    print 'Input file is ', inputfile
    print 'Working directory is ', workingdir

    if inputfile == '':
        print 'input file and working directory required: ' + HELPTEXT
        exit()

    seedfile = workingdir + "/docker-compose/docker-compose.yml"
    generate(seedfile, workingdir, inputfile)



if __name__ == "__main__":
    main(sys.argv[1:])