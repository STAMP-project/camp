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

from pkgutil import get_data

import yaml
import pprint
import inspect
import linecache
import timeit
import itertools
import sys, getopt, os



NSPAR = 3


backupmeta = """attribute: [
    {name: mandatory, type: Boolean}
]"""


class Finder(object):


    def __init__(self):
        self._specification = None
        self._images = dict()
        self._services = dict()
        self._features = dict()
        self._covered = []
        self._composes = dict()


    def find(self, workingdir):
        start_over()

        data = get_data('camp', 'data/images.yml')
        classes = yaml.load(data)
        Image, DownloadImage, Feature, Service = load_all_classes(classes)
        self._Feature = Feature

        generate_meta_constraints()

        with open(workingdir+'/features.yml', 'r') as stream:
            feature_spec = yaml.load(stream)
        self._declare_feature(feature_spec, None)

        self._prepare_all_sup()

        with open(workingdir + '/composite.yml', 'r') as stream:
            self._specification = yaml.load(stream)

        with open(workingdir + '/out/ampimages.yml', 'r') as stream:
            ampspec = yaml.load(stream)
            for k, v in ampspec['images'].iteritems():
                self._specification['images'][k] = v

        for name, value in self._specification['images'].iteritems():
            img = DefineObject(name, DownloadImage)
            self._images[name] = img
            img.force_value('features',
                            self._resolve_features(value['features']))
            img.force_value('dep', self._resolve_features(value.get('dep',[])))

        for name, value in self._specification['services'].iteritems():
            srv = DefineObject('srv_' + name, Service, suspended=True)
            self._services[name] = srv
            srv.force_value('imgfeature',
                            self._resolve_features(value.get('imgfeature', [])))

        print "Start searching for compositions"

        generate_config_constraints()

        e1, e2 = ObjectVars(Image, 'e1', 'e2')
        f1, f2, f3 = ObjectVars(Feature, 'f1', 'f2', 'f3')
        s1, s2 = ObjectVars(Service, 's1', 's2')

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
        )

        solver = Optimize()
        solver.add(*get_all_meta_facts())
        solver.add(*get_all_config_facts())

        for cst in self._specification['constraints']:
            solver.add(eval(cst, globals(), {"services": self._services} ))

        maxi = self._specification.get('maximal', 4)
        solver.push()
        for i in range(0, maxi):
            oldlen = len(self._covered)
            print 'In %.2f seconds.>>' % timeit.timeit(solver.check, number=1)
            self._print_result(solver.model(), i)
            print self._covered
            if oldlen == len(self._covered):
                print 'no new features can be introduced'
                break
            solver.pop()
            solver.push()
            solver.maximize(Feature.filter(
                f1, And(
                    And([f1 != fea for fea in self._covered]),
                    Service.exists(s1, s1.image.features.contains(f1))
                )).count()
            )

        finalresult = {
            'watching': self._specification['services'].keys(),
            'composes': self._composes
        }

        with open(workingdir+'/out/ampcompose.yml', 'w') as stream:
            yaml.dump(finalresult, stream)



    def _prepare_all_sup(self):
        features = [fea for fea in get_all_objects() if fea.type.name == 'Feature']
        for fea in features:
            sup = fea.forced_values.get('sup', None)
            if sup is None:
                fea.forced_values['allsup'] = []
            else:
                fea.forced_values['allsup'] = [sup]

        for f1 in features:
            for f2 in features:
                for f3 in features:
                    if (f2 in f1.forced_values['allsup']) and (f3 in f2.forced_values['allsup']):
                        f1.forced_values['allsup'].append(f3)

        for fea in features:
            roots = [f for f in fea.forced_values['allsup'] if not ('sup' in f.forced_values) ]
            if roots:
                fea.forced_values['root'] = roots[0]
            else:
                fea.forced_values['root'] = fea


    def _afeature(self, name, sup=None):
        fea = DefineObject(name, self._Feature)
        self._features[name] = fea
        if not sup is None:
            fea.force_value('sup', sup)
        return fea


    def _resolve_features(self, featurenames):
        return [self._features[n] for n in featurenames]


    def _declare_feature(self, spec, parent):
        if type(spec) is list:
            for str in spec:
                self._afeature(str, parent)
        if type(spec) is dict:
            for str, val in spec.iteritems():
                newparent = self._afeature(str, parent)
                self._declare_feature(val, newparent)


    def _print_result(self, model, index):
        result = cast_all_objects(model)
        current_features = []
        for x in result:
            if result[x]['type'] == 'Service' and result[x]['alive']:
                img = result[result[x]['image']]
                for fea in img['features']:
                    feaobj = get_object_by_name(fea)
                    current_features.append(str(feaobj))
                    if feaobj not in self._covered:
                        self._covered.append(feaobj)

        resultsrvs = dict()
        composite = {'features': current_features, 'services': resultsrvs}
        for obj in result:
            if result[obj]['type'] == 'Service':
                srv = result[obj]
                srvname = srv['name'][4:]
                img = self._specification['images'][srv['image']]
                resultsrvs[srvname] = {
                    'image': "%s:%s"%(img['name'], img['tag'])
                }
                dependson = [x[4:] for x in srv['dependson']]
                if dependson:
                    resultsrvs[srvname]['depends_on'] = dependson
                print result[obj]
        self._composes['compose%d' % index] = composite
