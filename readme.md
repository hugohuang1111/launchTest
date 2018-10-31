# Launch Android App Test

This is a python script that automatically tests android App launch.


## Useage

`launchTest.py`

```python
params = {
    'packageID': 'com.dingogames.tastyplanet4',
    'activity': 'org.cocos2dx.cpp.AppActivity',
    'times': 3,
    'spaceSecond': 10
}
```

this will launch android App `com.dingogames.tastyplantet4` 3 times. rest 10 second between every launch.


## dependency

1. Android ADB
2. [pidcat](https://github.com/JakeWharton/pidcat)
3. Python 2.7
