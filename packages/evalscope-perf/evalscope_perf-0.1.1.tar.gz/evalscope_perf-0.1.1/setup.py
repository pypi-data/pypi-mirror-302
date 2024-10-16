from setuptools import setup, find_packages

setup(
    name='evalscope-perf',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        # 在这里添加你的依赖包，例如：
        # 'requests',
        'typer',
        'pandas',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            # 在这里添加你的命令行工具，例如：
            'evalscope-perf=evalscope_perf:main',
        ],
    },
)