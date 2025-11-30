from injury_predictor import injury_predictor

print("Fixing model compatibility...")
result = injury_predictor.train()
print("Fixed! New model saved.")
print(f"Accuracy: {result['accuracy']:.3f}")
print("Now restart: uvicorn main:app --reload")
