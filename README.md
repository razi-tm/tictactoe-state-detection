# Tic-Tac-Toe State Detection

## Description
This project determines the state of a Tic-Tac-Toe game using an image as input. The function analyzes the board and returns one of four states: `X Wins`, `O Wins`, `Ongoing`, or `Draw`.

## File Structure
- `tic_tac_toe.py`: Contains the `check_state` function.

## Dependencies
- OpenCV (`cv2`)
- NumPy

## Usage
```python
from tic_tac_toe import check_state
state = check_state("path/to/image.jpg")
print(state)
```

