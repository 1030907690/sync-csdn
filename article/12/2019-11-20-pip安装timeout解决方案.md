---
layout:					post
title:					"pip安装timeout解决方案"
author:					Zhou Zhongqing
header-style:				text
catalog:					true
tags:
		- Web
		- JavaScript
---
- 使用官方的源国内一般都下载较慢，很容易出现timeout
- 解决方案一 (timeout参数设置--timeout):
>pip3.5 --timeout=500 install  requests
- 解决方案二(更换更快的源-i):
> pip3.5 install -i https://pypi.tuna.tsinghua.edu.cn/simple requests
- 下面看下pip参数说明
 

```bash

G:\迅雷下载\python\requests-2.22.0>pip3.5 help

Usage:
  pip <command> [options]

Commands:
  install                     Install packages.
  download                    Download packages.
  uninstall                   Uninstall packages.
  freeze                      Output installed packages in requirements format
  list                        List installed packages.
  show                        Show information about installed packages.
  search                      Search PyPI for packages.
  wheel                       Build wheels from your requirements.
  hash                        Compute hashes of package archives.
  completion                  A helper command used for command completion
  help                        Show help for commands.

General Options:
  -h, --help                  Show help.
  --isolated                  Run pip in an isolated mode, ignoring
                              environment variables and user configuration.
  -v, --verbose               Give more output. Option is additive, and can be
                              used up to 3 times.
  -V, --version               Show version and exit.
  -q, --quiet                 Give less output.
  --log <path>                Path to a verbose appending log.
  --proxy <proxy>             Specify a proxy in the form
                              [user:passwd@]proxy.server:port.
  --retries <retries>         Maximum number of retries each connection should
                              attempt (default 5 times).
  --timeout <sec>             Set the socket timeout (default 15 seconds).
  --exists-action <action>    Default action when a path already exists:
                              (s)witch, (i)gnore, (w)ipe, (b)ackup.
  --trusted-host <hostname>   Mark this host as trusted, even though it does
                              not have valid or any HTTPS.
  --cert <path>               Path to alternate CA bundle.
  --client-cert <path>        Path to SSL client certificate, a single file
                              containing the private key and the certificate
                              in PEM format.
  --cache-dir <dir>           Store the cache data in <dir>.
  --no-cache-dir              Disable the cache.
  --disable-pip-version-check
                              Don't periodically check PyPI to determine
                              whether a new version of pip is available for
                              download. Implied with --no-index.

G:\迅雷下载\python\requests-2.22.0>pip3.5 --timeout=500 install  requests
Requirement already satisfied (use --upgrade to upgrade): requests in d:\softw
e\python\python35\lib\site-packages\requests-2.22.0-py3.5.egg
Collecting chardet<3.1.0,>=3.0.2 (from requests)
  Downloading https://files.pythonhosted.org/packages/bc/a9/01ffebfb562e4274b6
7b4bb1ddec7ca55ec7510b22e4c51f14098443b8/chardet-3.0.4-py2.py3-none-any.whl (1
kB)
    38% |████████████▎                   | 51kB 2.2kB/s eta 0:00:
    46% |██████████████▊                 | 61kB 2.1kB/s eta 0:0
    53% |█████████████████▏              | 71kB 2.4kB/s eta
    61% |███████████████████▋            | 81kB 2.8kB/s et
    69% |██████████████████████▏         | 92kB 3.1kB/s
    76% |████████████████████████▋       | 102kB 3.2k
    84% |███████████████████████████     | 112kB 3.
    92% |█████████████████████████████▌  | 122kB
    99% |████████████████████████████████| 133
    100% |████████████████████████████████| 14
B 5.0kB/s
Requirement already satisfied (use --upgrade to upgrade): idna<2.9,>=2.5 in d:
oftware\python\python35\lib\site-packages (from requests)
Requirement already satisfied (use --upgrade to upgrade): urllib3!=1.25.0,!=1.
.1,<1.26,>=1.21.1 in d:\software\python\python35\lib\site-packages (from reque
s)
Requirement already satisfied (use --upgrade to upgrade): certifi>=2017.4.17 i
d:\software\python\python35\lib\site-packages\certifi-2019.9.11-py3.5.egg (fro
requests)
Installing collected packages: chardet
Successfully installed chardet-3.0.4

G:\迅雷下载\python\requests-2.22.0>
G:\迅雷下载\python\requests-2.22.0>pip3.5 -help

Usage:
  pip <command> [options]

Commands:
  install                     Install packages.
  download                    Download packages.
  uninstall                   Uninstall packages.
  freeze                      Output installed packages in requirements format
  list                        List installed packages.
  show                        Show information about installed packages.
  search                      Search PyPI for packages.
  wheel                       Build wheels from your requirements.
  hash                        Compute hashes of package archives.
  completion                  A helper command used for command completion
  help                        Show help for commands.

General Options:
  -h, --help                  Show help.
  --isolated                  Run pip in an isolated mode, ignoring
                              environment variables and user configuration.
  -v, --verbose               Give more output. Option is additive, and can be
                              used up to 3 times.
  -V, --version               Show version and exit.
  -q, --quiet                 Give less output.
  --log <path>                Path to a verbose appending log.
  --proxy <proxy>             Specify a proxy in the form
                              [user:passwd@]proxy.server:port.
  --retries <retries>         Maximum number of retries each connection should
                              attempt (default 5 times).
  --timeout <sec>             Set the socket timeout (default 15 seconds).
  --exists-action <action>    Default action when a path already exists:
                              (s)witch, (i)gnore, (w)ipe, (b)ackup.
  --trusted-host <hostname>   Mark this host as trusted, even though it does
                              not have valid or any HTTPS.
  --cert <path>               Path to alternate CA bundle.
  --client-cert <path>        Path to SSL client certificate, a single file
                              containing the private key and the certificate
                              in PEM format.
  --cache-dir <dir>           Store the cache data in <dir>.
  --no-cache-dir              Disable the cache.
  --disable-pip-version-check
                              Don't periodically check PyPI to determine
                              whether a new version of pip is available for
                              download. Implied with --no-index.
```
