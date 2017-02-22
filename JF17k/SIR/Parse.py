from __future__ import print_function, absolute_import, division


import numpy as np

result_on_neg = np.loadtxt("prediction_for_label0.txt")
result_on_pos = np.loadtxt("prediction_for_label1.txt")

PR_Rate = open("PR_Rate.txt", "w")
ROC = open("ROC.txt", "w")
TP_and_FP = open("TP_and_FP.txt", "w")

PR_Rate.write("thresh\tprecision\trecall\n")
ROC.write("thresh\tTPR\tFPR\n")
TP_and_FP.write("thresh\tTP\tFP\n")


for i in range(101):
    thresh = i / 100

    tp = 0
    fp = 0
    tn = 0
    fn = 0

    for j in range(result_on_neg.shape[0]):
        if result_on_neg[j, 1] < thresh:  # negative examples classified to negative examples
            tn += 1
        else:  # negative examples classified to positive examples
            fp += 1

    for j in range(result_on_pos.shape[0]):
        if result_on_pos[j, 1] < thresh:  # positive examples classified to negative examples
            fn += 1
        else:
            tp += 1

    TP_and_FP.write("{}\t{}\t{}\n".format(thresh, tp, fp))

    TPR = tp / (tp + fn)
    FPR = fp / (fp + tn)
    ROC.write("{}\t{}\t{}\n".format(thresh, TPR, FPR))

    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    PR_Rate.write("{}\t{}\t{}\n".format(thresh, precision, recall))


