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

from os import makedirs
from os.path import isdir, join


def do_generate(working_dir):
    start_over()
    NSPAR = 2

    classes_yaml = """
-
  name: Variable
-
  name: VarValue
  reference: [{name: variable, type: Variable, mandatory: true}]
-
  name: IntValue
  supertype: VarValue
  attribute: [{name: value, type: Integer}]
-
  name: Image
  abstract: True
  reference: [{name: features, type: Feature, multiple: true}]
- 
  name: BuildImage
  supertype: Image
  reference: [
    {name: from, type: Image, mandatory: true},
    {name: using, type: BuildRule, mandatory: true},
    {name: ival, type: VarValue, multiple: true}
  ]
-
  name: DownloadImage
  supertype: Image
-
  name: BuildRule
  reference: [
    {name: requires, type: Feature, multiple: true},
    {name: adds, type: Feature, multiple: true},
    {name: rvar, type: Variable, multiple: true}
  ]
-
  name: Feature
  reference: [
    {name: sup, type: Feature},
    {name: allsup, type: Feature, multiple: true},
    {name: root, type: Feature}
  ]
    """

    features = dict()
    dimages = dict()
    rules = dict()

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

        # for fea in features:
        #     print '%s: (%s)' % (fea.name, fea.forced_values['root'])

    def afeature(name, sup=None):
        fea = DefineObject(name, Feature)
        if not sup is None:
            fea.force_value('sup', sup)
        features[name] = fea
        return fea

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

    def require_feature(w, f):
        return w.features.exists(f1, Or(f1 == f, f1.allsup.contains(f)))

    def require_feature_all(wanted, featurelist):
        return And([require_feature(wanted,f) for f in featurelist])


    classes = yaml.load(classes_yaml)

    Variable, VarValue, IntValue, Image, BuildImage, DownloadImage, BuildRule, Feature \
        = load_all_classes(classes)

    generate_meta_constraints()

    e1, e2 = ObjectVars(Image, 'e1', 'e2')
    f1, f2, f3 = ObjectVars(Feature, 'f1', 'f2', 'f3')
    wanted = ObjectConst(Image, 'wanted')

    buildchains = []
    image_spec = None
    resultbuildimages = []

    def get_wanted(model):
        result = cast_all_objects(model)
        for i in get_all_objects():
            if i.type.package == wanted.type.package:
                if str(model.eval(wanted == i)) == 'True':
                    return result[str(i)]

    ampimages = dict()


    def print_model_deploy(model):
        global image_spec
        result = cast_all_objects(model)
        v = get_wanted(model)

        for each_feature in v["features"]:
            print "   - ", each_feature

        toprint = '\# %s: ' % v['features']

        for elem in result.itervalues():
            if elem['type'] == 'VarValue':
                elem['show'] = elem['name']
            if elem['type'] == 'IntValue':
                elem['show'] = '%s=%s' % (elem['name'], elem['value'])

        chain = []
        bc_item = {
            'chain': chain,
            'features': v['features']
        }
        buildchains.append(bc_item)
        newkey = ''
        newname = None
        newtag = None
        newfeatures = v['features']
        dep = []
        while True:
            if 'using' in v:
                if newname is None:
                    newname = v['using']
                else:
                    if newtag is None:
                        newtag = v['using']
                    else:
                        newtag = newtag + '-' + v['using']
                newkey = newkey + v['using']

                for x in image_spec['buildingrules'][v['using']].get('depends', []):
                    dep.append(x)
                toprint = toprint + "\n" + '%s(%s, %s) -> '%(v['name'], v['using'], [result[s]['show'] for s in v['ival']])
                chain.append({'rule': v['using']})
                v = result[v['from']]
            else:
                toprint = toprint + "\n" + v['name']
                dimage = image_spec['downloadimages'][v['name']]
                chain.append({'name': dimage['name'], 'tag': dimage['tag']})
                newtag = '%s-%s-%s' % (newtag, dimage['name'], dimage['tag'])
                newkey = newkey + v['name']
                break
        ampimages[newkey] = {
            'name': newname.lower(),
            'tag': newtag.lower(),
            'features': newfeatures,
            'dep': dep
        }
        #print toprint

    covered = []

    def find_covered_features(model):
        v = get_wanted(model)
        for f in v['features']:
            for i in get_all_objects():
                if i.name == f and not (i in covered):
                    covered.append(i)
        #print 'features covered: %s' % covered


    def declare_feature(spec, parent):
        if type(spec) is list:
            for str in spec:
                afeature(str, parent)
        if type(spec) is dict:
            for str, val in spec.iteritems():
                newparent = afeature(str, parent)
                declare_feature(val, newparent)

    def resolve_features(featurenames):
        return [features[n] for n in featurenames]

    def generate(workingdir):
        global image_spec

        with open(workingdir+'/features.yml', 'r') as stream:
            feature_spec = yaml.load(stream)
        declare_feature(feature_spec, None)
        # print features
        prepare_all_sup()

        print ""
        print "Searching for stacks ..."

        with open(workingdir + '/images.yml', 'r') as stream:
            image_spec = yaml.load(stream)
            assert image_spec, "Empty images specification!"
            
        for name, value in image_spec['downloadimages'].iteritems():
            img = DefineObject(name, DownloadImage)
            dimages[name] = img
            img.force_value('features', resolve_features(value['features']))

        for name, value in image_spec['buildingrules'].iteritems():
            img = DefineObject(name, BuildRule)
            rules[name] = img
            img.force_value('requires', resolve_features(value['requires']))
            img.force_value('adds', resolve_features(value['adds']))


        images = [DefineObject('image%d'%i, BuildImage, suspended=True) for i in range(0, NSPAR)]

        # wanted = ObjectConst(Image, 'wanted')

        heapsize = DefineObject('heapsize', Variable)
        # xmx512 = DefineObject('xmx512', VarValue).force_value('variable', heapsize)
        # xmx1024 = DefineObject('xmx1024', VarValue).force_value('variable', heapsize)
        xmxfree = DefineObject('xmxfree', IntValue).force_value('variable', heapsize)
        for r in rules.values():
            r.force_value('rvar', [heapsize])

        generate_config_constraints()

        bi1 = ObjectVar(BuildImage, 'bi1')
        bi2 = ObjectVar(BuildImage, 'bi2')
        v1 = ObjectVar(Variable, 'v1')
        vv1 = ObjectVar(VarValue, 'vv1')
        vv2 = ObjectVar(VarValue, 'vv2')
        meta_facts(
            BuildImage.forall(bi1, And(
                bi1.using.requires.forall(
                    f1, bi1['from'].features.exists(
                        f2, Or(f2==f1, f2.allsup.contains(f1))
                    )
                ),
                isunionf(bi1.features, bi1['from'].features, bi1.using.adds)
            )),
            BuildImage.forall(bi1, Not(bi1['from'] == bi1)),
            BuildImage.forall(bi1, bi1.features.exists(f1, Not(bi1['from'].features.contains(f1)))),
            BuildImage.forall(bi1, And(
                bi1.using.rvar.forall(v1, bi1.ival.exists(vv1, vv1.variable == v1)),
                bi1.ival.forall(vv1, bi1.using.rvar.contains(vv1.variable)),
                bi1.ival.forall(vv1, bi1.ival.forall(vv2, Or(vv1 == vv2, vv1.variable != vv2.variable)))
            )),

            # Image.forall(e1, (e1.features * e1.features).forall(
            #     [f1, f2], Or(f1==f2, Not(Feature.exists(f3, And(f1.allsup.contains(f3), f2.allsup.contains(f3)))))
            # )),
            Image.forall(e1, (e1.features * e1.features).forall(
                [f1, f2], Or(f1 == f2, Not(f1.root == f2.root))
            ))
        )

        solver = Optimize()
        solver.add(*get_all_meta_facts())
        solver.add(*get_all_config_facts())

        #----
        solver.add(xmxfree.value >=512)
        #----

        solver.add(wanted.isinstance(Image))
        solver.add(wanted.alive())

        solver.add(require_feature_all(wanted, [features[x] for x in image_spec['mandatoryfeature']]))


        for cst in image_spec.get('constraints', []):
            solver.add(eval(cst))

        maxi = image_spec.get('maximal', 4)
        solver.push()
        for i in range(0, maxi):
            oldlen = len(covered)
            print ' - Stack %d (in %.2f s.)' % (i+1, timeit.timeit(solver.check, number=1))

            find_covered_features(solver.model())
            if len(covered) == oldlen:
                break
            print_model_deploy(solver.model())
            solver.pop()
            solver.push()
            solver.maximize(wanted.features.filter(f1, And([Not(f1 == fea) for fea in covered])).count())

            print ''
        with open(workingdir + '/out/genimages.yml', 'w') as stream:
            yaml.dump({'buildchains': buildchains}, stream)
            stream.close()

        with open(workingdir + '/out/ampimages.yml', 'w') as stream:
            yaml.dump({'images': ampimages}, stream)
            stream.close()

    generate(working_dir)



class Finder:


    def __call__(self, arguments):
        self._verify_resources(arguments)
        do_generate(arguments.working_directory)

    def _verify_resources(self, arguments):
        out_directory = join(arguments.working_directory, "out")
        if not isdir(out_directory):
            makedirs(out_directory)
