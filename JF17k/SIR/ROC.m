delimiterIn = '\t';
headerlineIn = 1;
PR_Rate_data = importdata('PR_Rate.txt', delimiterIn, headerlineIn);
ROC_data = importdata('ROC.txt', delimiterIn, headerlineIn);
TP_and_FP_data = importdata('TP_and_FP.txt', delimiterIn, headerlineIn);

figure(1);
plot(PR_Rate_data.data(:, 3), PR_Rate_data.data(:, 2), '-.r');
xlabel('Recall')
ylabel('Precision')
title('P-R Curve')

figure(2);
plot(ROC_data.data(:, 3), ROC_data.data(:, 2), '-.r');
hold on
plot(ROC_data.data(:, 3), ROC_data.data(:, 1), '--b');
xlabel('False Positive Rate')
ylabel('True Positive Rate')
title('ROC Curve')

figure(3);
plot(TP_and_FP_data.data(:, 3), TP_and_FP_data.data(:, 2), '-.r');
xlabel('False Positive Samples')
ylabel('True Positive Samples')
title('False Positive and True Positive Samples')