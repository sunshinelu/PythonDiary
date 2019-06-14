#-*- coding: UTF-8 -*-


from .nlp_classifier import nlpclassification


input_sql = {}
output_sql = {}
temp_table = ["nlp_3class","nlp_3class_copy"]
new_table = ["nlp_3class_pred"]
modelpath = ""
machine = ["linearsvc",""]
columns = {
    "col_feature": ["SEED_TITLE"],
    "col_label": ["LABEL"],
    "col_predict": ["PRED"]
	}
params_train = []

nlpclassification(input_sql, output_sql, temp_table, new_table,
                      modelpath, machine, columns, params_train)