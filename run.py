from ml import run_model_pipeline
from modules import run_pipeline

def main() -> None:
    """
    Entry point for running the full analytics and prediction pipeline.
    """
    df = run_pipeline()
    run_model_pipeline(df)


if __name__ == "__main__":
    main()
