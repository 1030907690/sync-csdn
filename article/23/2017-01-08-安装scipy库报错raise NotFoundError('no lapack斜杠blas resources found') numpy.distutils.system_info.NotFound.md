---
layout:					post
title:					"安装scipy库报错raise NotFoundError('no lapack/blas resources found') numpy.distutils.system_info.NotFound"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
​
安装scipy库报错，我是安装了numpy的

Running from scipy source directory.
Traceback (most recent call last):
  File "setup.py", line 253, in <module>
    setup_package()
  File "setup.py", line 250, in setup_package
    setup(**metadata)
  File "/usr/local/lib/python3.5/site-packages/numpy-1.11.2-py3.5-linux-i686.egg/numpy/distutils/core.py", line 135, in setup
    config = configuration()
  File "setup.py", line 175, in configuration
    config.add_subpackage('scipy')
  File "/usr/local/lib/python3.5/site-packages/numpy-1.11.2-py3.5-linux-i686.egg/numpy/distutils/misc_util.py", line 1000, in add_subpackage
    caller_level = 2)
  File "/usr/local/lib/python3.5/site-packages/numpy-1.11.2-py3.5-linux-i686.egg/numpy/distutils/misc_util.py", line 969, in get_subpackage
    caller_level = caller_level + 1)
  File "/usr/local/lib/python3.5/site-packages/numpy-1.11.2-py3.5-linux-i686.egg/numpy/distutils/misc_util.py", line 906, in _get_configuration_from_setup_py
    config = setup_module.configuration(*args)
  File "scipy/setup.py", line 15, in configuration
    config.add_subpackage('linalg')
  File "/usr/local/lib/python3.5/site-packages/numpy-1.11.2-py3.5-linux-i686.egg/numpy/distutils/misc_util.py", line 1000, in add_subpackage
    caller_level = 2)
  File "/usr/local/lib/python3.5/site-packages/numpy-1.11.2-py3.5-linux-i686.egg/numpy/distutils/misc_util.py", line 969, in get_subpackage
    caller_level = caller_level + 1)
  File "/usr/local/lib/python3.5/site-packages/numpy-1.11.2-py3.5-linux-i686.egg/numpy/distutils/misc_util.py", line 906, in _get_configuration_from_setup_py
    config = setup_module.configuration(*args)
  File "scipy/linalg/setup.py", line 20, in configuration
    raise NotFoundError('no lapack/blas resources found')
numpy.distutils.system_info.NotFoundError: no lapack/blas resources found
我的是centos6.5

yum install lapack lapack-devel blas blas-devel
python3.5 setup.py install 


​