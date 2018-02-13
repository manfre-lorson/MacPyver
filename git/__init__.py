# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 14:12:17 2018

@author: Florian Wolf


@work: with the git class you can interact with you git repo
        
"""


import os
import subprocess
from glob import glob
import site


class git():
    """git() can work as normal git, to check branch...
        is checking in the python site-package folder
        
        init will create the branches, active branch 
        and the path to the repository
        
        checkout will change the active branch to the given name
        --> is the git checkout command
        
        get_active creates the active method (is used by init)
        
        custom allows you to pass a custom git command"""

    def __init__(self, repo_name, verbose=False):
        #get location of site-packages
        path = []
        sitepackages = site.getsitepackages()
        self.verbose = verbose
        for package in sitepackages:
            pck = glob(package + os.sep + repo_name)
            if pck:
                path.extend(pck)            

        if len(path) == 1:
            self.repo = path[0]
            if verbose:
                self.verbose = True
                
            #get list of existing branches
            os.chdir(self.repo)
            cmd = subprocess.Popen('git branch', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (output, error) = cmd.communicate()
            if not error:
                self.branches = []
                branches = output[2:-1].split('\n')
                for b in branches:
                    if b:
                        b = b.replace('*', '')
                        self.branches.append(b.strip())
                self.get_active()
                if self.verbose:
                    if len(self.branches)>1:
                        branchlist = self.branches[:]
                        branchlist.remove(self.active)
                        print "other existing branches are:\n{0}".format(('').join(['--> {0}\n'.format(x) for x in branchlist])) 
            
            else:
                print "ERROR: in reading braches"
                print error.decode()
        elif len(path) < 1:
            print 'no package found with name {0} (in {1})'.format(repo_name, sitepackages)
            None
            self.verbose=True
        elif len(path) > 1:
            print 'to many packages with the same name'
            print '{0}'.format(path)
            None
            self.verbose = True
            
            
    def __call__(self):
        try:
            if self.repo:
                if hasattr(self, 'verbose'):
                    print "object is initialized"
                return True
        except:
            if hasattr(self, 'verbose'):
                print "not a valid object"
                print "returned None"
            return None
        
        
    def checkout(self, branch_name, verbose = False):
        "change branch (git command = checkout)"
        self.ckpath()
        if branch_name in self.branches:
            cmd = subprocess.Popen('git checkout {0}'.format(branch_name), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            (output, error) = cmd.communicate()
            if verbose and output:
                print output.decode()
            if verbose and error:
                print error.decode()
     
     
    def get_active(self):
        '''get the active branch of the repo'''
        self.ckpath()
        cmd = subprocess.Popen('git rev-parse --abbrev-ref HEAD', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, error) = cmd.communicate()
        if not error:
            self.active = output[:-1]
            if self.verbose:
                print "your current active branch is\n--> {0}\n".format(self.active)
        else:
            print "ERROR: in HEAD"
            self.active = None       
            if self.verbose:
                "could not find the active branch, don't know what went wrong"
    
    def custom(self, command):
        '''pass a custom git command'''
        self.ckpath()
        if command.startswith('git'):
            command.replace('git ','')
        cmd = subprocess.Popen('git {0}'.format(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (output, error) = cmd.communicate()
        if not error:
            print output
        else:
            print error
            
    def ckpath(self):
        if os.getcwd() != self.repo:
            os.chdir(self.repo)
            if self.verbose:
                print 'changed current working directory to\n--> {0}'.format(self.repo)
        else:
            if self.verbose:
                print 'you are in the git repository\n--> {0}\n'.format(self.repo)