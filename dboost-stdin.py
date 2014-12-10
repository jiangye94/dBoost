#! /usr/bin/env python3
import dboost
import sys
import utils
import features
import argparse
import cli
import itertools 
from utils.autoconv import autoconv
from utils.print import print_rows

dataset = []
testset = []
row_length = None

parser = cli.get_sdtin_parser()
args, models, preprocessors, rules = cli.parsewith(parser)

if args.train_input is not None and args.test_input is not None:
  for line in args.train_input:
      line = line.strip().split(args.fs)
    
      if row_length != None and len(line) != row_length:
          sys.stderr.write("Discarding {}\n".format(line))

      row_length = len(line)
      dataset.append(tuple(autoconv(field) for field in line))

  for line in args.test_input:
      line = line.strip().split(args.fs)
    
      if row_length != None and len(line) != row_length:
          sys.stderr.write("Discarding {}\n".format(line))

      row_length = len(line)
      testset.append(tuple(autoconv(field) for field in line))

else:
    for line in args.input:
      line = line.strip().split(args.fs)
    
      if row_length != None and len(line) != row_length:
          sys.stderr.write("Discarding {}\n".format(line))

      row_length = len(line)
      dataset.append(tuple(autoconv(field) for field in line))

for preprocessor, model in itertools.product(preprocessors, models):
    outliers = dboost.outliers_static(dataset, preprocessor, model, rules, testset)

    if len(outliers) == 0:
        print("   All clean!")
    else:
        print_rows(outliers, model, preprocessor.hints,
                   features.descriptions(rules), args.verbosity)
