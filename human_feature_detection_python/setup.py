from setuptools import find_packages, setup

package_name = 'human_feature_detection_python'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/human_feature_detection.launch.py']),  
        ('share/' + package_name + '/images', ['images/sample_image.png']),        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='sobits',
    maintainer_email='sobits@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'feature_detect = human_feature_detection_python.feature_detect:main',
            'sample_2d = example.sample_2d:main'
        ],
    },
)
