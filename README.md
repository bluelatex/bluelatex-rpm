RPM Instructions for packaging \Bluelatex
=========================================

Download the matching sources from the official \BlueLatex website and copy them
into your RPM sourcedir.

Copy the build.sbt file into your RPM sourcedir. 

To build a rpm, run this command in a shell:

```shell
$ rpmbuild -bb bluelatex.spec
```
