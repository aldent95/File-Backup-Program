import unittest
import os,sys
lib_path = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))
sys.path.append(lib_path)
import backup as bu
import argparse

class TestBackupMethods(unittest.TestCase):
    def test_Positive_is_valid_path(self):
        parser = argparse.ArgumentParser(description='UnitTestParser')
        self.assertTrue(bu.is_valid_path(parser, os.getcwd()))
        

    def test_Negative_is_valid_path(self):
        parser = argparse.ArgumentParser(description='UnitTestParser')
        with self.assertRaises(SystemExit) as cm:
            bu.is_valid_path(parser, os.path.join(os.getcwd(),"fail"))
            self.assertEqual(cm.exception.code, 2)
        
    def test_Positive_createNode(self):
        node = bu.createNode('C:\\Users\\Alex', 'directory', 'parent')
        self.assertIsInstance(node, dict)
        self.assertEqual(node['name'], 'Alex')
        self.assertEqual(node['children'], [])
        self.assertEqual(node['path'], 'C:\\Users\\Alex')
        self.assertEqual(node['type'], 'directory')
        self.assertEqual(node['parent'], 'parent')

    def test_Negative_createNode(self):
        with self.assertRaises(ValueError):
            node = bu.createNode('C:\\Fail', 'fail', 'fail')
        with self.assertRaises(ValueError):
            node = bu.createNode('C:\\Users','fail','fail')

    def test_Positive_crawl(self):
        args = {'moveArg':False, 'year':2000, 'inputDirectory': 'dirtest',
                'outputDirectory':'dirtest', 'overrideArg':False}
        mainBU = bu.Main_Backup(args)
        root = mainBU.root
        self.assertIsInstance(root, dict)
        self.assertEqual(root['name'], 'dirtest')
        self.assertEqual(root['children'], [])
        self.assertEqual(root['path'], 'C:\\Users\\Alex\\Documents\\GitHub\\File-Backup-Program\\tests\\dirtest')
    #Crawl doesn't have any negative sides to test as all its parameters are checked by __init__


    #Positive args tests are done by other test methods, no need to do twice
    def test_Negative_args(self):
        args = {'moveArg':False, 'year':2000, 'inputDirectory': 'fail',
                'outputDirectory':'dirtest', 'overrideArg':False}
        with self.assertRaises(ValueError):
            mainBU = bu.Main_Backup(args)
        args = {'moveArg':1, 'year':2000, 'inputDirectory': 'dirtest',
                'outputDirectory':'dirtest', 'overrideArg':False}
        with self.assertRaises(ValueError):
            mainBU = bu.Main_Backup(args)
        args = {'moveArg':False, 'year':2000, 'inputDirectory': 'dirtest',
                'outputDirectory':'dirtest', 'overrideArg':1}
        with self.assertRaises(ValueError):
            mainBU = bu.Main_Backup(args)
        args = {'moveArg':False, 'year':9999, 'inputDirectory': 'dirtest',
                'outputDirectory':'dirtest', 'overrideArg':False}
        with self.assertRaises(ValueError):
            mainBU = bu.Main_Backup(args)

    def test_Positive_rebuild(self):
        #Very hard to actually test if it rebuilds correctly without manually checking, so we make do with ensureing no
        #errors appear
        args = {'moveArg':False, 'year':2000, 'inputDirectory': 'F',
                'outputDirectory':'testDump', 'overrideArg':False}
        mainBU = bu.Main_Backup(args)
