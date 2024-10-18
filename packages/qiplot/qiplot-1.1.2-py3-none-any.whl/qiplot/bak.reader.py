import sys, os, re, string
import numpy as np
from glob import glob
import traceback

#def lcheck(line):
#    "Return 0:skip signal. Return 1:accept signal"
#    li = line.strip()
#    res = 0
#    if li.replace('.','').replace(' ','').isdigit or li.replace('.','').replace(',','').isdigit:
#        if re.search(',', li):
#            sep = ','
#        else:
#            sep = None
#        c = li.split(sep)
#        if len(c) > 1:
#            try:
#                x, y = float(c[0]), float(c[1])
#                res = 1
#            except:
#                return res
#    return res
#
#
#def streak(nums, show=True):
#    """
#    :type nums: List[int]
#    :rtype: int
#    example = [0, 2, 4, 7, 8, 9, 10, 20, 21, 22, 23, 24, 25, 26, 30, 33, 34, 35]
#    _streak(example, show=True)
#    """
#    nums = list(dict.fromkeys(nums))
#    best = [0,0,0] #ini, fin, len
#    curr = [0,0,0]
#    for index, value in enumerate(nums):
#        if index + 1 >= len(nums):
#            break
#        curr[0] = nums[index]
#        if nums[index + 1] != value + 1:
#            curr[1] = nums[index]
#            curr[2] = 0
#        elif nums[index + 1] == value + 1:
#            curr[2] += 1
#            curr[1] = nums[index+1]
#            curr[0] = nums[index-(curr[2]-1)]
#            if curr[2] > best[2]:
#                best[2] = curr[2]
#                best[0] = curr[0]
#                best[1] = curr[1]
#        if show==True:
#            print('current:',curr, 'best:',best)
#    return best   #actual line indices. Add 1 to final index for *range* indices
#
#
#def filelinescheck(lines):
#    "Input: list of lines from readlines()"
#    accept = []
#    for n, l in enumerate(lines):
#        res = lcheck(l)
#        if res == 1:
#            accept.append(n)
#    longest = streak(accept, show=False)
#    return longest[0], longest[1]+1
#
#def get_xye(argfiles, label, romin=0, romax=10000):
#    argfiles = [glob(f'{arg}') for arg in argfiles  ]
#    argfiles = sorted(set([j for i in argfiles for j in i]))
#    names, data = [], []
#    for ind, f in enumerate(argfiles):
#        print(f'{ind:<4d}. {f}', end='')
#        if os.path.isfile(f):
#            with open(f, 'r') as fil:
#                lines = fil.readlines()
#            romin, romax = filelinescheck(lines); print(romin)
#            try:
#                x,y,e = np.loadtxt(f, unpack=True, usecols=(0,1,2), skiprows=romin, max_rows=romax)
#            except IndexError:  #no third column
#                x,y = np.loadtxt(f, unpack=True, usecols=(0,1), skiprows=romin, max_rows=romax)
#                e = np.zeros(y.shape)
#            except StopIteration: # empty file 1
#                print('Not enough data'); sys.exit(0)
#            except ValueError: # empty file 2
#                print('Not enough data'); sys.exit(0)
#            print(f': {len(x)} points')
#            data.append([x,y,e])
#            if '/' in f:
#                sep = '/'
#            elif '\\' in f:
#                sep = '\\'
#            else:
#                sep = '\\'
#            if label == 'index':
#                names.append(f.split(sep)[-1].split('.')[0].split('_')[-1])
#            elif label == 'prefix':
#                names.append(f.split(sep)[-1].split('.')[0])
#            elif label == 'dir':
#                names.append('/'.join(os.path.abspath(f).split(sep)[-2:]).split('.')[0])
#            elif label == 'full':
#                names.append(os.path.abspath(f))
#    return data, names


########## good until 20/2/23
#def _fromstring(s, dtype=float, sep=' '):
#    try:
#        res = [dtype(i) for i in s.strip().split(sep)]
#        return res
#    except Exception as err:
#        return err
#
#
#def _stringcheck(s):
#    out, numeric = None, 0
#    for sep in [' ',',',';']:
#        res = _fromstring(s, sep=sep)
#        if isinstance(res, list) is True:
#            out = res
#            numeric = 1
#            break
#        else:
#            continue
#    return out, numeric
#
#
#def fromascii(fname, usecols=[0,1,2], maxbytes=-1):
#    with open(fname, 'r') as f:
#        lines = f.readlines(maxbytes)
#    datalines = []
#    for i, l in enumerate(lines):
#        cols, numeric = _stringcheck(l)
#        if numeric == 1:
#            try:
#                cols = [cols[i] for i in usecols]
#            except IndexError:
#                cols = [cols[i] for i in usecols[:-1]] + [0]
#            datalines.append(cols)
#    return np.array(datalines).T
#
#
#
#
#def get_xye(argfiles, usecols, maxbytes, label):
#    argfiles = [glob(f'{arg}') for arg in argfiles  ]
#    argfiles = sorted(set([j for i in argfiles for j in i]))
#    names, data = [], []
#    for ind, f in enumerate(argfiles):
#        print(f'{ind:<4d}. {f}', end=': ')
#        if os.path.isfile(f) is False:
#            print('no file')
#        else:
#            x, y, e = fromascii(f, usecols, maxbytes)
#            print(f': {len(x)} points')
#            data.append([x,y,e])
#            if '/' in f:
#                sep = '/'
#            elif '\\' in f:
#                sep = '\\'
#            else:
#                sep = '\\'
#            if label == 'index':
#                names.append(f.split(sep)[-1].split('.')[0].split('_')[-1])
#            elif label == 'prefix':
#                names.append(f.split(sep)[-1].split('.')[0])
#            elif label == 'dir':
#                names.append('/'.join(os.path.abspath(f).split(sep)[-2:]).split('.')[0])
#            elif label == 'full':
#                names.append(os.path.abspath(f))
#    return data, names
#
########## good until 20/2/23


########## added 21/2/23
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
