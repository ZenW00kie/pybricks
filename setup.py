from setuptools import setup

requires =[
    'databricks-cli',
    'requests>==2.18.4'
]

setup(name='pybricks',
      version='0.0.1',
      description='Wrapper on Databricks CLI and API',
      author='Ron Thompson',
      packages=['pybricks'],
      package_data= {
          '':['*.json']
      },
      install_requires=requires)
