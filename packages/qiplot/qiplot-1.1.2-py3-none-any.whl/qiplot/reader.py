import sys, os, re, string
import numpy as np
from glob import glob
import traceback

def fromstring(s):
    ## check for letters other than e/E
    abpattern = '[a-df-zA-DF-Z:;=]+'
    if len(re.findall(abpattern, s)) > 0:
        return s, 0
    ## check for numbers including scientific notation
    numpattern = '[+\-]?[^A-Za-z]?(?:[0-9]\d*)?(?:\.\d*)?(?:[eE][+\-]?\d+)?'
    pts = re.findall(numpattern, s)
    out = []
    ## return the floats and skip empty lines
    for i in pts:
        try:
            out.append(float(i))
        except ValueError:
            pass
    if len(out) > 0:
        return out, 1
    else:
        return s, 0


def linecheck(fname, maxbytes=-1):
    datalines = []
    headerlines = []
    with open(fname, 'r') as f:
        lines = [l.strip() for l in f.readlines(maxbytes)]
    for n, line in enumerate(lines):
        cols, numeric = fromstring(line)
#        lgr.debug('(%-3d %-5s) %s', n, bool(numeric), cols)
        if numeric == 1:
            datalines.append(cols)
        else:
            headerlines.append(f'{n}: {line}')
#    lgr.debug('end of loop')
    ### find ncols
    n2 = [len(i) for i in datalines].count(2)
    n3 = [len(i) for i in datalines].count(3)
    if n2 > n3:
        datalines = [i for i in datalines if len(i)==2]
    elif n3 > n2:
        datalines = [i for i in datalines if len(i)==3]
    else:
#        lgr.warning('Something is wrong: same number of lines with 2 or 3 values')
        pass
#    lgr.debug('Accepted %d lines out of %d', len(datalines), len(lines))
    return datalines, headerlines


class colfile:
    def __init__(self, x, y, e, arr):
        self.x = x
        self.y = y
        self.e = e
        self.arr = arr


def fromcols(fname, usecols=None, maxbytes=-1):
    data, header = linecheck(fname, maxbytes)
    dar = np.array(data).T
    ### find X
    if usecols is None:
        try:
            for n, col in enumerate(dar):
                if all(np.diff(col)>0) & all(np.diff(col)<1):
                    x = col
                    xn = n
                    break
            y = dar[xn+1]
            try:
                e = dar[xn+2]
            except IndexError:
                e = np.zeros(y.shape)
        except Exception as err:
            print(traceback.format_exc())
#            lgr.warning(traceback.format_exc())
#            lgr.warning('Retry using specific column numbers (argument --cols)')
            return
    elif len(usecols) == 2:
        x = dar[usecols[0]]
        y = dar[usecols[1]]
        e = np.zeros(y.shape)
    elif len(usecols) == 3:
        x = dar[usecols[0]]
        y = dar[usecols[1]]
        try:
            e = dar[usecols[2]]
        except Exception as err:
            print(traceback.format_exc())
            e = np.zeros(y.shape)
    return data, header, colfile(x, y, e, dar)


def get_xye(argfiles, usecols, maxbytes, label):
    argfiles = [glob(f'{arg}') for arg in argfiles  ]
    argfiles = sorted(set([j for i in argfiles for j in i]))
    names, data = [], []
    for ind, f in enumerate(argfiles):
        print(f'{ind:<4d}. {f}', end=': ')
        if os.path.isfile(f) is False:
            print('no file')
        else:
            try:
                cf = fromcols(f, usecols, maxbytes)[-1]
                print(f'{len(cf.x)} points')
                data.append([cf.x, cf.y, cf.e])
                if '/' in f:
                    sep = '/'
                elif '\\' in f:
                    sep = '\\'
                else:
                    sep = '\\'
                if label == 'index':
                    names.append(f.split(sep)[-1].split('.')[0].split('_')[-1])
                elif label == 'prefix':
                    names.append(f.split(sep)[-1].split('.')[0])
                elif label == 'dir':
                    names.append('/'.join(os.path.abspath(f).split(sep)[-2:]).split('.')[0])
                elif label == 'full':
                    names.append(os.path.abspath(f))
            except Exception as err:
                print(traceback.format_exc())
                print(err)
                continue
    return data, names
