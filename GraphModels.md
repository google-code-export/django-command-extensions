Creates a **[GraphViz](http://www.graphviz.org/)** dot file for the specified app names.  You can pass multiple app names and they will all be combined into a single model.  Output is usually directed to a dot file.

With the latest revisions it's also possible to specify an output file if **[pygraphviz](https://networkx.lanl.gov/wiki/pygraphviz)** is installed and render directly to an image or other supported filetype.

## Example Usage ##

With **django-command-extensions** installed you can create a dot-file or an image by using the _graph\_models_ command. Like used in the following examples:

```
# Create a dot file
$ ./manage.py graph_models -a > my_project.dot
```
```
# Create a PNG image file called my_project_visualized.png with application grouping
$ ./manage.py graph_models -a -g -o my_project_visualized.png
```
```
# Create a dot file for only the 'foo' and 'bar' applications of your project
$ ./manage.py graph_models foo bar > my_project.dot
```

## Example Rendered Graphics ##

The following graphs are from the [PyCon-Tech](https://pycon.coderanger.net/) project.  PyCon-Tech is a conference management framework based on Django framework.

### Pycon-Tech Project ###
![![](http://ido.nl.eu.org/static/images/pycon_no_grouping_small.png)](http://ido.nl.eu.org/static/images/pycon_no_grouping.png)

[Big-Image](http://ido.nl.eu.org/static/images/pycon_no_grouping.png)

### Pycon-Tech Project Overview With Grouping ###
![![](http://ido.nl.eu.org/static/images/pycon_grouping_small.png)](http://ido.nl.eu.org/static/images/pycon_grouping.png)

[Big-Image](http://ido.nl.eu.org/static/images/pycon_grouping.png)