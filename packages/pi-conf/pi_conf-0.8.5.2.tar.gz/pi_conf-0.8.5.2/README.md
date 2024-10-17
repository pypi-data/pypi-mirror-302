# P-Conf

Easy use Configs for python projects. Allows loading the config files in the application directory (os specific). Once set the config can be used as a singleton across the project or pass around.

## Locations for the config file
The following are the default locations that will be searched
*  ```~/.config/<appname>/config.(toml|json|ini|yaml)```
* ```<system config directory>/<appname>/config.(toml|json|ini|yaml)```

## Example code

The example code uses the following as the example configuration file
```toml
# My config.toml file
foo = 1
[bar]
a = 2
```

### Using inside of a single script
```python
from pi_conf import load_config
cfg = load_config("ourappname")

print(cfg.foo) # 1
print(cfg.bar.a) # 2
```


### Using inside of applications
The following is the preferred way of using the pi-conf module. 

```python
# __init__.py

from pi_conf import load_config
cfg = load_config("ourappname") ## Loads the config from the application <appname> directory

```

### Using the config in files
Once it the config has been set you can use it from any file doing either of the following methods.
* Option 1
```python
from ourappname import cfg ## Import cfg from what we set in __init__.py

print(cfg.foo) # 1
```

* Option 2
```python
from pi_conf import load_config ## Just load it again
cfg = load_config("ourappname")

print(cfg.foo) # 1
```
