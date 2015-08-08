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

    def test_Positive_crawl(self):
        args = {'moveArg':False, 'startYear':2000, 'endYear':2015, 'inputDirectory': 'data',
                'outputDirectory':'C:\\Users\\Alex\\Desktop', 'overrideArg':False}
        mainBU = bu.Main_Backup(args)
        root = mainBU.root
        self.assertIsInstance(root, dict)
        self.assertEqual(root['name'], 'data')
        self.assertEqual(root['children'], [])
        self.assertEqual(root['path'], 'C:\\Users\\Alex\\Documents\\GitHub\\File-Backup-Program\\tests\\data')

        
        
