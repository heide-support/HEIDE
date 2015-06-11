#    Copyright (C) 2015  Grant Frame
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

# distutils: language = c++
# distutils: sources = ../BGV_HE/BGV_HE.cpp

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os

os.environ["CC"] = "x86_64-linux-gnu-g++"
os.environ["CXX"] = "x86_64-linux-gnu-g++"

HELIB_BASE = os.environ["HELIB_BASE"]
SRC_BASE = "./src/"

ext_modules = [
    Extension(
        name="PyHE",
        sources=[SRC_BASE + "PyHE.pyx",
                "../BGV_HE/BGV_HE.cpp",
                HELIB_BASE + "/BenesNetwork.cpp",
                HELIB_BASE + "/bluestein.cpp",
                HELIB_BASE + "/CModulus.cpp",
                HELIB_BASE + "/Ctxt.cpp",
                HELIB_BASE + "/debugging.cpp",
                HELIB_BASE + "/DoubleCRT.cpp",
                HELIB_BASE + "/EncryptedArray.cpp",
                HELIB_BASE + "/eqtesting.cpp",
                HELIB_BASE + "/EvalMap.cpp",
                HELIB_BASE + "/extractDigits.cpp",
                HELIB_BASE + "/FHEContext.cpp",
                HELIB_BASE + "/FHE.cpp",
                HELIB_BASE + "/hypercube.cpp",
                HELIB_BASE + "/IndexSet.cpp",
                HELIB_BASE + "/KeySwitching.cpp",
                HELIB_BASE + "/matching.cpp",
                HELIB_BASE + "/NumbTh.cpp",
                HELIB_BASE + "/OldEvalMap.cpp",
                HELIB_BASE + "/OptimizePermutations.cpp",
                HELIB_BASE + "/PAlgebra.cpp",
                HELIB_BASE + "/PermNetwork.cpp",
                HELIB_BASE + "/permutations.cpp",
                HELIB_BASE + "/polyEval.cpp",
                HELIB_BASE + "/powerful.cpp",
                HELIB_BASE + "/recryption.cpp",
                HELIB_BASE + "/replicate.cpp",
                HELIB_BASE + "/timing.cpp",
            ],
        include_dirs=[HELIB_BASE],
        libraries=[ "gmp",
                    "ntl"],
        library_dirs=[],
        language="c++",
        extra_compile_args=["-DNDEBUG",
                            "-g",
                            "-fwrapv",
                            "-O2",
                            "-Wall"],
    ),
    Extension(
        name="PyPtxt",
        sources=[SRC_BASE + "PyPtxt.py"],
        include_dirs=[],
        libraries=[],
        library_dirs=[],
        language="python",
    ),
    Extension(
        name="PyCtxt",
        sources=[SRC_BASE + "PyCtxt.py"],
        include_dirs=[],
        libraries=[],
        library_dirs=[],
        language="python",
    )
]

setup(
    name = 'PyHE',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules,
)
