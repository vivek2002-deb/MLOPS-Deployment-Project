import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, f1_score,precision_score, recall_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint

import mlflow
import mlflow.sklearn

logger=get_logger(__name__)

class ModelTraining:
    def __init__(self,train_data,test_data,model_output_path):
        self.train_data = train_data
        self.test_data = test_data
        self.model_output_path = model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS


    def load_and_split_data(self):
        try:
            logger.info("loading data from {self.train_data}")
            train_data = load_data(self.train_data)

            logger.info("loading data from {self.test_data}")
            test_data = load_data(self.test_data)

            x_train = train_data.drop(columns=['booking_status'])
            y_train = train_data['booking_status']

            x_test = test_data.drop(columns=['booking_status'])
            y_test = test_data['booking_status']

            logger.info("Data loaded and split into features and target variable")
            return x_train, y_train, x_test, y_test
        
        except Exception as e:
            logger.error(f"Error loading and splitting data: {e}")
            raise CustomException("Failed to load and split data", e)
        
    def train_model(self,x_train,y_train):
        try:
            logger.info("Training the model")
            model = lgb.LGBMClassifier(random_state=self.random_search_params['random_state'])

            logger.info("Starting our Hyperparameter tuning")
            # Perform Randomized Search CV
            random_search = RandomizedSearchCV(
                estimator=model,
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                n_jobs=self.random_search_params['n_jobs'],
                cv=self.random_search_params['cv'],
                verbose=self.random_search_params['verbose'],
                random_state=self.random_search_params['random_state'],
                scoring=self.random_search_params['scoring']
            )

            logger.info("Strarting our hyperparameter tuning")
            # Fit the model
            random_search.fit(x_train, y_train)

            logger.info("Best parameters found: ")
            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_
            logger.info(f"Best parameters: {best_params}")

            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error training the model: {e}")
            raise CustomException("Failed to train the model", e)
        
    def evaluate_model(self, model, x_test, y_test):
        try:
            logger.info("Evaluating the model")
            y_pred = model.predict(x_test)

            accuracy = accuracy_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)

            logger.info(f"Model evaluation metrics: Accuracy: {accuracy}, F1 Score: {f1}, Precision: {precision}, Recall: {recall}")
            return {"accuracy": accuracy, "f1_score": f1, "precision": precision, "recall": recall}
        
        except Exception as e:
            logger.error(f"Error evaluating the model: {e}")
            raise CustomException("Failed to evaluate the model", e)
        
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)

            logger.info(f"Saving the model")
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved at {self.model_output_path}")
        
        except Exception as e:
            logger.error(f"Error saving the model: {e}")
            raise CustomException("Failed to save the model", e)
        
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Starting MLflow run")
                logger.info("Starting the model training pipeline")
                logger.info("logging the training and testing dataset to MLFLOW")

                mlflow.log_artifact(self.train_data, artifact_path="dataset")
                mlflow.log_artifact(self.test_data, artifact_path="dataset")

                x_train, y_train, x_test, y_test = self.load_and_split_data()
                model = self.train_model(x_train, y_train)
                evaluation_metrics = self.evaluate_model(model, x_test, y_test)
                self.save_model(model)

                logger.info("logging the model into MLFLOW")
                mlflow.log_artifact(self.model_output_path, artifact_path="model")

                logger.info("logging the model parameters and metrics into MLFLOW")
                mlflow.log_params(model.get_params())
                mlflow.log_metrics(evaluation_metrics)
                logger.info("Model training pipeline completed successfully")
        
        except Exception as e:
            logger.error(f"Error during model training pipeline: {e}")
            raise CustomException("Error while model training pipeline", e)
        

if __name__ == "__main__":
    trainer = ModelTraining(
        train_data=PROCESSED_TRAIN_DATA_PATH,
        test_data=PROCESSED_TEST_DATA_PATH,
        model_output_path=MODEL_OUTPUT_PATH
    )
    trainer.run()
    logger.info("Model training script executed successfully")