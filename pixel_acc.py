import cv2
import numpy as np

def count_correct_yellow_pixels(gt_path, pred_path):
    # Load images
    gt = cv2.imread(gt_path)
    pred = cv2.imread(pred_path)

    # Convert BGR to HSV for better yellow detection
    gt_hsv = cv2.cvtColor(gt, cv2.COLOR_BGR2HSV)
    pred_hsv = cv2.cvtColor(pred, cv2.COLOR_BGR2HSV)

    # Define yellow range in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([35, 255, 255])

    # Create yellow masks
    gt_yellow = cv2.inRange(gt_hsv, lower_yellow, upper_yellow)
    pred_yellow = cv2.inRange(pred_hsv, lower_yellow, upper_yellow)

    # Find overlap (logical AND of masks)
    correct_yellow = cv2.bitwise_and(gt_yellow, pred_yellow)

    # Count non-zero pixels
    correct = np.count_nonzero(correct_yellow)
    gt_total = np.count_nonzero(gt_yellow)
    pred_total = np.count_nonzero(pred_yellow)

    return correct, gt_total, pred_total

# Example usage
correct, gt_total, pred_total = count_correct_yellow_pixels('ground_truth.png', 'prediction.png')
print(f"Correct yellow pixels: {correct}")
print(f"Total yellow in GT: {gt_total}, in prediction: {pred_total}")
if gt_total > 0:
    ratio = correct / gt_total
    print(f"Ratio of correct yellow pixels to total yellow pixels in GT: {ratio:.4f}")
else:
    print("No yellow pixels found in ground truth.")
