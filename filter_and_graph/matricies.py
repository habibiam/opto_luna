import numpy as np

"""Matrix Correction"""
# Matrix for 5 color matrix w/ CXR*0.5
# matrix = np.array([[1, -0.192, -0.045, -0.139, 0],
#                    [-0.728, 1, -0.43, -0.09, -0.013],
#                    [-0.22, -0.326, 1, -0.182, -0.014],
#                    [-0.2, -0.335, -1.11, 1, -0.013],
#                    [-0.017, -0.03, -0.1, -0.136, 1]])

# Matrix for 5 color matrix normalized to 15000 Except wen
# matrix = np.array([[1, -0.158, -0.069, -0.137, -0.01],
#                    [-0.937, 1, -0.73, -0.128, -0.04],
#                    [-0.22, -0.195, 1, -0.129, -0.01],
#                    [-0.17, -0.284, -1.56, 1, -0.02],
#                    [-0.013, -0.017, -0.1, -0.096, 1]])

# Matrix for non-normailzed data. Only baseline subtraction (10-21-16)
# matrix = np.array([[1, -0.19, -0.022, -0.138, 0],
#                    [-0.728, 1, -0.217, -0.09, -0.013],
#                    [-0.43, -0.65, 1, -0.36, -0.025],
#                    [-0.2, -0.32, -0.556, 1, -0.012],
#                    [-0.016, -0.028, -0.05, -0.138, 1]])

# Zero Matrix
ZERO_matrix = np.array([[1, 0, 0, 0, 0],
                        [0, 1, 0, 0, 0],
                        [0, 0, 1, 0, 0],
                        [0, 0, 0, 1, 0],
                        [0, 0, 0, 0, 1]])

# Matrix MODIFIED w/ EZRA for non-normailzed data. Only baseline subtraction (10-21-16) 20mW
matrix_MOD = np.array([[1, -0.2, 0.095, -0.138, 0],
                       [-0.63, 1, -0.22, 0.07, -0.013],
                       [0.03, -0.55, 1.0, -0.32, -0.018],
                       [0.02, 0.05, -0.57, 1, 0],
                       [0, 0, 0.03, -0.145, 1]])

# Allelic Ladder 20mW
matrix_MOD_AL = np.array([[1, -0.2, 0.095, -0.138, 0],
                       [-0.63, 1, -0.22, 0.07, -0.013],
                       [0.03, -0.62, 1.0, -0.32, -0.018],
                       [0.02, 0, -0.57, 1, 0],
                       [0, 0, 0.03, -0.145, 1]])

# Matrix MODIFIED w/ EZRA for non-normailzed data. Only baseline subtraction (10-21-16) 9mW
matrix_MOD2 = np.array([[1, -0.205, 0.105, -0.138, 0],
                       [-0.65, 1, -0.24, 0.07, -0.011],
                       [0.035, -0.58, 1.0, -0.28, -0.018],
                       [0.02, 0.05, -0.587, 1, 0],
                       [0, 0, 0.03, -0.145, 1]])

# Matrix 5mW, 10mW, (and most likely 9mW) . Only baseline subtraction (10-24-16)
matrix_10mW = np.array([[1, -0.18, -0.015, -0.11, 0.005],
                        [-0.74, 1, -0.19, -0.07, -0.016],
                        [-0.45, -0.67, 1, -0.3, -0.03],
                        [-0.21, -0.34, -0.57, 1, -0.01],
                        [-0.01, -0.02, -0.05, -0.14, 1]])

# Theresa's Matrix made for 10/13/16 Allelic Ladder
matrix_Theresa = np.array([[1, -0.2516, -0.0609, -0.1772, -0.0309],
                           [-0.7117, 1, -0.2266, -0.1772, -0.0662],
                           [-0.2941, -0.9296, 1, -0.4952, -0.0965],
                           [-0.0118, -0.6685, -0.5731, 1, -0.0662],
                           [-0.1732, -0.0959, -0.0759, -0.1470, 1]])

# Matrix 20mW RAW (No filters of any kind). (11/22/16)
matrix_20mW = np.array([[1, -0.234, -0.04, -0.178, 0],
                        [-0.737, 1, -0.229, -0.136, 0],
                        [-0.459, -0.666, 1, -0.397, 0],
                        [-0.205, -0.336, -0.554, 1, 0],
                        [0, 0, -0.052, -0.136, 1]])