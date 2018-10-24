"""Regression tests for 2uuy complex"""

import shutil
import os
import filecmp
from test.regression import RegressionTest


class TestRegression1ppe(RegressionTest):

    def setup(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.test_path = self.path + '/scratch_2uuy/'
        self.ini_test_path()
        self.golden_data_path = os.path.join(os.path.normpath(os.path.dirname(os.path.realpath(__file__))), 'golden')

    def teardown(self):
        self.clean_test_path()

    def test_1ppe(self):
        os.chdir(self.test_path)
        command = "python ../../../interface_classifier.py {} | tail -n +2 > prediction".format(os.path.join(self.golden_data_path, '2uuy.pdb'))
        os.system(command)

        assert filecmp.cmp(os.path.join(self.golden_data_path, '2uuy_prediction.txt'), os.path.join(self.test_path, 'prediction'))
