from setuptools import setup, find_packages

setup(
   version="0.0.1",
   name="fundar",
   author="Fundar",
   description="Python library.",
   packages=find_packages(),
   include_package_data=True,
   classifiers=[
       "Intended Audience :: Developers",
       "Operating System :: OS Independent"
   ],
   python_requires='>=3.10',
   setup_requires=['setuptools-git-versioning'],
   version_config={
       "dirty_template": "{tag}",
   }
)
