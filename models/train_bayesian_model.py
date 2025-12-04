"""
EditalShield: Bayesian Model Trainer
Trains and validates a Naive Bayes model for IP exposure detection
"""

import numpy as np
import pandas as pd
import json
import pickle
import os
from datetime import datetime
from pathlib import Path

try:
    from sklearn.naive_bayes import GaussianNB
    from sklearn.model_selection import StratifiedKFold
    from sklearn.metrics import roc_auc_score, f1_score, confusion_matrix
except ImportError:
    print("[!] scikit-learn not installed. Run: pip install scikit-learn")
    exit(1)


class BayesianModelTrainer:
    """Trains Naive Bayes model for PI exposure detection"""
    
    def __init__(self, output_dir: str = "./models"):
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        self.model = GaussianNB()
        self.scaler_stats = None
        self.metrics = {}
        
    def load_training_data_from_json(self, filepath: str = "data/synthetic_dataset.json") -> pd.DataFrame:
        """Load training data from JSON file"""
        
        if not os.path.exists(filepath):
            print(f"[!] Dataset not found: {filepath}")
            print("[!] Run: python database/generate_synthetic_data.py first")
            return pd.DataFrame()
        
        with open(filepath, 'r', encoding='utf-8') as f:
            dataset = json.load(f)
        
        # Extract paragraphs from memorials
        data = []
        for memorial in dataset['memorials']:
            for p in memorial['paragraphs']:
                data.append({
                    'entropy_normalized': p['stats'].get('entropy_normalized', 0),
                    'num_sensitive_patterns': 1 if p['has_exposure'] else 0,
                    'edital_type': 0,  # default to public
                    'section_technical': 1 if p['section'] == 'technical' else 0,
                    'has_exposure': int(p['has_exposure'])
                })
        
        df = pd.DataFrame(data)
        print(f"[✓] Loaded {len(df)} paragraphs from JSON")
        print(f"    Exposure: {df['has_exposure'].sum()} positive ({df['has_exposure'].mean()*100:.1f}%)")
        
        return df
    
    def load_training_data_from_db(self) -> pd.DataFrame:
        """Load training data from PostgreSQL database"""
        try:
            from database.models import SessionLocal, ParagraphAnnotated
            
            db = SessionLocal()
            paragraphs = db.query(ParagraphAnnotated).filter(
                ParagraphAnnotated.entropy_normalized.isnot(None)
            ).all()
            
            data = []
            for p in paragraphs:
                data.append({
                    'entropy_normalized': p.entropy_normalized,
                    'num_sensitive_patterns': p.num_sensitive_patterns or 0,
                    'edital_type': 1 if p.edital_type == 'confidential' else 0,
                    'section_technical': 1 if p.section_type == 'technical' else 0,
                    'has_exposure': int(p.has_exposure)
                })
            
            df = pd.DataFrame(data)
            print(f"[✓] Loaded {len(df)} paragraphs from database")
            print(f"    Exposure: {df['has_exposure'].sum()} positive ({df['has_exposure'].mean()*100:.1f}%)")
            
            return df
            
        except Exception as e:
            print(f"[!] Database connection failed: {e}")
            print("[*] Falling back to JSON data...")
            return self.load_training_data_from_json()
    
    def prepare_features(self, df: pd.DataFrame) -> tuple:
        """Prepare features X and target y"""
        
        feature_cols = [
            'entropy_normalized',
            'num_sensitive_patterns',
            'edital_type',
            'section_technical'
        ]
        
        X = df[feature_cols].values
        y = df['has_exposure'].values
        
        # Normalize features
        X_normalized = X.copy().astype(float)
        
        self.scaler_stats = {
            'means': X.mean(axis=0).tolist(),
            'stds': X.std(axis=0).tolist()
        }
        
        for i in range(X.shape[1]):
            if self.scaler_stats['stds'][i] > 0:
                X_normalized[:, i] = (X[:, i] - self.scaler_stats['means'][i]) / self.scaler_stats['stds'][i]
        
        return X_normalized, y, feature_cols
    
    def train(self, X: np.ndarray, y: np.ndarray):
        """Train the model"""
        self.model.fit(X, y)
        print("[✓] Model trained (Gaussian Naive Bayes)")
    
    def evaluate_kfold(self, X: np.ndarray, y: np.ndarray, k: int = 5) -> dict:
        """K-fold cross-validation"""
        print(f"\n[*] Evaluating with {k}-fold cross-validation...")
        
        skf = StratifiedKFold(n_splits=k, shuffle=True, random_state=42)
        
        scores_auc = []
        scores_f1 = []
        
        for fold, (train_idx, test_idx) in enumerate(skf.split(X, y)):
            X_train, X_test = X[train_idx], X[test_idx]
            y_train, y_test = y[train_idx], y[test_idx]
            
            model_fold = GaussianNB()
            model_fold.fit(X_train, y_train)
            
            y_pred = model_fold.predict(X_test)
            y_pred_proba = model_fold.predict_proba(X_test)[:, 1]
            
            auc = roc_auc_score(y_test, y_pred_proba)
            f1 = f1_score(y_test, y_pred, zero_division=0)
            
            scores_auc.append(auc)
            scores_f1.append(f1)
            
            print(f"  Fold {fold+1}: AUC={auc:.3f}, F1={f1:.3f}")
        
        return {
            'auc_mean': np.mean(scores_auc),
            'auc_std': np.std(scores_auc),
            'f1_mean': np.mean(scores_f1),
            'f1_std': np.std(scores_f1),
            'auc_scores': scores_auc,
            'ci_95_lower': np.mean(scores_auc) - 1.96 * np.std(scores_auc) / np.sqrt(k),
            'ci_95_upper': np.mean(scores_auc) + 1.96 * np.std(scores_auc) / np.sqrt(k)
        }
    
    def evaluate_full(self, X: np.ndarray, y: np.ndarray) -> dict:
        """Evaluate trained model on full dataset"""
        print(f"\n[*] Full dataset evaluation...")
        
        y_pred = self.model.predict(X)
        y_pred_proba = self.model.predict_proba(X)[:, 1]
        
        auc = roc_auc_score(y, y_pred_proba)
        f1 = f1_score(y, y_pred, zero_division=0)
        
        tn, fp, fn, tp = confusion_matrix(y, y_pred).ravel()
        
        metrics = {
            'auc': float(auc),
            'f1': float(f1),
            'true_positives': int(tp),
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn),
            'sensitivity': float(tp / (tp + fn)) if (tp + fn) > 0 else 0,
            'specificity': float(tn / (tn + fp)) if (tn + fp) > 0 else 0,
            'precision': float(tp / (tp + fp)) if (tp + fp) > 0 else 0,
            'accuracy': float((tp + tn) / (tp + tn + fp + fn))
        }
        
        print(f"  AUC: {auc:.3f}")
        print(f"  F1-Score: {f1:.3f}")
        print(f"  Accuracy: {metrics['accuracy']:.3f}")
        print(f"  Sensitivity: {metrics['sensitivity']:.3f}")
        print(f"  Specificity: {metrics['specificity']:.3f}")
        
        return metrics
    
    def save_model(self, model_path: str = None):
        """Save trained model"""
        if model_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            model_path = f"{self.output_dir}/bayesian_model_{timestamp}.pkl"
        
        with open(model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler_stats': self.scaler_stats,
                'metrics': self.metrics
            }, f)
        
        # Also save as "latest"
        latest_path = f"{self.output_dir}/bayesian_model_latest.pkl"
        with open(latest_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler_stats': self.scaler_stats,
                'metrics': self.metrics
            }, f)
        
        print(f"[✓] Model saved: {model_path}")
        print(f"[✓] Model saved: {latest_path}")
        return model_path
    
    def save_report(self, metrics: dict, kfold_metrics: dict, 
                   report_path: str = None):
        """Save validation report"""
        if report_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_path = f"{self.output_dir}/validation_report_{timestamp}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'full_evaluation': metrics,
            'cross_validation': {
                'k_folds': 5,
                'auc_mean': float(kfold_metrics['auc_mean']),
                'auc_std': float(kfold_metrics['auc_std']),
                'auc_ci_95': [float(kfold_metrics['ci_95_lower']), float(kfold_metrics['ci_95_upper'])],
                'f1_mean': float(kfold_metrics['f1_mean']),
                'f1_std': float(kfold_metrics['f1_std'])
            }
        }
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"[✓] Report saved: {report_path}")
        return report_path


# ============================================================================
# MAIN SCRIPT
# ============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("EditalShield: Bayesian Model Training")
    print("=" * 70)
    
    trainer = BayesianModelTrainer(output_dir="./models")
    
    # 1. Load data
    print("\n[1/4] Loading data...")
    df = trainer.load_training_data_from_json()
    
    if df.empty:
        print("[!] No data available. Exiting.")
        exit(1)
    
    # 2. Prepare features
    print("\n[2/4] Preparing features...")
    X, y, feature_cols = trainer.prepare_features(df)
    print(f"    Features: {feature_cols}")
    print(f"    Shape: X={X.shape}, y={y.shape}")
    
    # 3. Train model
    print("\n[3/4] Training model...")
    trainer.train(X, y)
    
    # 4. Evaluate
    print("\n[4/4] Evaluating model...")
    
    kfold_metrics = trainer.evaluate_kfold(X, y, k=5)
    full_metrics = trainer.evaluate_full(X, y)
    
    # 5. Save results
    print("\n[✓] Saving results...")
    trainer.metrics = full_metrics
    trainer.save_model()
    trainer.save_report(full_metrics, kfold_metrics)
    
    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)
    print(f"AUC (5-fold): {kfold_metrics['auc_mean']:.3f} ± {kfold_metrics['auc_std']:.3f}")
    print(f"CI 95%: [{kfold_metrics['ci_95_lower']:.3f}, {kfold_metrics['ci_95_upper']:.3f}]")
    print(f"F1-Score (5-fold): {kfold_metrics['f1_mean']:.3f} ± {kfold_metrics['f1_std']:.3f}")
    print("=" * 70)
