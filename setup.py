from setuptools import setup, find_packages

setup(name='PortfolioAnalysis',

      version='1.0',

      url='http://qraftec.com',

      license='MIT',

      author='hyojun.moon',

      author_email='hyojun.moon@qraftec.com',

      description='Manage configuration files',

      classifiers=[

          'Development Status :: 3 - Alpha',

          'Intended Audience :: Developers',

          'Topic :: Software Development :: Libraries',

          'License :: OSI Approved :: MIT License',

          'Programming Language :: Python :: 3.6',

      ],

      packages=find_packages(),

      long_description=open('README.md').read(),

      zip_safe=False,

      setup_requires=['bokeh>=0.12.16', 'numpy>=1.14.3', 'pandas>=0.23.0']
      )