# Package: poetic (poetic-py)
# Author: Kevin Wang
#
# The MIT License (MIT)
#
# Copyright 2020 Kevin Wang
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
import sys
import os
from pathlib import Path


AUTHOR = "Kevin Wang"

def main():
    
    all_files = find_files()
    
    if len(all_files) > 0:
        
        header = generate_header()
        
        for file in all_files:
            with open(file, "r+") as f:
                
                f.seek(0)
                firstline = f.readline()

                if "# Package: poetic (poetic-py)\n" in firstline:
                    f.close()
                    continue               
                
                f.seek(0)
                contents = f.read()
                contents = header + contents
                f.seek(0)
                f.write(contents)
                f.close()


def generate_header() -> str:
    
    out = "# Package: poetic (poetic-py)\n"
    out += "# Author: {}\n".format(AUTHOR)
    out += "#\n"
    
    out += "# The MIT License (MIT)\n"
    out += "#\n"

    out += "# Copyright 2020 {}\n".format(AUTHOR)
    out += "#\n"

    out += "# Permission is hereby granted, free of charge, to any person obtaining a\n"
    out += '# copy of this software and associated documentation files (the "Software"),\n'
    out += "# to deal in the Software without restriction, including without limitation\n"
    out += "# the rights to use, copy, modify, merge, publish, distribute, sublicense,\n"
    out += "# and/or sell copies of the Software, and to permit persons to whom the\n"
    out += "# Software is furnished to do so, subject to the following conditions:\n"
    out += "#\n"

    out += "# The above copyright notice and this permission notice shall be included\n"
    out += "# in all copies or substantial portions of the Software.\n"
    out += "#\n"

    out += '# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS\n'
    out += "# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n"
    out += "# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n"
    out += "# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n"
    out += "# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING\n"
    out += "# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER\n"
    out += "# DEALINGS IN THE SOFTWARE.\n"
    out += "#\n"
    
    return out


def find_files():
    
    path = sys.argv[1]
    
    if os.path.isdir(path):
        all_files = [str(file) for file in list(Path(path).glob("**/*.py"))]
        return all_files
    
    else: 
        return [path]
    
    
if __name__ == "__main__":
    main()