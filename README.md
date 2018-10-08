# Fuzzy car simulator

A car simulator to simulate the car movements with the fuzzy system.

![preview](https://imgur.com/XxzmuaQ.gif)

## Default setting

The inputs of the fuzzy system are front, 45 degrees left and right distance between the car and the wall. The output is the rotation angle of the steering wheel.

The simulated car is set as a circle which has a radius of 3 unit, and initial direction is +90 degree.

The target is to use the fuzzy system to reach the end area without encountering any wall. If the car arrives safely, then display and output the result.

The motion equation of the simulated car is as follows:

![motion equation](https://imgur.com/BITX9xi.jpg)

## Fuzzy system design

The fuzzy system uses the custom nine fuzzy rules and discrete center of gravity defuzzifier.

The fuzzy rule base uses the Mamdani fuzzy rule, and to avoid too complex the "antecedent or premise" only take two fuzzy variables (front distance and left-right distance). The "consequence or conclusion" set one fuzzy variable, steering wheel angle.

See [here](https://docs.google.com/document/d/164zeJNkSDSpMjxyjhQvf0cv7rn15wAfv5xkW5vL7h1g/edit?usp=sharing) for more details about experiments and analysis.
## Installation

1. download the project

```git bash
    git clone https://github.com/daniel4lee/fuzzy-system.git
```

2. Change directory to the root of the project and run with Python interpreter.

```git bash
    python main.py
```

## Test Customized Map

### Map File location and format

The map should be `*.txt` format and put in `/data` location.

### Example Format

![example map](https://i.imgur.com/oHiqTMr.jpg)

``` python
0,0,90  # x, y, degree(the initial position coordinate and direction angle of the car
18,40   # x, y (the top-left coordinate of the ending area)
30,37   # x, y (the bottom-right coordinate of the ending area)
-6,0   # the first point of the wall in map
-6,22
18,22
18,50
30,50
30,10
6,10
6,0
-6,0   # the last point of the wall in map
```

The coordinates after the third line are the corner points of the walls in the map.

## Output movement data

### `train4D.txt`

``` python
# Front_Distance Right_Distance Left_Distance Wheel_Angle

22.0000000 8.4852814 8.4852814 -16.0709664
21.1292288 9.3920089 7.7989045 -14.7971418
20.3973643 24.4555821 7.2000902 16.2304876
19.1995799 25.0357595 7.5129743 16.0825385
18.1744869 42.5622911 8.0705896 15.5075777
```

### `train6D.txt`

``` python
# X Y Front_Distance Right_Distance Left_Distance Wheel_Angle

0.0000000 0.0000000 22.0000000 8.4852814 8.4852814 -16.0709664
0.0000000 0.9609196 21.1292288 9.3920089 7.7989045 -14.7971418
-0.0892157 1.9236307 20.3973643 24.4555821 7.2000902 16.2304876
-0.2588831 2.8686659 19.1995799 25.0357595 7.5129743 16.0825385
-0.3398267 3.8261141 18.1744869 42.5622911 8.0705896 15.5075777
-0.3319909 4.7896773 17.2922349 8.1967401 8.9258102 -14.6592172
```

## Dependencies

- [numpy](http://www.numpy.org/)

- [PyQt5](https://pypi.org/project/PyQt5/)
- [Shapely](https://pypi.org/project/Shapely/)
- [descartes](https://pypi.org/project/descartes/)
- [matplotlib](https://matplotlib.org/)