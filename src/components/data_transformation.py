import sys
from dataclasses import dataclass

import numpy as np 
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder,StandardScaler

from src.exception import CustomException
import logging
import os
from src.utils import save_object
from typing import Tuple

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts','preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformation_object(self)->ColumnTransformer:

        """
        Creates and returns a preprocessing pipeline for numerical and categorical features.

        The pipeline includes:
            - For numerical columns: median imputation and standard scaling.
            - For categorical columns: most frequent imputation, ordinal encoding with predefined category order, and standard scaling.

        Returns:
            ColumnTransformer: A scikit-learn ColumnTransformer object that applies the defined preprocessing
            steps to the appropriate columns.
        """ 

        try:
            logging.info('Data Transformation initiated')
            # Define which columns should be ordinal-encoded and which should be scaled
            categorical_cols = ['cut', 'color','clarity']
            numerical_cols = ['carat', 'depth','table', 'x', 'y', 'z']
            
            # Define the custom ranking for each ordinal variable
            cut_categories = ['Fair', 'Good', 'Very Good','Premium','Ideal']
            color_categories = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
            clarity_categories = ['I1','SI2','SI1','VS2','VS1','VVS2','VVS1','IF']
            
            logging.info('Pipeline Initiated')

            ## Numerical Pipeline
            num_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='median')),
                ('scaler',StandardScaler())

                ]

            )

            # Categorigal Pipeline
            cat_pipeline=Pipeline(
                steps=[
                ('imputer',SimpleImputer(strategy='most_frequent')),
                ('ordinalencoder',OrdinalEncoder(categories=[cut_categories,color_categories,clarity_categories])),
                ('scaler',StandardScaler())
                ]

            )

            preprocessor=ColumnTransformer([
            ('num_pipeline',num_pipeline,numerical_cols),
            ('cat_pipeline',cat_pipeline,categorical_cols)
            ])
            
            logging.info('Pipeline Completed')

            return preprocessor

            

        except Exception as e:
            logging.error("Error in Data Trnasformation", exc_info=True)
            raise CustomException(e,sys)
        
    def initiate_data_transformation(self, train_path: str, test_path: str) -> Tuple[np.ndarray, np.ndarray, str]:

        """
        Applies data preprocessing to training and test datasets.

        This method reads the training and testing datasets from the given file paths,
        separates the input features and target variable, applies preprocessing pipelines 
        (including imputation, scaling, and encoding), and returns the transformed arrays 
        along with the path to the saved preprocessor object.

        Parameters:
            train_path (str): File path to the training dataset CSV.
            test_path (str): File path to the testing dataset CSV.

        Returns:
            Tuple[np.ndarray, np.ndarray, str]: A tuple containing:
                - Transformed training data as a NumPy array,
                - Transformed testing data as a NumPy array,
                - Path to the saved preprocessor pickle file.
        """

        try:
            # Reading train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Read train and test data completed')
            logging.info(f'Train Dataframe Head : \n{train_df.head().to_string()}')
            logging.info(f'Test Dataframe Head  : \n{test_df.head().to_string()}')

            logging.info('Obtaining preprocessing object')

            preprocessing_obj = self.get_data_transformation_object()

            target_column_name = 'price'
            drop_columns = [target_column_name,'id']

            input_feature_train_df = train_df.drop(columns=drop_columns,axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=drop_columns,axis=1)
            target_feature_test_df=test_df[target_column_name]
            
            ## Trnasformating using preprocessor obj
            input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df)

            logging.info("Applying preprocessing object on training and testing datasets.")
            

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(

                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj

            )
            logging.info('Preprocessor pickle file saved')

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
            
        except Exception as e:
            logging.error("Exception occured sin the initiate_datatransformation", exc_info=True)

            raise CustomException(e,sys)