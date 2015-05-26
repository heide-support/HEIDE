# distutils: language = c++
# distutils: sources = ../HElib_Ext/HElib_Ext.cpp

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import os

os.environ["CC"] = "x86_64-linux-gnu-g++"
os.environ["CXX"] = "x86_64-linux-gnu-g++"

HELIB_BASE = "../HElib/src"

ext_modules = [
    Extension(
        name="PyHE",
        sources=["PyHE.pyx",
                "../HElib_Ext/HElib_Ext.cpp",
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
        include_dirs=[],
        libraries=[	"gmp",
                    "ntl"],
        library_dirs=[],
        language="c++",
        extra_compile_args=["-DNDEBUG",
                            "-g",
                            "-fwrapv",
                            "-O2",
                            "-Wall"],
        )
]

setup(
name = 'PyHE',
cmdclass = {'build_ext': build_ext},
ext_modules = ext_modules,
)
