# SAPY

The purpose of this softeware is to allow a quick view of your personal budget.
Is designed to allow the creation of various lists of money moves and to compare
 them graphically.

## Installation

### Prerequisites

#### Fedora

In order to run the application

```sudo dnf install python3-matplotlib python3-matplotlib-gtk3```

#### Ubuntu

In order to run the application

```sudo apt install python3-matplotlib```


### Download and Install 

The following commands will 
 * download the application 
 * extract it to ~/.local/Sapy-<version>
 * create laucher in menu
 * create a link in user PATH ( export PREFIX to define)

```
    $ wget https://github.com/stethewwolf/Sapy/archive/v<version>.tar.gz -O sapy-v<version>.tar.gz

    $ tar -xf sapy-<version>.tar.gz -C $HOME/.local/

    $ cd $HOME/.local/Sapy-<version>

    $ install.sh -i
```

## Usage

### Command Line

#### Dsiplay Help
```
$ sapy -h
usage: Sapy [-h] [--add ADD] [--graph] [--gui] [--import IMPORT] [--list LIST]
            [--rm RM] [--version] [--balance] [--daily] [--end-date END_DATE]
            [--id ID] [--monthly] [--lom LOM] [--start-date START_DATE]
            [--value VALUE] [--weekly] [--cause CAUSE] [--date DATE]
            [--name NAME] [--new-year] [--new-month] [--end-week]
            [--end-month]

A spending traking tool

optional arguments:
  -h, --help            show this help message and exit
  --add ADD, -a ADD     add new item, takes : mom | lom | obj | tag
  --graph, -g           print the graph
  --gui                 run the application in grafical mode
  --import IMPORT, -i IMPORT
                        import data from csv file
  --list LIST, -l LIST  list things, target lom | mom | tag | obj
  --rm RM, -r RM        remove target : lom | mom | tag | obj
  --version, -V         print the version
  --balance, -b         print the actual balance of the list
  --daily, -D           set daily occurance
  --end-date END_DATE   set end date
  --id ID               specify id for operation
  --monthly             set monthly occurrance
  --lom LOM             specify the list of money ( lom )
  --start-date START_DATE
                        set start date
  --value VALUE, -v VALUE
                        set value
  --weekly              set weekly occurrance
  --cause CAUSE, -c CAUSE
                        set cause
  --date DATE, -d DATE  set the date for the operation
  --name NAME           set the name
  --new-year            start a new year
  --new-month           start a new month
  --end-week            ends the week, and insert real movement
  --end-month           ends the month

```
#### Display Version

```
[stethewwolf@hel ~]$ sapy -V
Sapy - 1.0.0
	
                        Stefano Prina <stethewwolf@gmail.com>
                         

```
#### List available list of movements
```
$ sapy -l lom
------------------------------
	id	|	name	          
------------------------------
	1	|	real	
	2	|	expected	
------------------------------
```

#### List movements on a list
```
$ sapy -l mom --lom real

------------------------------
real
------------------------------
	id	|	time	|	value	|	cause	
	6	|	2010-06-22	|	-8.89	|	Stuff
------------------------------
 balance : -8.89
------------------------------

```


#### Add a Movement

#### Remove Movement

#### Import From CSV File

### GUI

#### Select A List

#### Add a Movement

#### Remove Movement

#### Import From CSV File

## Notes

### CSV File Format

The CSV file you are importing must have following columns 

  * cause,

  * value,

  * day,

  * month,

  * year

the delimiter for decimal values is the char '.'

the file must not include the header line at the beginning