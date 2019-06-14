#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
@Author:     lufeng
@Contact:    lufeng0614@163.com
@Time:       2019/6/6  13:42
@note：      ***
"""
import numpy as np
import pandas as pd
import jieba
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim import models
from gensim.corpora import Dictionary
from gensim.matutils import sparse2full
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import ComplementNB, BernoulliNB, GaussianNB, MultinomialNB

from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


def nlpclassification(input_sql, output_sql, temp_table, new_table,
                      modelpath, machine, columns, params_train):
    """
    :return:
    """
    nlpclassifier_dict = {
        'randforclassifier': randforclassifier,
        'logisticregression': logisticregression,
        'linearsvc': linearsvc,
        'complementnb': complementnb,
        'bernoullinb': bernoullinb,
        'gaussiannb': gaussiannb,
        'multinomialnb': multinomialnb
    }
    global data_pred, Data
    if machine[1] == "train":  # 训练
        data_pred = nlpclassifier_dict[machine[0]](input_sql.read_sql(temp_table[0]),
                                                   columns,
                                                   modelpath,
                                                   params_train)
    elif machine[1] == "predict":  # 预测
        data_pred = model_load(input_sql.read_sql(temp_table[1]),
                               columns,
                               modelpath)
        Data = eval2classifier(input_sql.read_sql(temp_table[1]), data_pred, columns)

    elif machine[1] == 'test':  # 训练+预测
        nlpclassifier_dict[machine[0]](input_sql.read_sql(temp_table[0]),
                                       columns,
                                       modelpath,
                                       params_train)
        data_pred = model_load(input_sql.read_sql(temp_table[1]),
                               columns,
                               modelpath)
        Data = eval2classifier(input_sql.read_sql(temp_table[1]), data_pred, columns)

    if isinstance(data_pred, str):
        Code = -1  # 模型预测成功，但结果为空
        Data = ''
        return Code, data_pred, Data
    else:
        if output_sql.write_sql(new_table[0], data_pred) is None:
            Code = 0
            data_pred = 'write to %s success' % new_table[0]
            return Code, data_pred, Data


# 模型预测
def model_load(te_df, columns, modelpath):
    """
    :return:
    """
    # model
    clf = joblib.load(modelpath)
    tfidf_vec = tfidf_vector_load(te_df[columns['col_feature']], modelpath)

    predict_df = pd.DataFrame(clf.predict(tfidf_vec))

    if predict_df.empty:
        return 'predict data is None'
    else:
        # 计算打分列
        if hasattr(clf, "predict_proba"):
            prob_pos = pd.DataFrame(clf.predict_proba(tfidf_vec)[:, 1])
            return predict_score_df(te_df, predict_df, prob_pos, columns)
        elif hasattr(clf, "decision_function"):  # use decision function
            prob_pos = pd.DataFrame(clf.decision_function(tfidf_vec)[:, 0])
            print(prob_pos.shape)
            return predict_score_df(te_df, predict_df, prob_pos, columns)
        else:
            return predict_score_df(te_df, predict_df, prob_pos=pd.DataFrame(), columns=columns)


# create predict_score df
def predict_score_df(te_df, predict_df, prob_pos, columns):
    """
    :return: predict_score
    """
    predict_df.columns = columns['col_predict']
    if prob_pos.empty:

        predict_score = pd.concat([te_df[columns['col_label']],
                                   predict_df,
                                   te_df[columns['col_feature']]], axis=1)
    else:
        prob_pos.columns = ['dm_score']
        predict_score = pd.concat([te_df[columns['col_label']],
                                   predict_df, prob_pos,
                                   te_df[columns['col_feature']]], axis=1)
    return predict_score


# 分类模型评估
def eval2classifier(test_df, data_pred, columns):
    """
    :return:
    """
    eval2clf = dict()

    # label_true = pd.DataFrame(test_df[columns['col_label']], dtype=np.int).values
    label_true = test_df[columns['col_label']].iloc[:, 0].values
    label_pred = data_pred[columns['col_predict']].iloc[:, 0].values
    pos_label = list(set(label_true))

    # 准确率
    # eval2clf['precision'] = round(precision_score(label_true, label_pred), 5)
    # recall rate
    eval2clf['recall'] = round(recall_score(label_true, label_pred), 5)
    # f1
    eval2clf['f1'] = round(f1_score(label_true, label_pred, pos_label=pos_label[0]), 5)

    return eval2clf


# tfidf vector train
def tfidf_vector_train(corpus, modelpath):
    """
    :param corpus:
    :return:
    """
    # vectorizer = TfidfVectorizer()
    # X_train = vectorizer.fit_transform(corpus.iloc[:, 0].values)
    #
    # return X_train

    corpora_documents = []
    for i in corpus.iloc[:, 0].values:
        seg_data = jieba.lcut(i, cut_all=False)
        corpora_documents.append(seg_data)
    dct = Dictionary(corpora_documents)  # fit dictionary
    dct.save(modelpath + '.dict')
    corpus2bow = [dct.doc2bow(line) for line in corpora_documents]  # convert corpus to BoW format

    model = models.TfidfModel(corpus2bow, normalize=True)
    model.save(modelpath + '.tfidf')
    title_tfidf = model[corpus2bow]

    title_vecs = np.vstack([sparse2full(cc, len(dct)) for cc in title_tfidf])

    # ndarray to dataframe
    df = pd.DataFrame(title_vecs[0:, 0:])
    return df


# tfidf vector load
def tfidf_vector_load(corpus, modelpath):
    """
    dict load / tfidf model load
    :param text: predict text
    :return:
    """
    predict_corpus = []
    # segword jieba
    for i in corpus.iloc[:, 0].values:
        seg_data = jieba.lcut(i, cut_all=False)
        predict_corpus.append(seg_data)
    dct = Dictionary.load(modelpath + '.dict')
    corpus2bow = [dct.doc2bow(line) for line in predict_corpus]  # convert corpus to BoW format
    model = models.TfidfModel.load(modelpath + '.tfidf')

    title_tfidf = model[corpus2bow]
    title_vecs = np.vstack([sparse2full(c, len(dct)) for c in title_tfidf])

    # ndarray to dataframe
    df = pd.DataFrame(title_vecs[0:, 0:])
    return df


# 随机森林分类
def randforclassifier(tr_df, columns, modelpath, params_train):
    """
    :return:
    """
    tfidf_vec = tfidf_vector_train(tr_df[columns['col_feature']], modelpath)

    # n_jobs=n_jobs, bootstrap=bootstrap
    forest = RandomForestClassifier(n_estimators=int(params_train[0]),
                                    n_jobs=int(params_train[1]),
                                    bootstrap=params_train[2])
    forest = forest.fit(tfidf_vec,
                        tr_df[columns['col_label']])

    joblib.dump(forest, modelpath, compress=1)

    return 'Train model success'


# LogisticRegression
def logisticregression(tr_df, columns, modelpath, params_train):
    """
    :return:
    """
    tfidf_vec = tfidf_vector_train(tr_df[columns['col_feature']], modelpath)

    # 'solver': 'liblinear', 'random_state': 2080, n_jobs
    logist = LogisticRegression(solver=params_train[0],
                                random_state=int(params_train[1]),
                                n_jobs=int(params_train[2]))

    logist = logist.fit(tfidf_vec,
                        tr_df[columns['col_label']])

    joblib.dump(logist, modelpath, compress=1)

    return 'Train model success'


# C-Support Vector Classification
def linearsvc(tr_df, columns, modelpath, params_train):
    """
    :return:
    """
    tfidf_vec = tfidf_vector_train(tr_df[columns['col_feature']], modelpath)

    # C / random_state / penalty
    svc = SVC(C=float(params_train[0]), kernel=str(params_train[1]),
              random_state=int(params_train[2]))

    svc = svc.fit(tfidf_vec,
                  tr_df[columns['col_label']])

    joblib.dump(svc, modelpath, compress=1)

    return 'Train model success'


# ComplementNB
def complementnb(tr_df, columns, modelpath, params_train):
    """
    :return:
    """
    tfidf_vec = tfidf_vector_train(tr_df[columns['col_feature']], modelpath)

    # C / norm / penalty
    naivebayes = ComplementNB(alpha=params_train[0],
                              norm=params_train[1],
                              fit_prior=params_train[2])

    naivebayes = naivebayes.fit(tfidf_vec,
                                tr_df[columns['col_label']])

    joblib.dump(naivebayes, modelpath, compress=1)

    return 'Train model success'


# BernoulliNB
def bernoullinb(tr_df, columns, modelpath, params_train):
    """
    :return:
    """
    tfidf_vec = tfidf_vector_train(tr_df[columns['col_feature']], modelpath)

    # alpha / binarize / fit_prior
    naivebayes = BernoulliNB(alpha=params_train[0],
                             binarize=params_train[1],
                             fit_prior=params_train[2])

    naivebayes = naivebayes.fit(tfidf_vec,
                                tr_df[columns['col_label']])

    joblib.dump(naivebayes, modelpath, compress=1)

    return 'Train model success'


# GaussianNB
def gaussiannb(tr_df, columns, modelpath, params_train):
    """
    :return:
    """
    tfidf_vec = tfidf_vector_train(tr_df[columns['col_feature']], modelpath)

    # var_smoothing
    naivebayes = GaussianNB(var_smoothing=params_train[0])

    naivebayes = naivebayes.fit(tfidf_vec,
                                tr_df[columns['col_label']])

    joblib.dump(naivebayes, modelpath, compress=1)

    return 'Train model success'


# MultinomialNB
def multinomialnb(tr_df, columns, modelpath, params_train):
    """
    :return:
    """
    tfidf_vec = tfidf_vector_train(tr_df[columns['col_feature']], modelpath)

    # alpha / fit_prior
    naivebayes = MultinomialNB(alpha=params_train[0],
                               fit_prior=params_train[1])

    naivebayes = naivebayes.fit(tfidf_vec,
                                tr_df[columns['col_label']])

    joblib.dump(naivebayes, modelpath, compress=1)

    return 'Train model success'

