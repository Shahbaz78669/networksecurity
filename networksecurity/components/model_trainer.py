import os
import sys
import mlflow
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.artifact_entity import DataTransformationArtifact, ModelTrainerArtifact

from networksecurity.entity.config_entity import ModeltrainerConfig


from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import save_object, load_object
from networksecurity.utils.main_utils.utils import load_numpy_array_data, evaluate_modles
from networksecurity.utils.ml_utils.metric.classification_matric import get_classification_score


from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,
    GradientBoostingClassifier,
    RandomForestClassifier
)
import dagshub
dagshub.init(repo_owner='Shahbaz78669', repo_name='networksecurity', mlflow=True)


class ModelTrainer:
    def __init__(
        self,
        model_trainer_config: ModeltrainerConfig,
        data_transformation_artifact: DataTransformationArtifact
    ):
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def track_mlflow(self, best_model, classificationmetric):
        mlflow.set_experiment("NetworkSecurity")
        with mlflow.start_run():
            f1_score = classificationmetric.f1_score
            precision_score = classificationmetric.precision_score
            recall_score = classificationmetric.recall_score

            mlflow.log_metric("f1_score", f1_score)
            mlflow.log_metric("precision_score", precision_score)
            mlflow.log_metric("recall_score", recall_score)
            mlflow.sklearn.log_model(best_model, "model")

    def train_model(self, X_train, y_train, X_test, y_test):
        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Decision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost Classifier": AdaBoostClassifier(),


        }
        params = {
            "Logistic Regression": {
                # "C": [0.01, 0.1, 1, 10, 100],
                # "solver": ["lbfgs", "liblinear"],
                "max_iter": [100, 200, 500]
            },

            "Decision Tree": {
                "criterion": ["gini", "entropy"],
                # "max_depth": [None, 5, 10, 20],
                # "min_samples_split": [2, 5, 10],
                # "min_samples_leaf": [1, 2, 4]
            },
            "Random Forest": {
                "n_estimators": [50, 100, 200],
                # "criterion": ["gini", "entropy"],
                # "max_depth": [None, 5, 10],
                # "min_samples_split": [2, 5],
                # "max_features": ["sqrt", "log2"]
            },
            "Gradient Boosting": {
                # "n_estimators": [50, 100, 200],
                # "learning_rate": [0.01, 0.05, 0.1, 0.2],
                # "max_depth": [3, 5, 7],
                # "subsample": [0.7, 0.8, 1.0],
                "min_samples_split": [2, 5]
            },
            "AdaBoost Classifier": {
                "n_estimators": [50, 100, 200],
                # "learning_rate": [0.01, 0.05, 0.1, 0.5, 1.0]
            }
        }

        model_report: dict = evaluate_modles(X_train=X_train, y_train=y_train,
                                             X_test=X_test, y_test=y_test, models=models, params=params)

        best_model_score = max(sorted(model_report.values()))

        best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]

        best_model = models[best_model_name]

        y_train_pred = best_model.predict(X_train)

        classification_train_matric = get_classification_score(y_true=y_train, y_pred=y_train_pred)

        # tracking ML flow
        self.track_mlflow(best_model, classification_train_matric)

        y_test_pred = best_model.predict(X_test)
        classification_test_matric = get_classification_score(y_true=y_test, y_pred=y_test_pred)

        preprocessor = load_object(file_path=self.data_transformation_artifact.transformed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)
        os.makedirs(model_dir_path, exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)
        save_object(self.model_trainer_config.trained_model_file_path, obj=Network_Model)
        save_object(os.path.join("final_model", "best_model.pkl"), best_model)

        # Modle Trainer Artifact
        model_trainer_artifact = ModelTrainerArtifact(
            trianed_model_file_path=self.model_trainer_config.trained_model_file_path,
            train_metric_artifact=classification_train_matric,
            test_metric_artifact=classification_test_matric,
        )

        logging.info(f"Model trainer artifact:{model_trainer_artifact}")
        return model_trainer_artifact

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            train_file_path = self.data_transformation_artifact.transformed_train_file_path
            test_file_path = self.data_transformation_artifact.transformed_test_file_path

            train_arr = load_numpy_array_data(train_file_path)
            test_arr = load_numpy_array_data(test_file_path)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],

            )

            model = self.train_model(x_train, y_train, x_test, y_test)
            return model
        except Exception as e:
            raise NetworkSecurityException(e, sys)
