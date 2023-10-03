import pickle

import numpy as np
import seaborn as sns
import sklearn.ensemble
from matplotlib import pyplot as plt
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPClassifier


def dummy(X_train, X_test, y_train, y_test):
    # make dummy classifier that predicts the most common class
    model = DummyClassifier(strategy='prior')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(f"Dummy accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print(f"Dummy F1 score: {f1_score(y_test, y_pred, average='weighted'):.2f}")


def set_classifier(option="random_forest"):
    # Create the classifier

    if option == "random_forest":
        classifier = RandomForestClassifier(n_estimators=100)
    elif option == "mlp":
        classifier = MLPClassifier(hidden_layer_sizes=(100,), max_iter=500, alpha=0.0001,)
    elif option == "ada_boost":
        classifier = AdaBoostClassifier(n_estimators=100)
    elif option == "svm":
        classifier = sklearn.svm.SVC()

    return classifier


def train(classifier, X, y):
    print("Starting training")
    k = 5  # Replace with the number of folds you want
    kf = KFold(n_splits=k, shuffle=True, random_state=42)  # You can adjust the random_state if needed
    cv_scores = []
    max_score = 0
    best_clf = None

    for train_index, test_index in kf.split(X):
        X_train, X_test = np.array(X)[train_index], np.array(X)[test_index]
        y_train, y_test = np.array(y)[train_index], np.array(y)[test_index]

        model = classifier

        # Train the model on the training data
        model.fit(X_train, y_train)

        # Evaluate the model on the test data and store the score
        y_pred = model.predict(X_test)
        score = f1_score(y_test, y_pred, average='weighted')

        cv_scores.append(score)

        if score > max_score:
            max_score = score
            best_clf = model

    average_score = sum(cv_scores) / len(cv_scores)
    print(f"Average score: {average_score:.2f}")

    # Save the model
    pickle.dump(best_clf, open("model.pkl", "wb"))

    # Print the accuracy
    print(f"Accuracy of the best classifier on train: {accuracy_score(y, best_clf.predict(X)):.2f}")


def test_classifier(test_features, test_labels):
    # Load the model
    classifier = pickle.load(open("model.pkl", "rb"))
    y_pred = classifier.predict(test_features)

    # Print the accuracy
    print(f"Accuracy of the classifier on test: {accuracy_score(test_labels, y_pred):.2f}")
    print(f"F1 score on the test set: {f1_score(test_labels, y_pred, average='weighted'):.2f}")

    # plot a heatmap of the test results
    cm = confusion_matrix(test_labels, y_pred)
    class_names = classifier.classes_

    # Create the heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=class_names, yticklabels=class_names)

    # Add labels and title
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.title("Confusion Matrix Heatmap")

    # Show the plot
    plt.show()