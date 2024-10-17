import torch
import os

def load_house_price():
    # 현재 파일의 디렉토리 경로를 가져옴
    current_dir = os.path.dirname(__file__)

    # 절대 경로로 변환
    X_path = os.path.join(current_dir, 'data', '01', 'X_train_tensor.pt', weights_only=True)
    y_path = os.path.join(current_dir, 'data', '01', 'y_train_tensor.pt', weights_only=True)
    test_path = os.path.join(current_dir, 'data', '01', 'X_test_tensor.pt', weights_only=True)

    # 파일을 로드
    X = torch.load(X_path)
    y = torch.load(y_path)
    TEST = torch.load(test_path)

    return X, y, TEST
