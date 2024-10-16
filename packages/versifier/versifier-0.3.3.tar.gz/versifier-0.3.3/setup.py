# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['versifier']

package_data = \
{'': ['*']}

install_requires = \
['astunparse>=1.6.3,<2.0.0',
 'click==8.0.3',
 'cython>=3.0.11,<4.0.0',
 'pip-requirements-parser>=32.0.1,<33.0.0',
 'toml>=0.10.2,<0.11.0']

extras_require = \
{':python_version < "3.7"': ['dataclasses==0.8']}

entry_points = \
{'console_scripts': ['versifier = versifier.__main__:cli']}

setup_kwargs = {
    'name': 'versifier',
    'version': '0.3.3',
    'description': 'Versifier: A lyrical tool to transform Python requirements into Poetry configurations, effortlessly and elegantly.',
    'long_description': '# versifier\n\n[![Release](https://img.shields.io/github/v/release/mrlyc/versifier)](https://img.shields.io/github/v/release/mrlyc/versifier)\n[![Build status](https://img.shields.io/github/actions/workflow/status/mrlyc/versifier/main.yml?branch=main)](https://github.com/mrlyc/versifier/actions/workflows/main.yml?query=branch%3Amain)\n[![codecov](https://codecov.io/gh/mrlyc/versifier/branch/main/graph/badge.svg)](https://codecov.io/gh/mrlyc/versifier)\n[![Commit activity](https://img.shields.io/github/commit-activity/m/mrlyc/versifier)](https://img.shields.io/github/commit-activity/m/mrlyc/versifier)\n[![License](https://img.shields.io/github/license/mrlyc/versifier)](https://img.shields.io/github/license/mrlyc/versifier)\n\n## Overview\n\n这个项目提供了一套命令行工具集，主要用于处理 Python 项目的依赖管理。主要功能包括：\n- 将 requirements.txt 转化为 Poetry 的 pyproject.toml\n- 将 Poetry 的 pyproject.toml 导出为 requirements.txt\n- 将私有包提取到指定目录\n\n## Installation\n\n使用 pip 来安装这个项目：\n\n```shell\npip install versifier\n```\n\n## Commands\n### requirements-to-poetry\n\n将 requirements 转换为 poetry。\n\n```bash\nversifier requirements-to-poetry --requirements <requirements_files> --dev-requirements <dev_requirements_files> --exclude <exclude_packages> --add-only --config <config_file> --root <root_dir> --poetry-path <path_to_poetry> --nuitka-path <path_to_nuitka3> --log-level <log_level>\n```\n\n参数说明：\n- `-R, --requirements`: 指定 requirements 文件。默认为当前目录的 requirements.txt。\n- `-d, --dev-requirements`: 指定开发环境的 requirements 文件。默认为当前目录的 dev-requirements.txt。\n- `-e, --exclude`: 指定要排除的包。\n- `--add-only`: 只添加指定的包，而不删除任何现有的包。\n- `-c, --config`: 指定配置文件。\n- `-r, --root`: 指定根目录。默认为当前目录。\n- `--poetry-path`: 指定 poetry 的路径。默认为 "poetry"。\n- `--nuitka-path`: 指定 nuitka3 的路径。默认为 "nuitka3"。\n- `--log-level`: 指定日志级别。\n\n### poetry-to-requirements\n\n将 poetry 转换为 requirements。\n\n```bash\nversifier poetry-to-requirements --output <output_file> --exclude-specifiers --include-comments --include-dev-requirements --extra-requirements <extra_requirements> --markers <markers> --private-packages <private_packages> --config <config_file> --root <root_dir> --poetry-path <path_to_poetry> --nuitka-path <path_to_nuitka3> --log-level <log_level>\n```\n\n参数说明：\n- `-o, --output`: 指定输出文件。\n- `--exclude-specifiers`: 排除指定的包。\n- `--include-comments`: 包含注释。\n- `-d, --include-dev-requirements`: 包含开发环境的 requirements。\n- `-E, --extra-requirements`: 指定额外的 requirements。\n- `-m, --markers`: 指定标记。\n- `-P, --private-packages`: 指定私有包。\n- `-c, --config`: 指定配置文件。\n- `-r, --root`: 指定根目录。默认为当前目录。\n- `--poetry-path`: 指定 poetry 的路径。默认为 "poetry"。\n- `--nuitka-path`: 指定 nuitka3 的路径。默认为 "nuitka3"。\n- `--log-level`: 指定日志级别。\n\n### extract-private-packages\n\n提取私有包。\n\n```bash\nversifier extract-private-packages --output <output_dir> --extra-requirements <extra_requirements> --exclude-file-patterns <exclude_files> --private-packages <private_packages> --config <config_file> --root <root_dir> --poetry-path <path_to_poetry> --nuitka-path <path_to_nuitka3> --log-level <log_level>\n```\n\n参数说明：\n- `-o, --output`: 指定输出目录。默认为当前目录。\n- `-E, --extra-requirements`: 指定额外的 requirements。\n- `--exclude-file-patterns`: 指定要排除的文件模式。\n- `-P, --private-packages`: 指定要提取的私有包列表。\n- `-c, --config`: 指定配置文件。\n- `-r, --root`: 指定根目录。默认为当前目录。\n- `--poetry-path`: 指定 poetry 的路径。默认为 "poetry"。\n- `--nuitka-path`: 指定 nuitka3 的路径。默认为 "nuitka3"。\n- `--log-level`: 指定日志级别。\n\n### obfuscate-project-dirs\n\n混淆项目目录。\n\n```bash\nversifier obfuscate-project-dirs --output <output_dir> --sub-dirs <included_sub_dirs> --exclude-packages <exclude_packages> --config <config_file> --root <root_dir> --poetry-path <path_to_poetry> --nuitka-path <path_to_nuitka3> --log-level <log_level>\n```\n\n参数说明：\n- `-o, --output`: 指定输出目录。默认为当前目录。\n- `-d, --sub-dirs`: 指定要包含的子目录。\n- `--exclude-packages`: 指定要排除的包。\n- `-c, --config`: 指定配置文件。\n- `-r, --root`: 指定根目录。默认为当前目录。\n- `--poetry-path`: 指定 poetry 的路径。默认为 "poetry"。\n- `--nuitka-path`: 指定 nuitka3 的路径。默认为 "nuitka3"。\n- `--log-level`: 指定日志级别。\n\n### obfuscate-private-packages\n\n混淆私有包。\n\n```bash\nversifier obfuscate-private-packages --output <output_dir> --extra-requirements <extra_requirements> --private-packages <private_packages> --config <config_file> --root <root_dir> --poetry-path <path_to_poetry> --nuitka-path <path_to_nuitka3> --log-level <log_level>\n```\n\n参数说明：\n- `-o, --output`: 指定输出目录。默认为当前目录。\n- `-E, --extra-requirements`: 指定额外的 requirements。\n- `-P, --private-packages`: 指定要混淆的私有包列表。\n- `-c, --config`: 指定配置文件。\n- `-r, --root`: 指定根目录。默认为当前目录。\n- `--poetry-path`: 指定 poetry 的路径。默认为 "poetry"。\n- `--nuitka-path`: 指定 nuitka3 的路径。默认为 "nuitka3"。\n- `--log-level`: 指定日志级别。\n\n\n## License\n\n此项目使用 MIT 许可证。有关详细信息，请参阅 LICENSE 文件。\n\n## Contributing\n\n我们欢迎各种形式的贡献，包括报告问题、提出新功能、改进文档或提交代码更改。如果你想要贡献，请查看 CONTRIBUTING.md 获取更多信息。',
    'author': 'MrLYC',
    'author_email': 'fx@m.mrlyc.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrlyc/versifier',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0',
}


setup(**setup_kwargs)
