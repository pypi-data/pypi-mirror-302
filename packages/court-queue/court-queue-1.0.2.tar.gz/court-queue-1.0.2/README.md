# court-queue


[![PyPI version](https://badge.fury.io/py/court-queue.svg)](https://badge.fury.io/py/court-queue)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)


This library provides tools to visualize and work with a novel data structure known as the 'court queue.' The court queue combines the concepts of 2D arrays and right/left queues to create a multi-level queue system with specific rules for adding, removing, and moving elements between levels. It’s designed to offer a structured and efficient approach to managing hierarchical data or tasks.


Whether you're a beginner or a professional, this library is tailored to suit various levels of expertise, providing both straightforward and advanced features for working with the court queue data structure.


## Installation


You can install `court-queue` via pip:


```bash
pip install court-queue
```


## Usage 


### You can create the queue from a predefined, static 2D array (matrix)


```python
from court_queue import courtQueue


static_matrix = [[1, 2, 3], [6, 5, 4], [7, 8, 9]]
x = courtQueue(static_matrix)
print(x)
```


### Output


```bash
[[1, 2, 3], [6, 5, 4], [7, 8, 9]]
```


### You can show all details


```python
from court_queue import courtQueue


static_matrix = [[1, 2, 3], [6, 5, 4], [7, 8, 9]]
x = courtQueue(static_matrix, detail=True)
print(x)
```


### Output


```bash
╒══════════╤═══╤═══╤═══╤══════════╕
│ <- EXIT  │ 1 │ 2 │ 3 │ <- ENTER │
├──────────┼───┼───┼───┼──────────┤
│ ENTER -> │ 6 │ 5 │ 4 │ EXIT ^   │
├──────────┼───┼───┼───┼──────────┤
│ ^ EXIT   │ 7 │ 8 │ 9 │ <- ENTER │
╘══════════╧═══╧═══╧═══╧══════════╛
```


### You can dequeue values


```python
from court_queue import courtQueue


static_matrix = [[1, 2, 3], [6, 5, 4], [7, 8, 9]]
x = courtQueue(static_matrix, detail=True)
print(x)
x.dequeue()
print(x)
```


### Output


```bash
╒══════════╤═══╤═══╤═══╤══════════╕
│ <- EXIT  │ 1 │ 2 │ 3 │ <- ENTER │
├──────────┼───┼───┼───┼──────────┤
│ ENTER -> │ 6 │ 5 │ 4 │ EXIT ^   │
├──────────┼───┼───┼───┼──────────┤
│ ^ EXIT   │ 7 │ 8 │ 9 │ <- ENTER │
╘══════════╧═══╧═══╧═══╧══════════╛
╒══════════╤═══╤═══╤═══╤══════════╕
│ <- EXIT  │ 2 │ 3 │ 4 │ <- ENTER │
├──────────┼───┼───┼───┼──────────┤
│ ENTER -> │ 7 │ 6 │ 5 │ EXIT ^   │
├──────────┼───┼───┼───┼──────────┤
│ ^ EXIT   │ 8 │ 9 │   │ <- ENTER │
╘══════════╧═══╧═══╧═══╧══════════╛
```


### You can enqueue values


```python
from court_queue import courtQueue


static_matrix = [[1, 2, 3], [6, 5, 4], [7, 8, None]]
x = courtQueue(static_matrix, detail=True)
print(x)
x.enqueue(9)
print(x)
```


### Output


```bash
╒══════════╤═══╤═══╤═══╤══════════╕
│ <- EXIT  │ 1 │ 2 │ 3 │ <- ENTER │
├──────────┼───┼───┼───┼──────────┤
│ ENTER -> │ 6 │ 5 │ 4 │ EXIT ^   │
├──────────┼───┼───┼───┼──────────┤
│ ^ EXIT   │ 7 │ 8 │   │ <- ENTER │
╘══════════╧═══╧═══╧═══╧══════════╛
╒══════════╤═══╤═══╤═══╤══════════╕
│ <- EXIT  │ 1 │ 2 │ 3 │ <- ENTER │
├──────────┼───┼───┼───┼──────────┤
│ ENTER -> │ 6 │ 5 │ 4 │ EXIT ^   │
├──────────┼───┼───┼───┼──────────┤
│ ^ EXIT   │ 7 │ 8 │ 9 │ <- ENTER │
╘══════════╧═══╧═══╧═══╧══════════╛
```


### You can create the queue from scratch


```python
from court_queue import courtQueue


x = courtQueue(rows=3, columns=3, detail=True)
print(x)
for i in range(9):
    x.enqueue(i + 1)
print(x)
```


### Output


```bash
╒══════════╤══╤══╤══╤══════════╕
│ <- EXIT  │  │  │  │ <- ENTER │
├──────────┼──┼──┼──┼──────────┤
│ ENTER -> │  │  │  │ EXIT ^   │
├──────────┼──┼──┼──┼──────────┤
│ ^ EXIT   │  │  │  │ <- ENTER │
╘══════════╧══╧══╧══╧══════════╛
╒══════════╤═══╤═══╤═══╤══════════╕
│ <- EXIT  │ 1 │ 2 │ 3 │ <- ENTER │
├──────────┼───┼───┼───┼──────────┤
│ ENTER -> │ 6 │ 5 │ 4 │ EXIT ^   │
├──────────┼───┼───┼───┼──────────┤
│ ^ EXIT   │ 7 │ 8 │ 9 │ <- ENTER │
╘══════════╧═══╧═══╧═══╧══════════╛
```


### You can show how many values are in the queue


```python
from court_queue import courtQueue


static_matrix = [[1, 2, 3], [6, 5, 4], [7, 8, 9]]
x = courtQueue(static_matrix, detail=True)
print(len(x))
```


### Output


```bash
9
```


### You can check whether the queue is empty


```python
from court_queue import courtQueue


static_matrix = [[None, None, None], [None, None, None], [None, None, None]]
x = courtQueue(static_matrix, detail=True)
print(x.isEmpty())
x.enqueue(1)
print(x.isEmpty())
```


### Output


```bash
True
False
```


### You can check whether the queue is full


```python
from court_queue import courtQueue


static_matrix = [[1, 2, 3], [6, 5, 4], [7, 8, 9]]
x = courtQueue(static_matrix, detail=True)
print(x.isFull())
x.dequeue()
print(x.isFull())
```


### Output


```bash
True
False
```


### You can check the next value to be dequeued using peek or top


```python
from court_queue import courtQueue


static_matrix = [[1, 2, 3], [6, 5, 4], [7, 8, 9]]
x = courtQueue(static_matrix, detail=True)
print(x.peek())
print(x.top())
```


### Output


```bash
1
1
```


### You can clear all the values from the queue


```python
from court_queue import courtQueue


static_matrix = [[1, 2, 3], [6, 5, 4], [7, 8, 9]]
x = courtQueue(static_matrix, detail=True)
print(x)
x.clear()
print(x)
```


### Output


```bash
╒══════════╤═══╤═══╤═══╤══════════╕
│ <- EXIT  │ 1 │ 2 │ 3 │ <- ENTER │
├──────────┼───┼───┼───┼──────────┤
│ ENTER -> │ 6 │ 5 │ 4 │ EXIT ^   │
├──────────┼───┼───┼───┼──────────┤
│ ^ EXIT   │ 7 │ 8 │ 9 │ <- ENTER │
╘══════════╧═══╧═══╧═══╧══════════╛
╒══════════╤══╤══╤══╤══════════╕
│ <- EXIT  │  │  │  │ <- ENTER │
├──────────┼──┼──┼──┼──────────┤
│ ENTER -> │  │  │  │ EXIT ^   │
├──────────┼──┼──┼──┼──────────┤
│ ^ EXIT   │  │  │  │ <- ENTER │
╘══════════╧══╧══╧══╧══════════╛
```


## License


This project is licensed under the Apache License 2.0 - see the [LICENSE](https://opensource.org/licenses/Apache-2.0) for more details.
