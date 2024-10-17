from setuptools import setup, find_packages

setup(
    name='evalscope-perf',
    version='0.1.2',
    author = 'Junjian Wang',
    author_email = 'vwarship@163.com',
    description = '大模型性能压测可视化',
    long_description = 'file: README.md',
    long_description_content_type = 'text/markdown',
    url = 'http://www.wangjunjian.com',
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
            'evalscope-perf=evalscope_perf.main:app',
        ],
    },
)