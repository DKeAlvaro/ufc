import argparse
import os
import joblib
from datetime import datetime

# Use absolute imports to avoid relative import issues
try:
    from src.config import MODELS_DIR
except ImportError:
    # Fallback for when running directly
    from ..config import MODELS_DIR

def predict_new_fight(fighter1_name, fighter2_name, model_path):
    """
    Loads a trained model and predicts the outcome of a new, hypothetical fight.
    """
    print("--- Predicting New Fight ---")
    
    # 1. Load the trained model
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at '{model_path}'. Please train and save a model first.")
    
    print(f"Loading model from {model_path}...")
    model = joblib.load(model_path)
    print(f"Model '{model.model.__class__.__name__}' loaded.")

    # 2. Create the fight dictionary for prediction
    # The predict method requires a dictionary with specific keys.
    # We use today's date as a placeholder for the event date.
    fight = {
        'fighter_1': fighter1_name,
        'fighter_2': fighter2_name,
        'event_date': datetime.now().strftime('%B %d, %Y')
        # Other keys like 'winner', 'method', etc., are not needed for prediction.
    }

    # 3. Make the prediction
    print(f"\nPredicting winner for: {fighter1_name} vs. {fighter2_name}")
    prediction_result = model.predict(fight)
    
    if prediction_result and prediction_result.get('winner'):
        winner = prediction_result['winner']
        prob = prediction_result['probability']
        print(f"\n---> Predicted Winner: {winner} ({prob:.1%}) <---")
    else:
        print("\nCould not make a prediction. One of the fighters may not be in the dataset.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Predict the outcome of a new UFC fight.")
    parser.add_argument('fighter1', type=str, help="The full name of the first fighter (e.g., 'Jon Jones').")
    parser.add_argument('fighter2', type=str, help="The full name of the second fighter (e.g., 'Stipe Miocic').")
    parser.add_argument(
        '--model_path', 
        type=str, 
        default=os.path.join(MODELS_DIR, 'XGBoostModel.joblib'),
        help="Path to the saved model file."
    )
    args = parser.parse_args()
    
    predict_new_fight(args.fighter1, args.fighter2, args.model_path) 