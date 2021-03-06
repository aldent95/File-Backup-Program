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

def createNode(directory, nodeType, parent,filtered):
    if os.path.exists(directory):
        if nodeType != 'directory' and nodeType != 'file':
            raise ValueError('Incorrect Node Type')
        pathName = os.path.split(directory)[1]
        node = {'name': pathName, 'children':[], 'path': directory, 'parent':parent, 'type':nodeType, 'filtered':filtered}
        return node
    else:
        raise ValueError('Invalid path')
        
def tryInt(string):
    try:
        return int(string)
    except ValueError:
        return -1


class Main_Backup:
    def __init__(self, args):
        self.check_valid(args)
        self.oldRoot = os.path.abspath(args['inputDirectory'])
        newRoot = os.path.abspath(args['outputDirectory'])
        #os.chdir((os.path.abspath(args['inputDirectory'])))
        self.root = ""
        self.crawl(args['year'])
        if(args['deleteArg']):
            self.delete()
        else:
            self.rebuild(self.oldRoot, newRoot, args['overrideArg'])
        
    def check_valid(self, args):
        if not os.path.exists(os.path.abspath(args['inputDirectory'])):
            raise ValueError("Invalid input path given")
        if not type(args['deleteArg']) == bool or not type(args['overrideArg']) == bool:
            raise ValueError('Move arg or Override arg was not given a boolean')
        if args['year'] > datetime.datetime.now().year:
            raise ValueError('Provided year is greater than the current year.\n What are you, some kind of time traveler?')
    #Status marks
    #0:Don't copy
    #1: Client Folder
    #2: Year Folder
    #3: File or folder inside year folder
    #4: Parent folder to copy
    #5: Client folder to copy
    def crawl(self, start):
        parent = ""
        noFilteredFound = True
        for root, dirs, files in os.walk(self.oldRoot):
            if parent == "":
                parent = createNode(root, 'directory', parent, 0)
                for d in dirs:
                    parent['children'].append(createNode(os.path.join(root,d),'directory',parent, 0))
                self.root = parent
            elif not self.noDirectories(parent):
                    temp = parent['parent']
                    
                    while not self.hasChild(temp, root):
                        if temp == self.root:
                            break
                        temp = temp['parent']
                    if temp == self.root:
                        continue
                    parent = self.getChild(temp, root)
                    if parent['filtered'] == 0:
                        noFilteredFound = True
                    else:
                        noFilteredFound = False 
                    for d in dirs:
                        child=createNode(os.path.join(root,d),'directory',parent, 0)
                        if ((parent['filtered'] == 1 or parent['filtered'] == 5) and str(start) in child['name']):
                            noFilteredFound = False
                            child['filtered'] =2
                            self.markParent(child)
                            parent['children'].append(child)
                        elif (parent['filtered'] == 0 and 1000 <= tryInt(child['name']) <= 9999):
                            noFilteredFound = False
                            child['filtered'] = 1
                            parent['children'].append(child)
                        elif noFilteredFound == True or parent['filtered'] == 2 or parent['filtered']==3:
                            if parent['filtered'] == 2 or parent['filtered']==3:
                                child['filtered'] = 3
                            parent['children'].append(child)
                    for f in files:
                        if parent['filtered'] == 2 or parent['filtered'] == 3:
                            parent['children'].append(createNode(os.path.join(root,f),'file',parent, 3))
                
            else:
                temp = self.getChild(parent, root)
                if temp == None:
                    continue
                parent = temp
                for d in dirs:
                    child=createNode(os.path.join(root,d),'directory',parent, 0)
                    if ((parent['filtered'] == 1 or parent['filtered'] == 5) and str(start) in child['name']):
                        noFilteredFound = False
                        child['filtered'] =2
                        self.markParent(child)
                        parent['children'].append(child)
                    elif (parent['filtered'] == 0 and 1000 <= tryInt(child['name']) <= 9999):
                        noFilteredFound = False
                        child['filtered'] = 1
                        parent['children'].append(child)
                    elif noFilteredFound == True or parent['filtered'] == 2 or parent['filtered']==3:
                        if parent['filtered'] == 2 or parent['filtered']==3:
                            child['filtered'] = 3
                        parent['children'].append(child)
                for f in files:
                    if parent['filtered'] == 2 or parent['filtered'] == 3:
                        parent['children'].append(createNode(os.path.join(root,f),'file',parent, 3))
                

    def rebuild(self, oldRoot, newRoot, override):
        queue = [self.root]
        while queue:
            node = queue.pop()
            for child in node['children']:
                if child['filtered'] == 0 or child['filtered'] == 1:
                    continue
                path = child['path'].replace(oldRoot, '')
                path = newRoot+'\\' + path
                if child['type'] == 'directory' and not os.path.exists(path):
                    os.mkdir(path)
                elif child['type'] == 'file' and (not os.path.exists(path) or override == True):
                    shutil.copy2(child['path'], path)
                queue.append(child)
    def markParent(self, node):
        while(node != ""):
            if node['filtered'] == 0: 
                node['filtered'] = 4
            if node['filtered'] == 1:
                node['filtered'] = 5
            node = node['parent']
    def delete(self):
        queue = [self.root]
        while queue:
            node = queue.pop()
            if node['filtered'] == 2:
                shutil.rmtree(node['path'])
            else:
                [queue.append(child) for child in node['children']]
                

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
    argparse.add_argument('-d', dest='deleteArg',action='store_true', help='Use to delete files after you have already run the program one time for the copy',default=False)
    argparse.add_argument('-o', dest='overrideArg',action='store_true', help='Add to enable overriding of existing files in the output location. Off by default',default=False)
    args = vars(argparse.parse_args())
    main = Main_Backup(args)


