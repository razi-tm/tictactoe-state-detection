import cv2
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    return thresh

def extract_cells(thresh):
    height, width = thresh.shape
    cell_h, cell_w = height // 3, width // 3
    print(f"Image Dimensions: {height}x{width}, Cell Size: {cell_h}x{cell_w}")
    
    cells = []
    for i in range(3):
        row = []
        for j in range(3):
            cell = thresh[i * cell_h: (i + 1) * cell_h, j * cell_w: (j + 1) * cell_w]
            row.append(cell)
        cells.append(row)
    # Visual inspection
    grid = np.vstack([np.hstack(row) for row in cells])
    cv2.imshow("All Cells", grid)
    cv2.waitKey(1500)
    cv2.destroyAllWindows()

    # Check if cells are correctly extracted
    print(f"Extracted {len(cells)} rows, Each row length: {[len(row) for row in cells]}")
    return cells

def recognize_symbol(cell, i, j):
    contours, _ = cv2.findContours(cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print(f"Cell ({i}, {j}): Empty")
        return ""
    
    # Filter small noise
    contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 300]
    print(f"Cell ({i}, {j}): {len(contours)} valid contours found")
    
    if len(contours) == 0:
        return ""
    
    # Analyze the largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)
    perimeter = cv2.arcLength(largest_contour, True)
    circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0
    x, y, w, h = cv2.boundingRect(largest_contour)
    aspect_ratio = w / float(h)
    
    print(f"Cell ({i}, {j}): Area = {area}, Aspect Ratio = {aspect_ratio:.2f}, Circularity = {circularity:.2f}")
    
    # Determine X or O
    if circularity > 0.75:  # High circularity indicates 'O'
        return "O"
    elif len(contours) >= 2 or (0.8 <= aspect_ratio <= 1.2):  # Multiple lines or square-like = 'X'
        return "X"
    else:
        return ""

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] != "":
            return f"{row[0]} Wins"
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != "":
            return f"{board[0][col]} Wins"
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return f"{board[0][0]} Wins"
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return f"{board[0][2]} Wins"

    return "Draw" if all(cell != "" for row in board for cell in row) else "Ongoing"

def check_state(image_path):
    thresh = preprocess_image(image_path)
    cells = extract_cells(thresh)

    board = [[recognize_symbol(cells[i][j], i, j) for j in range(3)] for i in range(3)]

    print("Detected Board:")
    for row in board:
        print(row)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return check_winner(board)

if __name__ == "__main__":
    image_path = "/home/rtm/Downloads/dooz/Data/O Wins.png"  # Replace with your image path
    result = check_state(image_path)
    print("Result:", result)

