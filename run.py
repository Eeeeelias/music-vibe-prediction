import model
from dataset_preparation import get_train_test_split


if __name__ == '__main__':
    X_train, X_test, y_train, y_test = get_train_test_split(restict_to=('Classical', 'Piano', 'Pop',
                                                                        'Rock', 'Musical'),
                                                            input_features="features_ext.pkl")
    # validate with dummmy classifier
    model.dummy(X_train, X_test, y_train, y_test)

    # train and test the model
    clf = model.set_classifier("random_forest")
    model.train(clf, X_train, y_train)
    model.test_classifier(X_test, y_test)
