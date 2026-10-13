from setuptools import find_packages, setup

package_name = 'system_check'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='master26',
    maintainer_email='mololuwaadeniyi@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'motor_safety_ctrl = system_check.motor_safety_ctrl_node:main',
            'robot_safety_ctrl = system_check.robot_safety_check_node:main', 
        ],
    },
)
