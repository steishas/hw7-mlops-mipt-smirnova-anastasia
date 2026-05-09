"""
Планирование A/B-теста для ML-модели
Сравнение Model A (DummyClassifier) и Model B (RandomForest 100 деревьев)
"""

import numpy as np
from scipy.stats import fisher_exact
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

np.random.seed(42)

# Загрузка данных
iris = load_iris()
X, y = iris.data, iris.target
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Модель A — 50 деревьев
model_A = DummyClassifier(strategy='stratified', random_state=42)
model_A.fit(X_train, y_train)

# Модель B — 100 деревьев
model_B = RandomForestClassifier(n_estimators=100, random_state=42)
model_B.fit(X_train, y_train)

# Предсказания
y_pred_A = model_A.predict(X_test)
y_pred_B = model_B.predict(X_test)

# Метрики
acc_A = accuracy_score(y_test, y_pred_A)
acc_B = accuracy_score(y_test, y_pred_B)

print("-" * 60)
print("Планирование A/B-теста для ML-модели")
print("-" * 60)

print(f"  Параметры эксперимента:")
print(f"  Модель A: DummyClassifier")
print(f"  Модель B: RandomForestClassifier(n_estimators=100)")
print(f"  Метрика: accuracy")
print(f"  Размер тестовой выборки: {len(X_test)}")
print(f"  Уровень значимости alpha: 0.05")
print(f"  Способ разделения: случайный 50/50 (random_state=42)")
print(f"  Длительность: однократное измерение на фиксированном тесте")

# Точный тест Фишера
cm_A = np.sum(y_pred_A == y_test)
cm_B = np.sum(y_pred_B == y_test)
n = len(y_test)

contingency_table = [
    [cm_A, n - cm_A],
    [cm_B, n - cm_B]
]

odds_ratio, p_value = fisher_exact(contingency_table, alternative='two-sided')

print(f"  Результаты:")
print(f"  Accuracy модели A: {acc_A:.4f}")
print(f"  Accuracy модели B: {acc_B:.4f}")
print(f"  Odds ratio: {odds_ratio:.4f}")
print(f"  P-value: {p_value:.4f}")

print(f" Вывод:")
if p_value < 0.05:
    print(f"   Различие статистически значимо (p={p_value:.4f} < 0.05)")
    if acc_B > acc_A:
        print(f" Рекомендация: развернуть модель B в production")
    else:
        print(f" Рекомендация: оставить модель A в production")
else:
    print(f"  Нет статистически значимых различий (p={p_value:.4f} >= 0.05)")
    print(f"  Рекомендация: оставить текущую модель A, продолжить наблюдение")
