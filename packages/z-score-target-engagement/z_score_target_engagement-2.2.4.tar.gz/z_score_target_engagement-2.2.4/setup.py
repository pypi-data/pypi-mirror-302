from setuptools import setup, find_packages

# # Reading dependencies from the environment.yml file (if applicable)
# def read_dependencies_from_yml(filename):
#     import yaml
#     with open(filename, 'r') as file:
#         data = yaml.safe_load(file)
#         return data.get('dependencies', [])

# # Read dependencies from environment.yml if it exists
# dependencies = read_dependencies_from_yml('environment.yml')

setup(
    name='z_score_target_engagement',  
    version='2.2.4',                    
    packages=find_packages(),            
    include_package_data=True,          
    package_data={
        'z_score_target_engagement': ['data/*.json', 'data/*.txt'],  
    },
#     entry_points={
#         'console_scripts': [
#             'analysis_script = scripts.analysis_script:main',  

#         ],
#     },
#     install_requires=dependencies,  
#     author='Lillian Tatka',          
#     description='A package for z-score target engagement analysis', 
#     long_description=open('README.md').read(),  
#     long_description_content_type='text/markdown',  
#     url='http://your.package.url',   # Replace with your package's URL if available
#     classifiers=[                    # Classifiers help users find your package
#         'Programming Language :: Python :: 3',
#         'License :: OSI Approved :: MIT License',  # Replace with your license
#         'Operating System :: OS Independent',
#     ],
#     python_requires='>=3.6',         # Specify the minimum Python version
)