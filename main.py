import torch
import json
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Ruta del modelo
model_path = "./scibert_classifier"

# Cargar tokenizer y modelo
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Cargar clases desde JSON
with open(f"{model_path}/label_encoder.json", "r") as f:
    clases = json.load(f)
clases = np.array(clases)  # para indexar fácilmente

# Función de predicción
def predecir(texto):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)

    inputs = tokenizer(
        texto,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=512
    ).to(device)

    outputs = model(**inputs)
    pred = torch.argmax(outputs.logits, dim=1).item()
    return clases[pred]   # directamente el nombre de la clase

# Ejemplo
ejemplo = "Hypothesis: ACE inhibitors improves heart disease outcomes via acute myeloid leukemia pathways. Methods: randomized controlled trial with 264 diabetic patients, measuring interstitial nephritis and kidney. Results: better quality of life measures. Conclusion: cost-effectiveness implications."

print("Predicción:", predecir(ejemplo))
