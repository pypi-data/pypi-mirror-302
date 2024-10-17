from setuptools import setup, find_packages

setup(
    name='evalscope-perf',
    version='0.1.3',
    author = 'Junjian Wang',
    author_email = 'vwarship@163.com',
    description = '大模型性能压测可视化',
    url = 'http://www.wangjunjian.com',
    packages=find_packages(),
    install_requires=[
        # 在这里添加你的依赖包，例如：
        # 'requests',
        'typer',
        'pandas',
        'matplotlib',
        # 'evalscope',  # 太大了，不建议直接依赖
    ],
    entry_points={
        'console_scripts': [
            # 在这里添加你的命令行工具，例如：
            'evalscope-perf=evalscope_perf.main:app',
        ],
    },
)