from setuptools import setup

setup(name='easy_jobs',
      version='0.1',
      description='Persistent job queue employing Redis',
      url='https://github.com/msempere/easy_jobs',
      author='msempere',
      author_email='msempere@gmx.com',
      license='MIT',
      packages=['easy_jobs'],
      test_suite="tests",
      zip_safe=False)
