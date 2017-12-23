#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Adapts HTML generated for upload to be viewable locally"""

__authors__    = ["Erik Vesteraas"]
__copyright__  = "Erik Vesteraas"
__credits__    = ["Erik Vesteraas"]
__version__    = "0.1"
__license__    = "MIT"
# This file is subject to the terms and conditions defined in 'LICENSE.txt'

import glob

def main():
    in_head = """
        <link rel="stylesheet" href="https://www.mn.uio.no/vrtx/decorating/resources/dist/src/css/style.css" type="text/css">
        <link rel="stylesheet" media="only screen and (max-width: 15.5cm) and (orientation : portrait), only screen and (max-width: 17.5cm) and (orientation : landscape)" href="https://www.mn.uio.no/vrtx/decorating/resources/dist/src/css/responsive.css">
        <link rel="stylesheet" media="print" href="https://www.mn.uio.no/vrtx/decorating/resources/dist/src/css/print.css">
        <script type="text/javascript" src="https://www.mn.uio.no/vrtx/decorating/resources/dist/src/lib/jquery.min.js"></script>
    """

    in_body_start = """
        <div id="main">
            <div id="left-main" style="background: #eee;"></div>
            <div id="right-main" class="uio-main">
    """

    in_body_end = """
            </div>
        </div>
    """

    for filename in glob.iglob('./docs/*.html'):
        with open(filename, 'r+') as f:
            html = f.read()
            html = html.replace('<head>', '<head>' + in_head, 1)
            html = html.replace('<body>', '<body>' + in_body_start, 1)
            html = html.replace('<body lang="en">', '<body lang="en">' + in_body_start, 1)
            html = html.replace('</body>', '</body>' + in_body_end, 1)
            f.seek(0)
            f.write(html)

if __name__ == '__main__':
    main()
