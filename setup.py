import os
from glob import glob
from setuptools import find_packages, setup

package_name = "susumu_respeaker_ros"

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        # launchファイルをインストール対象に含める (launch/*.launch.py など)
        (os.path.join('share', package_name, 'launch'),
            glob(os.path.join('launch', '*.launch.*'))),
    ],
    install_requires=[
        'setuptools',
        # 以下、pipでインストールさせたいPythonライブラリ
        'pyaudio',
        'numpy',
        'torch',
        'vosk',
        'google-cloud-speech',
        'openwakeword',
    ],
    zip_safe=True,
    maintainer='Sato Susumu',
    maintainer_email='75652942+sato-susumu@users.noreply.github.com',
    description='TODO: Package description',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # ROS 2 ノードとして起動する際に呼び出せるエントリポイントを指定
            # ここで指定した名前を、launchファイル等から `executable=` に使うことが多い
            'susumu_asr_node = susumu_asr_ros.susumu_asr_node:main',
        ],
    },
)
