from setuptools import setup, find_packages

setup(
    name='nescli',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'qrcode',
        'requests',
        # 'pyzxing',
        'opencv-python',
    ],
    entry_points={
        'console_scripts': [
            'tree = nescli.commands.tree:tree',
            'pkg = nescli.commands.pypkg:pkg',
            'f = nescli.commands.file:cli',
            'qr = nescli.commands.qrconsole:qrconsole'
        ],
    },
)
