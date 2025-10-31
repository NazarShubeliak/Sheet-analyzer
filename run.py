from ml import run_model_pipeline
from modules import run_pipeline

if __name__ == "__main__":
    df = run_pipeline()
    run_model_pipeline(df)
