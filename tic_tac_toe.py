import cv2
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV)
    return thresh

def find_grid_lines(thresh):
    edges = cv2.Canny(thresh, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
    return lines

def extract_cells(thresh):
    height, width = thresh.shape
    cell_h, cell_w = height // 3, width // 3
    cells = []
    for i in range(3):
        row = []
        for j in range(3):
            cell = thresh[i * cell_h: (i + 1) * cell_h, j * cell_w: (j + 1) * cell_w]
            row.append(cell)
        cells.append(row)
    return cells

def recognize_symbol(cell):
    contours, _ = cv2.findContours(cell, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return ""
    largest_contour = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest_contour)
    if area < 100:  # Ignore small noise
        return ""
    x, y, w, h = cv2.boundingRect(largest_contour)
    aspect_ratio = w / float(h)
    return "X" if aspect_ratio > 0.8 and aspect_ratio < 1.2 else "O"

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
    _ = find_grid_lines(thresh)
    cells = extract_cells(thresh)
    board = [[recognize_symbol(cell) for cell in row] for row in cells]
    return check_winner(board)

if __name__ == "__main__":
    image_path = "tic_tac_toe_board.jpg"  # Replace with your image path
    result = check_state(image_path)
    print(result)

