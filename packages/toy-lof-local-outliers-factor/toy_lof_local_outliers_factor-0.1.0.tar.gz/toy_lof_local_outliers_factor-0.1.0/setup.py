from setuptools import setup

setup(
    name='toy_lof_local_outliers_factor',
    version='0.1.0',              # 包的版本号
    description='Python implementation of Local Outlier Factor algorithm.',
    author='Damjan Kužnar',
    py_modules=['toy_lof_local_outliers_factor'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # 指定支持的 Python 版本
)
