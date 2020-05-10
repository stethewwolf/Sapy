# SAPY

The purpose of this softeware is to allow a quick view of your personal budget.
Is designed to allow the creation of various lists of money moves and to compare them graphically.

## Releases

* [sapy-v0.1](https://github.com/stethewwolf/Sapy/releases/tag/v0.1)
* [sapy-v0.2](https://github.com/stethewwolf/Sapy/releases/tag/v0.2)

## Installation

### Prerequisites

#### Fedora

In order to run the application

``` sudo dnf install python3-gobject gtk3 ```

Packages neede to build 

``` sudo dnf install cairo-gobject-devel gcc gobject-introspection-devel cairo-devel pkg-config python3-devel gtk3```

#### Build and install 

Download the tar, uncompress it and run the install.sh

```
    wget https://github.com/stethewwolf/Sapy/archive/v<version>.tar.gz

    cd sapy-v<version>

    install.sh -p <path> # build and copy compressed app to path

    # or

    install.sh  # setup the system to use the current files


```
