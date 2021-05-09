import csv
from sklearn.metrics import roc_curve, confusion_matrix, classification_report
from matplotlib import pyplot as plt
import numpy as np


def read_csv(path_file):
    enter = 0
    noenter = 0
    with open(path_file, newline='') as File:
        reader = csv.reader(File, delimiter=';', quotechar=';',
                            quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            enter = enter + int(row[1])
            noenter = noenter + int(row[2])

    return enter, noenter


def read_csv_conf(path_file):
    results = []
    with open(path_file, newline='') as File:
        reader = csv.reader(File, delimiter=';', quotechar=';',
                            quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            results.append(np.array(row, dtype=float))
    return results


def get_direct_rates(enter_gt, no_enter_gt, enter_rt, no_enter_rt):
    FP = abs(enter_gt - enter_rt)
    TP = enter_gt - FP
    FN = abs(no_enter_gt - no_enter_rt)
    TN = no_enter_gt - FN
    FRR = FN / (FN + TP)
    TRR = TN / (FP + TN)
    TPR = TP / (FN + TP)
    return TP, FP, TN, FN, FRR, TRR, TPR


def get_others_rates(TP, FP, TN, FN):
    acurracy = (TP + TN) / (TP + FP + TN + FN)
    precision = TP / (TP + FP)
    iou = TP / (FN + TP + FP)
    f1_score = 2 * (TP / (FN + 2 * TP + FP))
    return acurracy, precision, iou, f1_score


def get_classification_report(real, predict):
    print(classification_report(real, predict))


def get_curve_roc(real, predict, conf):
    positives = (real == predict) * 1
    print(positives)
    x_curve, y_curve, h = roc_curve(positives, conf)
    plt.plot(x_curve, y_curve)
    plt.title("CURVA ROC")
    plt.xlabel("True Positive Rate")
    plt.ylabel("False Positive Rate")
    plt.savefig("./curva_roc.png")


def get_curve_cap(real, predict, conf):
    positive = real == predict
    sorted_index = np.flip(np.argsort(conf))
    curve = np.add.accumulate((positive * 1)[sorted_index])
    curve = np.concatenate(([0.0], curve))
    x_curve = np.arange(0, curve.shape[0]) / (curve.shape[0] - 1)
    y_curve = curve / (curve.shape[0] - 1)
    plt.plot([0, 1], [0, 1])
    plt.plot(x_curve, y_curve)
    plt.title("CURVA CAP")
    plt.xlabel("Perceptil")
    plt.ylabel("Acierto")
    plt.savefig("./curva_cap.png")


def get_PR_curve_no_optimizada(real, predict, conf):
    positive = real == predict
    sorted_index = np.flip(np.argsort(conf))
    sorted_positive = positive[sorted_index]
    sorted_conf = conf[sorted_index]
    tp = 0
    fp = 0
    p = np.sum(positive)
    x_curve = [0]
    y_curve = [1]
    for pos_case, conf_case in zip(sorted_positive, sorted_conf):
        if pos_case:
            tp += 1
        else:
            fp += 1
        precision = tp / (tp + fp)
        recall = tp / p

        x_curve.append(recall)
        y_curve.append(precision)
    plt.plot(x_curve, y_curve)
    plt.title("Curva Precision Recall (P-R)")
    plt.xlabel("Precision")
    plt.ylabel("Recall")
    plt.savefig("./curva_pr.png")


if __name__ == "__main__":
    path_file_gt = "./groundtruth.csv"
    path_file_rt = "./results.csv"
    path_conf = "./groundtruth_conf.csv"
    enter_gt, no_enter_gt = read_csv(path_file_gt)
    enter_rt, no_enter_rt = read_csv(path_file_rt)
    TP, FP, TN, FN, FRR, TRR, TPR = get_direct_rates(enter_gt, no_enter_gt, enter_rt, no_enter_rt)
    print(TP, FP, TN, FN, FRR, TRR, TPR)
    acurracy, precision, iou, f1_score = get_others_rates(TP, FP, TN, FN)
    print(acurracy, precision, iou, f1_score)

    results = read_csv_conf(path_conf)
    get_classification_report(results[0], results[1])
    get_curve_roc(results[0], results[1], results[2])
    get_curve_cap(results[0], results[1], results[2])
    get_PR_curve_no_optimizada(results[0], results[1], results[2])
