# G2 Review Analyzer

## API used

* Reviews List : [API Doc Link](https://data.g2.com/api/docs#reviews-list)

## Overview

This is the source code for the client review analysis & summarisation pipeline used by G2.com
Unbiased customer reviews are gathered from the above mentioned API endpoints and a database is built that contains organised information about different opinions and perspectives on our products. This is used by a query / search mechanism to help those looking to try our solutions to navigate reviews and get a picture of what we do and simplified view of various review metrics like votes & ratings.

## Implementation
The pipeline for processing reviews is built with python using NLP modules spacY , nltk & yake.
Additional modules used: pandas, textblob, gensim
Checkout requirements.txt for more info!

The frontend is a single page application built with React JS.
We have used chart JS to plot the metrics and make UI aesthetics.
The found in /frontend can be run as development server using 
```
npm start
```

## How are reviews aggregated?

* Country-wise star-rating
* Finding mean of metrics given in secondary comments
* Finding keywords for the different love and hate comments given in reviews and indexing them to query through suggest relevant reviews to user by finding similarity between query and these tags.
* Statistics corresponding to votes given in reviews
* Getting polarity scores corresponding to the common aspects which users look for, like value-for-money, ease-of-use, performance, scalability and using this to fetch suitable reviews and display


## Links

Some useful links that might help you:

- [API Doc Link](https://data.g2.com/api/docs#reviews-list)


## Source Code sitemap
```
ABOUT-NLS          - Notes on the Free Translation Project.
AUTHORS            - VLC authors.
COPYING            - The GPL license.
COPYING.LIB        - The LGPL license.
INSTALL            - Installation and building instructions.
NEWS               - Important modifications between the releases.
README             - Project summary.
THANKS             - VLC contributors.

bin/               - VLC binaries.
bindings/          - libVLC bindings to other languages.
compat/            - compatibility library for operating systems missing
                     essential functionalities.
contrib/           - Facilities for retrieving external libraries and building
                     them for systems that don't have the right versions.
doc/               - Miscellaneous documentation.
extras/analyser    - Code analyser and editor specific files.
extras/buildsystem - Different build system specific files.
extras/misc        - Files that don't fit in the other extras/ categories.
extras/package     - VLC packaging specific files such as spec files.
extras/tools/      - Facilities for retrieving external building tools needed
                     for systems that don't have the right versions.
include/           - Header files.
lib/               - libVLC source code.
modules/           - VLC plugins and modules. Most of the code is here.
po/                - VLC translations.
share/             - Common resource files.
src/               - libvlccore source code.
test/              - Testing system.
```
