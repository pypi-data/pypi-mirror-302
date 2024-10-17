from setuptools import setup, find_packages

# 运行installMode安装依赖库
setup(
    name='PyMyMethods',
    version='1.0.4',
    author='Mikuas',
    packages=find_packages(),
    install_requires=[
        'PySide6',
        'pyautogui',
        'easycor',
        'comtypes',
        'pycaw'
    ]
)
