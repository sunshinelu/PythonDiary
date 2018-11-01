# -*- coding: utf-8 -*-
"""
Created on Mon Oct 29 15:57:44 2018

@author: Mindong
"""

import pandas as pd
import pymysql
from sqlalchemy import create_engine
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

#机器学习
from sklearn.linear_model import LogisticRegression #逻辑回归
from sklearn.svm import SVC,LinearSVC #支持向量机
from sklearn.ensemble import RandomForestClassifier # 随机森林
from sklearn.neighbors import KNeighborsClassifier #K最近邻算法
from sklearn.naive_bayes import GaussianNB# 朴素贝叶斯
from sklearn.linear_model import Perceptron#感知机
from sklearn.linear_model import SGDClassifier# 不知道
from sklearn.tree import DecisionTreeClassifier# 决策树


yconnect=pymysql.connect(
        user='root',
        password='root',
        host='localhost',
        port=3306,
        database='titanic')
train=pd.read_sql('select * from train',yconnect)
test=pd.read_sql('select * from test',yconnect)
train_P=train[['Pclass','Survived']].groupby(['Pclass'],as_index=False).mean().sort_values(by='Survived',ascending=False)
train_S=train[['Sex','Survived']].groupby(['Sex'],as_index=False).mean().sort_values(by='Survived',ascending=False)
train_E=train[['Embarked','Survived']].groupby(['Embarked'],as_index=False).mean().sort_values(by='Embarked',ascending=False)
g=sns.FacetGrid(train,col='Survived')

g.map(plt.hist,'Pclass',bins=20)
grid=sns.FacetGrid(train,col='Survived',row='Pclass',size=2.2,aspect=1.6)
grid.map(plt.hist,'Age',alpha=.5,bins=20)
grid.add_legend()
g=sns.FacetGrid(train,row='Embarked',size=2.2,aspect=1.6)
g.map(sns.pointplot,'Pclass','Survived','Sex',palette='deep')
grid.add_legend()
g=sns.FacetGrid(train,row='Embarked',col='Survived',size=2.2,aspect=1.6)
g.map(sns.barplot,'Sex','Fare',alpha=.5)
g.add_legend()
train=train.drop(['Ticket','Cabin'],axis=1)
test=test.drop(['Ticket','Cabin'],axis=1)
combine=[train,test]

for dataset in combine:
    dataset['Title']=dataset.Name.str.extract('([A-Za-z]+)\.',expand=False)

for dataset in combine:
    dataset['Title']=dataset['Title'].replace(['Capt','Col','Countess','Don','Dr','Jonkheer','Lady',
        'Major','Rev','Sir','Dona'],'Rare')
    dataset['Title']=dataset['Title'].replace('Mlle','Miss')
    dataset['Title']=dataset['Title'].replace('Ms','Miss')
    dataset['Title']=dataset['Title'].replace('Mme','Mrs')

train_F=train[['Title','Survived']].groupby(['Title'],as_index=False).mean().sort_values(by='Survived',ascending=False)

title_mapping={'Mr':1,'Miss':2,'Mrs':3,'Master':4,'Rare':5}
for dataset in combine:
    dataset['Title']=dataset['Title'].map(title_mapping)
    dataset['Title']=dataset['Title'].fillna(0)

train=train.drop(['Name','PassengerId'],axis=1)
test=test.drop(['Name'],axis=1)
combine=[train,test]

for dataset in combine:
    dataset['Sex']=dataset['Sex'].map({'female':1,'male':0}).astype(int)
    
grid=sns.FacetGrid(train,row='Pclass',col='Sex')
grid.map(plt.hist,'Age',alpha=.5,bins=20)

grid.add_legend()

#用性别和class的不同来预测年龄，填补年龄的缺失值
guess_ages=np.zeros((2,3))
for dataset in combine:
    for i in range(0,2):
        for j in range(0,3):
            guess_df=dataset[(dataset['Sex']==i)&(dataset['Pclass']==j+1)]['Age'].dropna()
            age_guess=guess_df.median()
            guess_ages[i,j]=int(age_guess/0.5+0.5)*0.5
    
    for i in range(2):
        for j in range(3):
            dataset.loc[(dataset.Age.isnull())&(dataset.Sex==i)&(dataset.Pclass==j+1),
                        'Age']=guess_ages[i,j]
    dataset['Age']=dataset['Age'].astype(int)
                                         
train['AgeBand']=pd.cut(train['Age'],5)
for dataset in combine:
    dataset.loc[dataset['Age']<16,'Age']=0
    dataset.loc[(dataset['Age']>=16)&(dataset['Age']<32),'Age']=1
    dataset.loc[(dataset['Age']>=32)&(dataset['Age']<48),'Age']=2
    dataset.loc[(dataset['Age']>=48)&(dataset['Age']<64),'Age']=3
    dataset.loc[(dataset['Age']>=64),'Age']=4
train=train.drop(['AgeBand'],axis=1)
combine=[train,test]
#家庭人数
for dataset in combine:
    dataset['FamilySize']=dataset['SibSp']+dataset['Parch']+1

for dataset in combine:
    dataset['IsAlone']=0
    dataset.loc[dataset['FamilySize']==1,'IsAlone']=1

train=train.drop(['SibSp','Parch','FamilySize'],axis=1)
test=test.drop(['SibSp','Parch','FamilySize'],axis=1)
combine=[train,test]

for dataset in combine:
    dataset['Age*Pclass']=dataset.Age*dataset.Pclass

#填补Embarked的空值，用众数添加
for dataset in combine:
    dataset['Embarked']=dataset['Embarked'].fillna(dataset['Embarked'].dropna().mode()[0])    
    dataset['Embarked']=dataset['Embarked'].map({'S':0,'C':1,'Q':2}).astype(int)
    dataset['Fare']=dataset['Fare'].fillna(dataset['Fare'].dropna().mode()[0])
train['FareBand']=pd.qcut(train['Fare'],4)   
for dataset in combine:
    dataset.loc[dataset['Fare']<=7.91,'Fare']=0
    dataset.loc[(dataset['Fare']>7.91)&(dataset['Fare']<=14.454),'Fare']=1
    dataset.loc[(dataset['Fare']>14.454)&(dataset['Fare']<=31.0),'Fare']=2
    dataset.loc[(dataset['Fare']>31.0),'Fare']=3

train=train.drop(['FareBand'],axis=1)
combine=[train,test]

#建模
X_train=train.drop(['Survived'],axis=1)
y_train=train['Survived']
X_test=test.drop(['PassengerId'],axis=1).copy()


#机器学习建模
#逻辑回归
logreg=LogisticRegression()
logreg.fit(X_train,y_train)
Y_pred=logreg.predict(X_test)
acc_log=round(logreg.score(X_train,y_train)*100,2)
#80.469999999999999

coeff=pd.DataFrame(train.columns.delete(0))
coeff.columns=['Feature']
coeff['Correlation']=pd.Series(logreg.coef_[0])

#支持向量机
svc=SVC()
svc.fit(X_train,y_train)
Y_pred=svc.predict(X_test)
acc_svm=round(svc.score(X_train,y_train)*100,2)
# acc_svm=96.299999999999997

#KNN
knn=KNeighborsClassifier()
knn.fit(X_train,y_train)
Y_pred=knn.predict(X_test)
acc_knn=round(knn.score(X_train,y_train)*100,2)
# acc_knn=74.189999999999998

#朴素贝叶斯
gaussian=GaussianNB()
gaussian.fit(X_train,y_train)
Y_pred=gaussian.predict(X_test)
acc_gau=round(gaussian.score(X_train,y_train)*100,2)

# acc_gau=76.989999999999995

#感知机
perceptron=Perceptron()
perceptron.fit(X_train,y_train)
Y_pred=perceptron.predict(X_train)
acc_pre=round(perceptron.score(X_train,y_train)*100,2)

#acc_pre=61.840000000000003

#liner_svc
liner_svc=LinearSVC()
liner_svc.fit(X_train,y_train)
Y_pred=liner_svc.predict(X_test)
acc_l_svc=round(liner_svc.score(X_train,y_train)*100,2)
# acc_l_svc=79.799999999999997

#SGC
sgd=SGDClassifier()
sgd.fit(X_train,y_train)
Y_pred=sgd.predict(X_test)
acc_sgd=round(sgd.score(X_train,y_train)*100,2)
# acc_sgd=61.840000000000003

#决策树
decision=DecisionTreeClassifier()
decision.fit(X_train,y_train)
Y_pred=decision.predict(X_test)
acc_dec=round(decision.score(X_train,y_train)*100,2)

# acc_dec=100

# 随机森林
ran_F=RandomForestClassifier()
ran_F.fit(X_train,y_train)
Y_pred=ran_F.predict(X_test)
acc_ran=round(ran_F.score(X_train,y_train)*100,2)
# acc_ran=98.540000000000006

models=pd.DataFrame({'Model':['Logistic Regression','SVM','KNN','Naive Bayes','Perceptron','line_SVC',
                              'SGD','Decision Tree','RandomForest'],
    'Score':[acc_log,acc_svm,acc_knn,acc_gau,acc_pre,acc_l_svc,acc_sgd,acc_dec,acc_ran]})

submission=pd.DataFrame({
        'PassengerId':test['PassengerId'],
        'Survived':Y_pred})

conn=create_engine('mysql+mysqldb://root:root@localhost:3306/titanic?''charset=utf8')
pd.io.sql.to_sql(Y_pred,'predict',conn,schema='titanic',if_exists=('append'))








































