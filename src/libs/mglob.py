#!/usr/bin/env python

r""" mglob - enhanced file list expansion module

Use as stand-alone utility (for xargs, `backticks` etc.),
or a globbing library for own python programs. Globbing the sys.argv is something
that almost every Windows script has to perform manually, and this module is here
to help with that task. Also Unix users will benefit from enhanced modes
such as recursion, exclusion, directory omission...

Unlike glob.glob, directories are not included in the glob unless specified
with 'dir:'

'expand' is the function to use in python programs. Typical use
to expand argv (esp. in windows)::

    try:
        import mglob
        files = mglob.expand(sys.argv[1:])
    except ImportError:
        print "mglob not found; try 'easy_install mglob' for extra features"
        files = sys.argv[1:]

Note that for unix, shell expands *normal* wildcards (*.cpp, etc.) in argv.
Therefore, you might want to use quotes with normal wildcards to prevent this
expansion, in order for mglob to see the wildcards and get the wanted behaviour.
Not quoting the wildcards is harmless and typically has equivalent results, though.

Author: Ville Vainio <vivainio@gmail.com>
License: MIT Open Source license

"""

#Assigned in variable for "usage" printing convenience"

globsyntax = """\
This program allows specifying filenames with "mglob" mechanism.
Supported syntax in globs (wilcard matching patterns)::

 *.cpp ?ellowo*
     - obvious. Differs from normal glob in that dirs are not included.
       Unix users might want to write this as: "*.cpp" "?ellowo*"
 rec:/usr/share=*.txt,*.doc
     - get all *.txt and *.doc under /usr/share,
       recursively
 rec:/usr/share
     - All files under /usr/share, recursively
 rec:*.py
     - All .py files under current working dir, recursively
 foo
     - File or dir foo
 !*.bak readme*
     - readme*, exclude files ending with .bak
 !.svn/ !.hg/ !*_Data/ rec:.
     - Skip .svn, .hg, foo_Data dirs (and their subdirs) in recurse.
       Trailing / is the key, \ does not work!
 dir:foo
     - the directory foo if it exists (not files in foo)
 dir:*
     - all directories in current folder
 foo.py bar.* !h* rec:*.py
     - Obvious. !h* exclusion only applies for rec:*.py.
       foo.py is *not* included twice.
 @filelist.txt
     - All files listed in 'filelist.txt' file, on separate lines.
 """


__version__ = "0.4"


import os
import glob
import fnmatch
import sys


def expand(flist,exp_dirs = False):
    """ Expand the glob(s) in flist.

    flist may be either a whitespace-separated list of globs/files
    or an array of globs/files.

    if exp_dirs is true, directory names in glob are expanded to the files
    contained in them - otherwise, directory names are returned as is.

    """
    if isinstance(flist, basestring):
        flist = flist.split()
    done_set = set()
    denied_set = set()

    def recfind(p, pats = ["*"]):
        denied_dirs = ["*" + d+"*" for d in denied_set if d.endswith("/")]
        #print "de", denied_dirs
        for (dp,dnames,fnames) in os.walk(p):
            # see if we should ignore the whole directory
            dp_norm = dp.replace("\\","/") + "/"
            deny = False
            #print "dp",dp
            for deny_pat in denied_dirs:
                if fnmatch.fnmatch( dp_norm, deny_pat):
                    deny = True
                    break
            if deny:
                continue


            for f in fnames:
                matched = False
                for p in pats:
                    if fnmatch.fnmatch(f,p):
                        matched = True
                        break
                if matched:
                    yield os.path.join(dp,f)

    def once_filter(seq):
        for it in seq:
            p = os.path.abspath(it)
            if p in done_set:
                continue
            done_set.add(p)
            deny = False
            for deny_pat in denied_set:
                if fnmatch.fnmatch(os.path.basename(p), deny_pat):
                    deny = True
                    break
            if not deny:
                yield it
        return

    res = []

    for ent in flist:
        ent = os.path.expanduser(os.path.expandvars(ent))
        if ent.lower().startswith('rec:'):
            fields = ent[4:].split('=')
            if len(fields) == 2:
                pth, patlist = fields
            elif len(fields) == 1:
                if os.path.isdir(fields[0]):
                    # single arg is dir
                    pth, patlist = fields[0], '*'
                else:
                    # single arg is pattern
                    pth, patlist = '.', fields[0]

            elif len(fields) == 0:
                pth, pathlist = '.','*'

            pats = patlist.split(',')
            res.extend(once_filter(recfind(pth, pats)))
        # filelist
        elif ent.startswith('@') and os.path.isfile(ent[1:]):
            res.extend(once_filter(open(ent[1:]).read().splitlines()))
        # exclusion
        elif ent.startswith('!'):
            denied_set.add(ent[1:])
        # glob only dirs
        elif ent.lower().startswith('dir:'):
            res.extend(once_filter(filter(os.path.isdir,glob.glob(ent[4:]))))

        # get all files in the specified dir
        elif os.path.isdir(ent) and exp_dirs:
            res.extend(once_filter(filter(os.path.isfile,glob.glob(ent + os.sep+"*"))))

        # glob only files

        elif '*' in ent or '?' in ent:
            res.extend(once_filter(filter(os.path.isfile,glob.glob(ent))))

        else:
            res.extend(once_filter([ent]))
    return res


def test():
    assert (
        expand("*.py ~/.ipython/*.py rec:/usr/share/doc-base") ==
        expand( ['*.py', '~/.ipython/*.py', 'rec:/usr/share/doc-base'] )
        )

def main():
    if len(sys.argv) < 2:
        print globsyntax
        return

    print "\n".join(expand(sys.argv[1:])),

def mglob_f(self, arg):
    from IPython.genutils import SList
    if arg.strip():
        return SList(expand(arg))
    print "Please specify pattern!"
    print globsyntax

def init_ipython(ip):
    """ register %mglob for IPython """
    mglob_f.__doc__ = globsyntax
    ip.expose_magic("mglob",mglob_f)

# test()
if __name__ == "__main__":
    main()
