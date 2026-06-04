# 🛡️ Wallet Guard – AI-Powered Hybrid Fraud Detection Platform

## Overview

Wallet Guard is a production-ready fraud detection platform that combines machine learning, rule-based anomaly validation, explainable AI, and audit logging to detect suspicious wallet transactions in real time.

The system uses an XGBoost fraud detection model enhanced with a hybrid decision engine to classify transactions into:

- ✅ APPROVE
- ⚠️ REVIEW
- ❌ REJECT

It provides explainable fraud analysis through SHAP feature attribution, detailed audit logs, JWT-secured APIs, and a Streamlit-based analytics dashboard.

---

## 🌐 Live Demo

### Frontend (Streamlit)

https://wallet-fraud-guard-frontend-prjgmukesfkzsquttkdbgj.streamlit.app/

### Backend API

https://wallet-fraud-guard.onrender.com

---

## ✨ Key Features

### Hybrid Fraud Detection Engine

- XGBoost-based fraud risk scoring
- Rule-based anomaly validation
- Hybrid risk fusion strategy
- 3-tier transaction decision engine

### Explainable AI

- SHAP feature attribution
- Human-readable fraud explanations
- Top risk factor analysis
- Risk contribution reporting

### Secure Backend

- FastAPI REST API
- JWT Authentication
- Password hashing using bcrypt
- Protected endpoints

### Audit & Compliance

- Transaction persistence
- Fraud audit logs
- Decision traceability
- Historical fraud analytics

### Analytics Dashboard

- Fraud rate monitoring
- Transaction statistics
- Approval / Review / Rejection breakdown
- Audit log explorer

---

## 🏗️ System Architecture

```text
                    ┌────────────────────┐
                    │  Streamlit Frontend │
                    └─────────┬──────────┘
                              │
                              ▼
                    ┌────────────────────┐
                    │   FastAPI Backend  │
                    └─────────┬──────────┘
                              │
             ┌────────────────┼────────────────┐
             ▼                ▼                ▼

      XGBoost Model     Rule Engine      JWT Security

             ▼                ▼
       Hybrid Risk Fusion Engine

                    ▼

            Decision Engine

      APPROVE | REVIEW | REJECT

                    ▼

         SHAP Explainability Layer

                    ▼

              SQLite Database
```

---

## 🤖 Machine Learning Pipeline

### Model

- XGBoost Classifier

### Dataset

- Credit Card Fraud Detection Dataset

### Feature Engineering

Additional behavioral features include:

- Failed login attempts
- Transaction velocity
- Merchant risk score
- Device novelty
- Geo-distance anomaly
- IP risk score
- Night-time transaction indicator

### Threshold Optimization

Custom threshold tuning was performed to balance:

- Precision
- Recall
- False Positive Rate

### Results

| Metric | Value |
|----------|----------|
| Precision | 83.3% |
| False Positives | 14 |
| Legitimate Transactions Evaluated | 56,651+ |

---

## ⚙️ Hybrid Decision Engine

### Rule-Based Validation

Examples:

- High transaction amount
- New device detected
- Multiple failed attempts
- High transaction velocity
- High-risk merchant
- Suspicious IP score
- Abnormal geo-distance

### Risk Fusion Formula

```text
Final Risk Score =
(0.55 × ML Risk Score)
+
(0.45 × Rule Risk Score)
```

### Decision Logic

| Risk Score | Decision |
|------------|----------|
| < 0.30 | APPROVE |
| 0.30 – 0.50 | REVIEW |
| > 0.50 | REJECT |

---

## 🔍 Explainability

Wallet Guard provides transparent fraud reasoning through SHAP.

### Triggered Rules

```text
High transaction amount
New device detected
Multiple failed attempts
```

### SHAP Explanations

```text
V14 increased fraud risk by 3.84
V10 increased fraud risk by 1.03
V17 increased fraud risk by 0.54
```

### Outputs

- Top risk factors
- Impact scores
- Human-readable fraud explanations

---

## 🗄️ Database Design

### Users

Stores:

- User information
- Credentials
- Account creation metadata

### Wallets

Stores:

- Wallet ownership
- Current balance
- Wallet status

### Transactions

Stores:

- Transaction history
- Risk scores
- Final decisions
- Timestamps

### Fraud Logs

Stores:

- Triggered rules
- SHAP explanations
- Risk factors
- Audit metadata

---

## 🚀 API Endpoints

### Authentication

```http
POST /auth/register
POST /auth/login
```

### Wallet Operations

```http
POST /wallet/transfer
```

### Fraud Monitoring

```http
GET /fraud/logs
GET /fraud/rejected
GET /fraud/analytics
GET /fraud/transaction/{transaction_id}
```

---

## 📈 Performance

### Load Testing

- Concurrent Users: 50
- Transactions Processed: 1,200+
- Zero data loss during testing

### Inference Performance

```json
{
  "average_latency_ms": 8.63,
  "maximum_latency_ms": 10.99,
  "minimum_latency_ms": 8.03
}
```

Average model inference latency remained below:

```text
10ms
```

---

## 🛠️ Tech Stack

### Backend

- FastAPI
- Python
- JWT Authentication
- SQLite

### Machine Learning

- XGBoost
- SHAP
- Scikit-Learn
- NumPy
- Pandas

### Frontend

- Streamlit

### Deployment

- Render (Backend)
- Streamlit Community Cloud (Frontend)

---

## 💻 Local Setup

### Clone Repository

```bash
git clone https://github.com/<username>/wallet-fraud-guard.git
cd wallet-fraud-guard
```

### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Start Backend

```bash
uvicorn main:app --reload
```

### Start Dashboard

```bash
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔮 Future Enhancements

- PostgreSQL migration
- Redis caching
- Real-time fraud streaming
- Graph-based fraud analytics
- Multi-wallet support
- User risk profiling
- Automated model retraining

---

## 🎯 Resume Highlights

- Built a production-ready FastAPI fraud detection platform with JWT authentication, audit logging, and SQLite persistence.
- Reduced false-positive fraud alerts through a hybrid XGBoost and rule-based detection engine, achieving 83.3% precision with only 14 false positives across 56K+ legitimate transactions.
- Delivered explainable fraud analysis using SHAP feature attribution and audit-ready logging across users, wallets, transactions, and fraud-decision workflows.

---

## 📄 License

MIT License
