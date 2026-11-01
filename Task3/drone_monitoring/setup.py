from setuptools import find_packages, setup

package_name = 'drone_monitoring'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Yuvvraj Kalra',
    maintainer_email='yuvvrajkalra60@gmail.com',
    description='Simulated drone telemetry and monitoring system.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'sensor_publisher = drone_monitoring.sensor_publisher:main',
            'telemetry_monitor = drone_monitoring.telemetry_monitor:main',
            'warning_publisher = drone_monitoring.warning_publisher:main',
        ],
    },
)
