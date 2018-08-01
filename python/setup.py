from setuptools import setup
import unittest

def my_test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test*.py')
    return test_suite

setup(name='escaperoom',
      version='0.1',
      description='Escaperoom text adventure using Google DialogFlow',
      url='http://github.com/themainingredient/escaperoom',
      author='Erik van der Pluijm',
      author_email='erik@themainingredient.co',
      license='MIT',
      packages=['escaperoom'],
      install_requires=[
          'pyaudio',
          'wave',          
          'google-cloud-speech',          
          'google-cloud-texttospeech',
          'dialogflow'          
      ],
      test_suite='setup.my_test_suite',
      zip_safe=False)