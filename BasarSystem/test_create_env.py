# coding: utf-8

import unittest

#from test.test_create_sellers import TestCreateSellers
#from test.test_create_paydesks import TestCreatePaydesks
#from test.test_create_articles import TestCreateArticles
from test.test_scan_process import TestScanProcess

#testmodules = ['test.test_create_sellers',]

# initialize the test suite
#loader = unittest.TestLoader()
#suite  = unittest.TestSuite()

'''
for t in testmodules:
    try:
        mod=__import__(t,globals(), locals(), ['suite'])
        suitefn = getattr(mod,'suite')
        suite.addTest(suitefn())
    except:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))

suite_1=unittest.makeSuite(TestCreateSellers)
suite.addTest(suite_1)
'''
#suite_2=unittest.makeSuite(TestCreatePaydesks)
#suite.addTest(suite_2)

#suite_3=unittest.makeSuite(TestCreateArticles)
#suite.addTest(suite_3)
'''
suite_4=unittest.makeSuite(TestScanProcess)
suite.addTest(suite_4)
'''
# initialize a runner, pass it your suite and run it
#runner = unittest.TextTestRunner(verbosity=1)
#result = runner.run(suite)