import sys
import argparse
import os
import shutil
import datetime

def is_valid_path(parser, arg):
    if not os.path.exists(arg):
        parser.error("That directory does not exist: %s" % arg)
    else:
       return arg

def createNode(directory, nodeType, parent):
    if os.path.exists(directory):
        if nodeType != 'directory' and nodeType != 'file':
            raise ValueError('Incorrect Node Type')
        pathName = os.path.split(directory)[1]
        node = {'name': pathName, 'children':[], 'path': directory, 'parent':parent, 'type':nodeType}
        return node
    else:
        raise ValueError('Invalid path')
        

class Main_Backup:
    def __init__(self, args):
        self.check_valid(args)
        self.oldRoot = os.path.abspath(args['inputDirectory'])
        newRoot = os.path.abspath(args['outputDirectory'])
        #os.chdir((os.path.abspath(args['inputDirectory'])))
        self.root = ""
        self.crawl(args['year'])
        self.rebuild(self.oldRoot, newRoot)
        
    def check_valid(self, args):
        if not os.path.exists(os.path.abspath(args['inputDirectory'])):
            raise ValueError("Invalid input path given")
        if not type(args['moveArg']) == bool or not type(args['overrideArg']) == bool:
            raise ValueError('Move arg or Override arg was not given a boolean')
        if args['year'] > datetime.datetime.now().year:
            raise ValueError('Provided year is greater than the current year.\n What are you, some kind of time traveler?')
        
    def crawl(self, start):
        parent = ""
        #for root, dirs, files in os.walk(os.getcwd()):
        for root, dirs, files in os.walk(self.oldRoot):
            if parent == "":
                parent = createNode(root, 'directory', parent)
                for d in dirs:
                    parent['children'].append(createNode(os.path.join(root,d),'directory',parent))
                for f in files:
                    parent['children'].append(createNode(os.path.join(root,f),'file',parent))
                self.root = parent
            elif not self.noDirectories(parent):
                    parent = parent['parent']
                    while not self.hasChild(parent, root):
                        parent = parent['parent']
                    parent = self.getChild(parent, root)
                    for d in dirs:
                        parent['children'].append(createNode(os.path.join(root,d),'directory',parent))
                    for f in files:
                        parent['children'].append(createNode(os.path.join(root,f),'file',parent))
                
            else:
                parent = self.getChild(parent, root)
                for d in dirs:
                    parent['children'].append(createNode(os.path.join(root,d),'directory',parent))
                for f in files:
                    parent['children'].append(createNode(os.path.join(root,f),'file',parent))
                

    def rebuild(self, oldRoot, newRoot):
        queue = [self.root]
        while queue:
            node = queue.pop()
            for child in node['children']:
                path = child['path'].replace(oldRoot, '')
                path = newRoot + path
                if child['type'] == 'directory' and not os.path.exists(path):
                    os.mkdir(path)
                elif not os.path.exists(path):
                    shutil.copy2(child['path'], path)
                queue.append(child)

    def noDirectories(self, parent):
        for child in parent['children']:
            if child['type'] == 'directory':
                return True
        return False

    def hasChild(self, parent, path):
        for child in parent['children']:
            if child['path'] == path:
                return True
        return False
    
    def getChild(self, parent, path):
        for node in parent['children']:
            if node['path'] == path:
                return node
    

if __name__ == '__main__':
    argparse = argparse.ArgumentParser(description="Backup files from commandline")
    argparse.add_argument('-i', dest='inputDirectory',required=True, help='Input directory',type=lambda x: is_valid_path(argparse,x))
    argparse.add_argument('-b', dest='outputDirectory',required=True, help='Output directory',type=lambda x: is_valid_path(argparse,x))
    argparse.add_argument('-y', dest='year',required=True, help='Year for backup',type=int)
    argparse.add_argument('-m', dest='moveArg',action='store_true', help='Add to enable moving files. Without this argument the program defaults to copying',default=False)
    argparse.add_argument('-o', dest='overrideArg',action='store_true', help='Add to enable overriding of existing files in the output location. Off by default',default=False)
    args = vars(argparse.parse_args())
    main = Main_Backup(args)


