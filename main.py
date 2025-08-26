import torch
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from sklearn.preprocessing import MultiLabelBinarizer

# ==============================
# 1. Rutas locales
# ==============================
model_path = "./scibert_classifier"  # carpeta donde está tu modelo

# ==============================
# 2. Cargar modelo, tokenizer y mlb
# ==============================
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

# Cargar clases desde JSON
with open("label_encoder.json", "r") as f:
    classes = json.load(f)

# Reconstruir el mlb
mlb = MultiLabelBinarizer(classes=classes)
mlb.fit([[]])  # "hack" para inicializar

# ==============================
# 3. Función de predicción
# ==============================
def predict(text, model, tokenizer, mlb, threshold=0.5, max_length=256):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()

    encoding = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=max_length,
        return_tensors="pt"
    ).to(device)

    with torch.no_grad():
        outputs = model(**encoding)
        logits = outputs.logits
        probs = torch.sigmoid(logits).cpu().numpy()[0]

    # Mapear clases con umbral
    predicted_labels = [cls for cls, prob in zip(mlb.classes_, probs) if prob > threshold]
    return predicted_labels, probs

# ==============================
# 4. Texto de prueba
# ==============================
example_text = "Mechanisms of myocardial ischemia induced by epinephrine: comparison with exercise-induced ischemia. The role of epinephrine in eliciting myocardial ischemia was examined in patients with coronary artery disease. Objective signs of ischemia and factors increasing myocardial oxygen consumption were compared during epinephrine infusion and supine bicycle exercise. Both epinephrine and exercise produced myocardial ischemia as evidenced by ST segment depression and angina. However, the mechanisms of myocardial ischemia induced by epinephrine were significantly different from those of exercise. Exercise-induced myocardial ischemia was marked predominantly by increased heart rate and rate-pressure product with a minor contribution of end-diastolic volume, while epinephrine-induced ischemia was characterized by a marked increase in contractility and a less pronounced increase in heart rate and rate-pressure product. These findings indicate that ischemia produced by epinephrine, as may occur during states of emotional distress, has a mechanism distinct from that due to physical exertion."
labels, probs = predict(example_text, model, tokenizer, mlb)

print("Etiquetas predichas:", labels)
print("Probabilidades:", probs)
