# PyPnPObjects

## Table of content

* [Introduction](#introduction)
* [Version Information](#version-information)
* [Installation](#installation)
    * [Install with pip](#install-with-pip)
    * [Install with git](#install-with-git)
* [Uninstallation](#uninstallation)
    * [Unsinstall using pip](#uninstall-using-pip)
* [Clearing](#clearing)
* [Platform Supports](#platform-supports)
* [Dependencies](#dependencies)
* [Usage](#usage)
    * [CLI](#cli)
    * [Python script](#python-script)
* [API References](#api-references)
    * [WMIStorePNPObjects(object)](#wmistorepnpobjects(object))
        * [Constructor](#constructor)
        * [Representation](#representation)
        * [def load(self, ...)](#def-load(self,-...)-->-`type`)
        * [def query(self, ...)](#def-query(self,-...)-->-`WMIInternalPNPObjectProperties`)
        * [def free(self)](#def-free(self)-->-`NoneType`)
    * [WMIStorePNPObjectsException(Exception)](#wmistorepnpobjectsexception(exception))
    * [WMIInternalPNPObjectProperties(object)](#wmiinternalpnpobjectproperties(object))
* [Development Areas](#development-areas)
* [License](#license)
* [Contribution](#contribution)

----

## Introduction ##

This is a simple python module to get the detail level information about Win32 [WMI](https://docs.microsoft.com/en-us/windows/win32/wmisdk/wmi-start-page) objects. To know more about [Win32 PnpEntity](https://docs.microsoft.com/en-us/windows/win32/cimwin32prov/win32-pnpentity), click on it.

## Version Information ##

Current version of this module is in BETA version ***0.1.9***.

----

## Installation ##

Installing pypnpobjects is as easy as installing any other python module.

### Install with pip ###

```bash
pip install pypnpobjects
```

### Install with git ###

```bash
git clone https://github.com/antaripchatterjee/PyPnPObjects.git
cd PyPnPObjects
python setup.py install
```

----

## Uninstallation ##

You can uninstall this module whenever you want, using below method.

### Uninstall using pip ###

```bash
pip uninstall pypnpobjects
```
----

## Clearing ##

You can clear the folders and files created, during last installation using below command.

```bash
python clear.py
```

----

## Platform Supports ##

PyPnPObjects is available only for win32 systems. I tested this module with python version 2.7.18 and python 3.5.4+, successfully.

> *P.S.: When I tested this module with python 2, I could not use argument `timeout` of `WMIStorePNPObjects.load` method, and in windows 7, some properties of pnp entity was missing (e.g. `PNPClass`).

----

## Dependencies ##

There are no such external dependencies, except it uses windows **powershell**.

----

## Usage ##

You can either use this module as a CLI application or you can also use it in your python script.

### CLI ###

You can run a simple command as below to test it's functionality.

```bash
get-pnpobjects -select name -select pnpclass -where pnpclass:audio% -ignore_case -operator like
```

When I executed the above command it gave the below output, it might be different in your system.

```output
Name                    :Microphone (Realtek(R) Audio)
PNPClass                        :AudioEndpoint

Name                    :Speakers (Realtek(R) Audio)
PNPClass                        :AudioEndpoint

Name                    :Stereo Mix (Realtek(R) Audio)
PNPClass                        :AudioEndpoint
```

To get the version, you can use below command.

```bash
get-pnpobjects -version
```

You can also get the metadata about the project by using below command.

```bash
get-pnpobjects -meta <Meta-Property>
```

To know about the available meta properties, use `-show-meta-props`.

```bash
get-pnpobjects -show-meta-props
```

You can use `-h` to know more.

```bash
get-pnpobjects -h
```

### Python script ###

Just do copy and paste to test this code.

```python
from pypnpobjects import WMIStorePNPObjects

if __name__ == "__main__":
    with WMIStorePNPObjects() as wmipnp:
        proc_res = wmipnp.load()
        if proc_res[0] == 0:
            for dev in wmipnp.query('*', pnpclass='cameR_', case_sensitive_comparision = False, comparision_operator = 'like'):
                print('Device %s is %s'%(dev.Name))
        else:
            print('Error with code %d : %s'%(proc_res))
```

For me the output was as below, since I am only having integrated camera in my computer.

```output
Device Name is USB2.0 VGA UVC WebCam

```

----

## API References ##

The primary class of this module is ***`WMIStorePNPObjects`***, however it also includes some other classes for internal purpose which are ***`WMIStorePNPObjectsException`*** and ***`WMIInternalPNPObjectProperties`***.

### WMIStorePNPObjects(object) ###

This class contains some public methods and they are *`load`*, *`query`* and *`free`*. This class is also having some implementations of `__enter__` and `__exit__` magic methods which means it supports ***context manager*** functionality as well, so that you do not need to explicitly free and close the context.

#### Constructor ####

The ***`__init__`*** method takes a single positional argument which expects a value of *`list`* or *`str`* type object.

> *(optional) `str` | `list` | `tuple` **command:*** The default value of this argument is **`["Get-WmiObject", "Win32_PnPEntity"]`** but you can  also change the value according to your need. The argument value should be a valid **powershell** command too. 

If you run the below **powershell** command you will get an overall idea about the available properties for different kind of PnP entities.

```powershell
Get-WmiObject Win32_PnpEntity
```

#### Representation ####

This class also implements the `__repr__` magic method which also let us see the **powershell** command, that will be executed after calling the `load` method. You can refer the below code.

```python
from pypnpobjects import WMIStorePNPObjects

if __name__ == "__main__":
    with WMIStorePNPObjects() as wmipnp:
        print(wmipnp)
        ...
        ...
```

The above code will generate a output like below.

```output
WMIStorePNPObjects object at 0x216ffb969b0 <powershell Get-WmiObject Win32_PnPEntity>
...
...
```

#### def load(self, ...) -> `tuple` ####

A very important method from this class is ***`load`***, which does a number of sequential tasks like, it first executes the command if the command is valid, then parses the command result and creates a python *`dict`* and finally stores the result into a **SQLite** database instance. It also takes a number of positional arguments and below you will find some useful information about them.

> *(optional) `str` **db:*** The value for this argument should be either `':memory:'` or `':file:'`. The default value is `':memory:'` and the ***SQLite*** database will be created in memory but not as a physical file and hence this option is making the database volatile. If you choose it as `':file:'`, then a physical **SQLite** file, called `win32_pnpentity.sqlite.db`, will be created in the same working directory and you can also reuse it later in your application. Any value other than `':memory:'` or `':file:'` will be changed to `':memory:'`.

> *(optional) `str` **table:*** The value of this argument refers the table name of the **SQLite** database where all the information about the PnP entities will be stored. The default value is `Win32_PnPEntity`.

> *(optional) `int` **expected_exit_code:*** The default value for this argument is `0` and the **`load`** method returns immediately if the exit code of the command or process is not same as `expected_exit_code`.

> *(optional) `int` **timeout:*** The value of this argument is time in second to find and execute the command or process. The default value is `30`. To study more about this option refer this [link](https://docs.python.org/3/library/subprocess.html#subprocess.Popen.wait) from [subprocess](https://docs.python.org/3/library/subprocess.html) module. If the time limit exceeds, the `load` method will return immediately with return code as `None` and with a error message. This argument is only available for python 3.

This method returns an object of `tuple` of length 2. The *0th* element, which is a `int` type object, is the exit code of the command or process and the *1st* element, which is a `str` type object, holds the error message if any error occurred during the execution.

#### def query(self, ...) -> `types.GeneratorType` ####

Another important public method is `query` which basically queries the required information based on your input to the function from the same **SQLite** database connection. It also takes number arguments as input.

> *(optional) `str` | `int` **\*select:*** This is a *variable length non-keyword argument*. Each value in this argument either should be a valid property name or a valid property index otherwise it will throw a `WMIStorePNPObjectsException`. If you keep it empty while calling the method, the `query` method itself will fetch all the properties for an entity from the same **SQLite** database instance.

> *(optional) `str` | `int` | `float` | `bool` **\*\*where:*** This argument is a *variable length keyword argument*, which takes any valid property id of an entity as a keyword and the value of the keyword is used as a where condition during the query execution. The value can also be a SQL pattern and this can be matched with *SQL* operator `LIKE`.

> *(optional) `str` **comparision_operator:*** This argument should be either `'like'` or `'equal'` and the default value is `'equal'` which means the `query` method will do a equality check while querying the entities but if we specify `'like'`, the method will use *SQL* operator `LIKE` to match the pattern instead. Any value other than `'like'` or `'equal'` will be changed to `'equal'`.

> *(optional) `bool` | `int` | `str` **case_sensitive_comparision:*** This argument should receive a python `bool` object i.e. either it should be `True` or `False` but if we specify any non-zero values, it would be considered as `True` otherwise `False`. Also we can pass `str` representation of `True` or `False`. The default value is `True` which means, the conditions will be checked as case sensitively otherwise it will be checked as case insensitively.

This method returns a generator object and each element of it is a object of `WMIInternalPNPObjectProperties`, which holds the data about the properties of a PnP entity, and you can see them either by using *key-value* mechanism \(e.g dev\['Name'\]\) or by using `.` operator \(e.g. dev.Name\) and this keys are case insenitive which means `dev.name == dev.Name` will give you `True` result and every property returns a tuple of actual property id and it's value i.e. `dev.name` will return `('Name', '<Property Value>')`.

#### def free(self) -> `NoneType` ####

This method closes the connection of the same **SQLite** database instance and does not return any value, however if you use `with` context manager, you do not need to explicitly call this method.

### WMIStorePNPObjectsException(Exception) ###

This class is a exception type and it is used internally to raise different concerns during the execution.

### WMIInternalPNPObjectProperties(object) ###

Every element of the generator object, returned by `WMIStorePNPObjects.query` method, is a object of `WMIInternalPNPObjectProperties` class. This class is having some ground level implementations of `__contains__`, `__getattr__`,  `__getitem__`, `__iter__` and `__len__` magic methods, in order to provide some `dict` like functionalities however this class is inherited from `object` class only.

----

## Development Areas ##

I was working in a project which had some requirements and I could not figure out the solutions for them, so I have made this python module, however I have more plans to implement in it and will update them on a regular basis. Below are some points, which I am planning to implement.

* I will make a similar python module for `*NIX` based system to make it cross-platform.
* I will also make this module compatible for any `WINDOWS` system which does not have **powershell**.

----

## License ##

With the power of opensource project, this module is licensed with [MIT License](https://github.com/antaripchatterjee/pypnpobjects/LICENSE) which let you feel free to do any thing that comes under [MIT License](https://opensource.org/licenses/MIT).

----

## Contribution ##

Pull requests are always awesome and you are free to contribute anytime, but please make sure to raise a ticket before doing any changes.

----
