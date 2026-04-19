import sys
import os
import certifi
import pandas as pd
import numpy as np
import pymongo
from dotenv import load_dotenv

from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from uvicorn import run as app_run

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.constants.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME
)

# Initializations
ca = certifi.where()
load_dotenv()
mongo_db_url = os.getenv("MONGODB_URL_KEY")

client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    from starlette.responses import RedirectResponse
    return RedirectResponse(url="/docs")


@app.get("/train", tags=["training"])
async def train_route():
    """
    Train the phishing URL detection model.
    Runs the complete training pipeline.
    """
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return JSONResponse(
            status_code=200,
            content={"message": "Training completed successfully!"}
        )
    except Exception as e:
        logging.error(f"Training failed: {str(e)}")
        raise NetworkSecurityException(e, sys)


@app.post("/predict", tags=["prediction"])
async def predict_route(request: Request, file: UploadFile = File(...)):
    """
    Predict phishing URLs from a CSV file.

    Expected CSV format:
    - Must contain feature columns matching training data
    - May optionally contain 'Result' or 'result' column (will be dropped)

    Returns:
    - JSON with predictions and statistics
    - CSV file saved to 'prediction_output/output.csv'
    """
    print("\n--- NEW PREDICTION REQUEST RECEIVED ---")
    try:
        # Step 1: Read the uploaded CSV
        df = pd.read_csv(file.file)
        logging.info(f"File loaded. Original Shape: {df.shape}")
        print(f"Columns in uploaded file: {df.columns.tolist()}")

        # Step 2: Load Preprocessor and Model
        # Ensure these paths match your folder structure exactly
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/best_model.pkl")

        if preprocessor is None or final_model is None:
            error_msg = "Model files not found. Check 'final_model' folder."
            logging.error(error_msg)
            return JSONResponse(
                status_code=500,
                content={"error": error_msg}
            )

        # Step 3: Clean the incoming data
        # Drop the target column if the user included it
        target_cols = ['Result', 'result']
        df = df.drop(columns=[c for c in target_cols if c in df.columns], errors='ignore')
        logging.info(f"Shape after dropping target columns: {df.shape}")

        # Step 4: The "id" Fix
        # We found that the model was trained with an 'id' column.
        # If it's missing from the CSV, we add it back as a dummy.
        if "id" not in df.columns:
            df["id"] = 0
            logging.info("Dummy 'id' column added for schema alignment.")

        # Step 5: Feature Reordering
        # This ensures the columns match the EXACT sequence seen during training
        try:
            expected_features = preprocessor.feature_names_in_
            df = df[expected_features]
            logging.info(f"Features reordered. Final shape: {df.shape}")
        except Exception as e:
            error_msg = f"Feature reordering failed: {str(e)}"
            logging.error(error_msg)
            return JSONResponse(
                status_code=400,
                content={"error": error_msg}
            )

        # Step 6: Transform and Predict
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        y_pred = network_model.predict(df)
        logging.info(f"Predictions generated. Shape: {y_pred.shape}")

        # Step 7: Finalize Output
        df['predicted_column'] = y_pred

        # Save predictions to CSV
        os.makedirs('prediction_output', exist_ok=True)
        output_path = 'prediction_output/output.csv'
        df.to_csv(output_path, index=False)
        logging.info(f"Predictions saved to {output_path}")

        # Step 8: Calculate statistics
        unique_predictions = int(np.unique(y_pred).shape[0])
        prediction_distribution = {
            "phishing": int((y_pred == 1).sum()),
            "legitimate": int((y_pred == 0).sum()),
            "total": int(len(y_pred))
        }

        # Step 9: Return JSON response
        return JSONResponse(
            status_code=200,
            content={
                "message": "Prediction successful",
                "predictions_count": len(y_pred),
                "unique_classes": unique_predictions,
                "distribution": prediction_distribution,
                "output_file": output_path,
                "sample_predictions": y_pred[:10].tolist()  # First 10 predictions
            }
        )

    except Exception as e:
        error_msg = f"Prediction failed: {str(e)}"
        print("--- THE ACTUAL ERROR IS BELOW ---")
        print(error_msg)
        print("---------------------------------")
        logging.error(error_msg)
        raise NetworkSecurityException(e, sys)


@app.get("/health", tags=["health"])
async def health_check():
    """
    Health check endpoint.
    Returns status of the API and model availability.
    """
    try:
        # Check if model files exist
        preprocessor_exists = os.path.exists("final_model/preprocessor.pkl")
        model_exists = os.path.exists("final_model/best_model.pkl")

        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "model_preprocessor_available": preprocessor_exists,
                "model_best_model_available": model_exists,
                "all_models_ready": preprocessor_exists and model_exists
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "unhealthy", "error": str(e)}
        )

if __name__ == "__main__":
    app_run(app, host="0.0.0.0", port=8000)
