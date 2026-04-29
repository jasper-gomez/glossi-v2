## 📈Glossi
An upgraded version of Glossi utilizing System Dynamics (SD) simulation.

---

## 💡Objective
Glossi 2.0 aims to create a digital simulation of the hair data I gathered during Glossi 1.0. Through an SD simulation, this models the dynamics of hair dryness.

---

## ⚙️Methodology
1. **Data Gathering**: Data used is from Glossi 1.0.
2. **Data Preprocesing**: The data has undergone numerical encoding using `LabelEncoder` and feature selection using [`FeSeCo`](https://github.com/jasper-gomez/feature-selection-companion)
3. **Model Development**: Developed a simple Linear Regression (LR) model.
4. **Coefficient Extraction**: Using the LR model, the coefficients and intercept have been identified.

---

## 📝Evaluation Results
- **R2 Score**: 0.49389830590874906 (Good enough for human factors)
- **MSE**: 0.502868000847341
- **MAE**: 0.5705126874430705
- **RMSE**: 0.7091318642166216
- **Explained Variance Score**: 0.4939475909608376

---

## 🔍Findings

#### **Target Variable**: min_dryness (minimum dryness)

#### **Intercept**: 4.20783117458634

**Coefficients**
- `shampoo_used_today`: 0.53021863
- `conditioner_used_today`: 0.16230531
- `leave_in_amt`: - 0.21417387
- `sweat`: 0.03747662
- `humidity`: - 0.01787766
- `bath_intensity`: - 0.09956396
- `wind_exposure`: 0.10925777

