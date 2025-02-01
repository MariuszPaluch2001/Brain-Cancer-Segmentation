import torch
from sklearn.metrics import recall_score, precision_score, f1_score


def recall(y_true, y_pred):
    return recall_score(
        y_true.numpy().flatten(), y_pred.numpy().flatten(), zero_division=1.0
    )


def precission(y_true, y_pred):
    return precision_score(
        y_true.numpy().flatten(), y_pred.numpy().flatten(), zero_division=1.0
    )


def f1(y_true, y_pred):
    return f1_score(
        y_true.numpy().flatten(), y_pred.numpy().flatten(), zero_division=1.0
    )


def dice(y_true, y_pred, smooth=100):
    y_true_flatten = torch.flatten(y_true)
    y_pred_flatten = torch.flatten(y_pred)

    intersection = torch.sum(y_true_flatten * y_pred_flatten)
    union = torch.sum(y_true_flatten) + torch.sum(y_pred_flatten)
    return (2 * intersection + smooth) / (union + smooth)
