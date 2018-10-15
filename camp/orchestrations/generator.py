#
# CAMP
#
# Copyright (C) 2017, 2018 SINTEF Digital
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the MIT license.  See the LICENSE file for details.
#



from ozepy import *
from z3 import *

import yaml
import pprint
import inspect
import linecache
import timeit
import itertools
import sys, getopt, os



NSPAR = 3

classes_yaml = """
-
  name: Image
  abstract: True
  reference: [
    {name: features, type: Feature, multiple: true},
    {name: dep, type: Feature, multiple: true}
  ]
-
  name: DownloadImage
  supertype: Image
-
  name: Feature
  reference: [
    {name: sup, type: Feature},
    {name: allsup, type: Feature, multiple: true},
    {name: root, type: Feature}
  ]
-
  name: Service
  reference: [
    {name: image, type: Image, mandatory: true},
    {name: dependson, type: Service, multiple: true},
    {name: imgfeature, type: Feature, multiple: true}
  ]
"""

backupmeta = """attribute: [
    {name: mandatory, type: Boolean}
]"""

def prepare_all_sup():
    features = [fea for fea in get_all_objects() if fea.type.name == 'Feature']
    for fea in features:
        sup = fea.forced_values.get('sup', None)
        if sup is None:
            fea.forced_values['allsup'] = []
        else:
            fea.forced_values['allsup'] = [sup]
    # print features
    for f1 in features:
        for f2 in features:
            for f3 in features:
                if (f2 in f1.forced_values['allsup']) and (f3 in f2.forced_values['allsup']):
                    f1.forced_values['allsup'].append(f3)
    #======== See later if we need a root reference or not=========#
    for fea in features:
        roots = [f for f in fea.forced_values['allsup'] if not ('sup' in f.forced_values) ]
        if roots:
            fea.forced_values['root'] = roots[0]
        else:
            fea.forced_values['root'] = fea


specification = None
images = dict()
services = dict()
features = dict()

def afeature(name, sup=None):
    fea = DefineObject(name, Feature)
    features[name] = fea
    if not sup is None:
        fea.force_value('sup', sup)
    return fea

classes = yaml.load(classes_yaml)

Image, DownloadImage, Feature, Service\
    = load_all_classes(classes)

generate_meta_constraints()

e1, e2 = ObjectVars(Image, 'e1', 'e2')
f1, f2, f3 = ObjectVars(Feature, 'f1', 'f2', 'f3')
s1, s2 = ObjectVars(Service, 's1', 's2')


def resolve_features(featurenames):
    return [features[n] for n in featurenames]

def declare_feature(spec, parent):
    if type(spec) is list:
        for str in spec:
            afeature(str, parent)
    if type(spec) is dict:
        for str, val in spec.iteritems():
            newparent = afeature(str, parent)
            declare_feature(val, newparent)

covered = []
composes = dict()
def print_result(model, index):
    result = cast_all_objects(model)
    current_features = []
    for x in result:
        if result[x]['type'] == 'Service' and result[x]['alive']:
            img = result[result[x]['image']]
            for fea in img['features']:
                feaobj = get_object_by_name(fea)
                current_features.append(str(feaobj))
                if feaobj not in covered:
                    covered.append(feaobj)

    resultsrvs = dict()
    composite = {'features': current_features, 'services': resultsrvs}
    for obj in result:
        if result[obj]['type'] == 'Service':
            srv = result[obj]
            srvname = srv['name'][4:]
            img = specification['images'][srv['image']]
            resultsrvs[srvname] = {
                'image': "%s:%s"%(img['name'], img['tag'])
            }
            dependson = [x[4:] for x in srv['dependson']]
            if dependson:
                resultsrvs[srvname]['depends_on'] = dependson
            print result[obj]
    composes['compose%d' % index] = composite



def generate(workingdir):
    global specification

    with open(workingdir+'/features.yml', 'r') as stream:
        feature_spec = yaml.load(stream)
    declare_feature(feature_spec, None)
    # print features
    prepare_all_sup()

    with open(workingdir + '/composite.yml', 'r') as stream:
        specification = yaml.load(stream)
    with open(workingdir + '/ampimages.yml', 'r') as stream:
        ampspec = yaml.load(stream)
        for k, v in ampspec['images'].iteritems():
            specification['images'][k] = v

    for name, value in specification['images'].iteritems():
        img = DefineObject(name, DownloadImage)
        images[name] = img
        img.force_value('features', resolve_features(value['features']))
        img.force_value('dep', resolve_features(value.get('dep',[])))

    for name, value in specification['services'].iteritems():
        srv = DefineObject('srv_' + name, Service, suspended=True) #not value.get('mandatory', False))
        services[name] = srv
        srv.force_value('imgfeature', resolve_features(value.get('imgfeature', [])))
        # srv.force_value('mandatory', value.get('mandatory', False))


    print "Start searching for compositions"
    # wanted = ObjectConst(Image, 'wanted')

    generate_config_constraints()

    def supersetf(set1, set2):
        return set2.forall(f1, set1.contains(f1))
    def subsetf(set1, set2):
        return set1.forall(f1, set2.contains(f1))
    def isunionf(res, set1, set2):
        return And(
            res.forall(f1, Or(set1.contains(f1), set2.contains(f1))),
            set1.forall(f1, res.contains(f1)),
            set2.forall(f1, res.contains(f1))
        )

    def eq_or_child(sub, sup):
        return Or(sub == sup, sub.allsup.contains(sup))

    meta_facts(
        Service.forall(s1, s1.image.dep.forall(
            f1, s1.dependson.exists(s2, s2.image.features.exists(f2, eq_or_child(f2, f1))))),
        Service.forall(s1, Or(Feature.exists(f1, s1.image.dep.contains(f1)), Service.forall(s2, Not(s1.dependson.contains(s2))))),
        Service.forall(s1, Not(s1.dependson.contains(s1))),
        Service.forall(s1, s1.imgfeature.forall(
            f1, s1.image.features.exists(f2, eq_or_child(f2, f1))
        ))
        # Service.forall(s1, Or(s1.mandatory, s1.alive() == Service.exists(s2, s2.dependson.contains(s1))))
    )

    solver = Optimize()
    solver.add(*get_all_meta_facts())
    solver.add(*get_all_config_facts())
    #solver.add(Service.forall(s1, s1.dependson.count() <= 1))

    for cst in specification['constraints']:
        solver.add(eval(cst))

    maxi = specification.get('maximal', 4)
    solver.push()
    for i in range(0, maxi):
        oldlen = len(covered)
        print 'In %.2f seconds.>>' % timeit.timeit(solver.check, number=1)
        print_result(solver.model(), i)
        print covered
        if oldlen == len(covered):
            print 'no new features can be introduced'
            break
        solver.pop()
        solver.push()
        solver.maximize(Feature.filter(
            f1, And(
                And([f1 != fea for fea in covered]),
                Service.exists(s1, s1.image.features.contains(f1))
            )).count()
        )

    finalresult = {
        'watching': specification['services'].keys(),
        'composes': composes
    }

    with open(workingdir+'/out/ampcompose.yml', 'w') as stream:
        yaml.dump(finalresult, stream)



class Solver:

    def generate(self. working_directory):
        generate(working_directory)
        



if __name__ == "__main__":
    main(sys.argv[1:])

