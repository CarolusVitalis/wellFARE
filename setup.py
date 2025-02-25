try:
    from setuptools import setup
except ImportError:
    try:
        import ez_setup
        ez_setup.use_setuptools()
    except ImportError:
        raise ImportError("wellFARE could not be installed, probably because"
                          " neither setuptools nor ez_setup are installed on this computer."
                          "\nInstall ez_setup ([sudo] pip install ez_setup) and try again.")

from setuptools import setup, find_packages


from setuptools import setup, find_packages

setup(name='wellfare',
      version='0.1.1',
      author='Valentin',
      description='',
      long_description=open('README.rst').read(),
      license='see LICENSE.txt',
      keywords="",
      install_requires=['numpy>=1.9.1',
                        'scipy>=0.9.0',
                        'docopt>=0.6.1',
                        'xlrd>=0.9.2'],
      packages=find_packages(exclude=['docs', 'examples']))
