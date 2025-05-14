import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml, load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE

logger=get_logger(__name__)

class DataProcessor:
    def __init__(self,train_data, test_data,processed_dir,config):
        self.train_data = train_data
        self.test_data = test_data
        self.processed_dir = processed_dir
        self.config = read_yaml(config)
        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)

    def preprocess_data(self,df):
        try:
            logger.info("Starting out Data Processing step")
            logger.info("Dropping the columns")
            df.drop(columns=['Unnamed: 0','Booking_ID'], inplace=True)
            df.drop_duplicates(inplace=True)

            ##Divide the data into categorical and numerical columns
            cat_cols = self.config['data_processing']['cat_cols']
            num_cols = self.config['data_processing']['num_cols']

            logger.info("label encoding the categorical columns")
            le=LabelEncoder()
            mapping={}

            for col in cat_cols:
                df[col]=le.fit_transform(df[col])
                mapping[col]=dict(zip(le.classes_,le.transform(le.classes_)))

            logger.info("Skewness Handling")
            skewness_threshold = self.config['data_processing']['skewness_threshold']
            skewness = df[num_cols].apply(lambda x: x.skew())

            for col in skewness[skewness > skewness_threshold].index:
                df[col] = np.log1p(df[col])

            return df
        
        except Exception as e:
            logger.error(f"Error in preprocessing data: {e}")
            raise CustomException("Failed to preprocess data", e)
        
    def balance_data(self,df):
        try:
            logger.info("Balancing the data using SMOTE")
            smote=SMOTE(random_state=42)
            X = df.drop(columns=['booking_status'])
            y = df['booking_status']

            X_resampled, y_resampled = smote.fit_resample(X, y)
            balanced_df=pd.concat([X_resampled,y_resampled],axis=1)

            logger.info("Data balancing completed")
            return balanced_df
        except Exception as e:
            logger.error(f"Error in balancing data: {e}")
            raise CustomException("Failed to balance data", e)
        
    def feature_engineering(self,df):
        try:
            logger.info("Feature Engineering")
            x=df.drop(columns=['booking_status'])
            y=df['booking_status']

            model = RandomForestClassifier(random_state=42)
            model.fit(x, y)

            feature_importance = model.feature_importances_
            feature_importance_df = pd.DataFrame({'feature': x.columns, 'importance': feature_importance})
            feature_importance_df = feature_importance_df.sort_values(by='importance', ascending=False)
            top_features=feature_importance_df.head(self.config['data_processing']['num_features'])
            logger.info(f"Top features: {top_features}")

            df=df[top_features['feature'].tolist() + ['booking_status']]

            logger.info("Feature Engineering completed")
            return df
        except Exception as e:
            logger.error(f"Error in feature engineering: {e}")
            raise CustomException("Failed to perform feature engineering", e)
        
    def save_data(self,df, file_path):
        try:
            logger.info(f"Saving processed data to {file_path}")
            df.to_csv(file_path, index=False)
            logger.info("Data saved successfully")
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            raise CustomException("Failed to save data", e)
        
    def process(self):
        try:
            logger.info("Loading data from RAW directory")
            train_df=load_data(self.train_data)
            test_df=load_data(self.test_data)

            train_df=self.preprocess_data(train_df)
            test_df=self.preprocess_data(test_df)

            train_df=self.balance_data(train_df)

            train_df=self.feature_engineering(train_df)
            test_df=test_df[train_df.columns]

            self.save_data(train_df, PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df, PROCESSED_TEST_DATA_PATH)

            logger.info("Data processing completed successfully")

        except Exception as e:
            logger.error(f"Error during preprocessing pipeline: {e}")
            raise CustomException("Error while data preprocessing pipeline", e)
        


if __name__ == "__main__":
    processor = DataProcessor(TRAIN_FILE_PATH, TEST_FILE_PATH, PROCESSED_DIR, CONFIG_PATH)
    processor.process()



