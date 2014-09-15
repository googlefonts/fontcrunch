# coding: utf-8
# Copyright 2013 The Font Bakery Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# See AUTHORS.txt for the list of Authors and LICENSE.txt for the License.

from setuptools import setup, Extension

module1 = Extension('_quadopt',
                    sources=['quadopt_wrap.cxx', 'quadopt.cc'],
                    extra_compile_args=['-std=c++0x', '-O3'])

setup(
    name="FontCrunch",
    version='0.1',
    url='https://github.com/googlefonts/fontcrunch/',
    description='fontcrunch',
    author='Raph Levien',
    packages=["fontcrunch"],
    scripts=['tools/font-crunch.py'],
    zip_safe=False,
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    ext_modules=[module1],
    py_modules=['quadopt', ]
)
