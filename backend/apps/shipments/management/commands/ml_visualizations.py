"""
Machine Learning Visualization Utilities for CargoSmart Delay Prediction Model
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    roc_curve, precision_recall_curve, confusion_matrix,
    classification_report, roc_auc_score, average_precision_score
)
from sklearn.calibration import calibration_curve
import joblib
from typing import Tuple, List, Optional

# Set style for better-looking plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class MLVisualizer:
    """Class to create comprehensive ML model visualizations"""
    
    def __init__(self, output_dir: str = "models/plots"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def plot_data_distribution(self, df: pd.DataFrame, target_col: str = "delayed_flag") -> None:
        """Plot data distribution and feature analysis. Safe if target missing."""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('CargoSmart Data Distribution Analysis', fontsize=16, fontweight='bold')
        
        # 1. Target distribution
        ax1 = axes[0, 0]
        if target_col in df.columns:
            target_counts = df[target_col].value_counts()
            labels = []
            values = []
            # Map 0->On Time, 1->Delayed if numeric
            for k, v in target_counts.items():
                if k in [0, 1]:
                    labels.append('Delayed' if k == 1 else 'On Time')
                else:
                    labels.append(str(k))
                values.append(v)
            if values:
                ax1.pie(values, labels=labels, autopct='%1.1f%%', 
                        colors=['lightgreen', 'lightcoral'])
                ax1.set_title('Delay Distribution')
        else:
            ax1.text(0.5, 0.5, f"Target '{target_col}' not found", ha='center', va='center')
            ax1.set_title('Delay Distribution')
        
        # 2. Distance distribution
        ax2 = axes[0, 1]
        if 'haversine_km' in df.columns:
            ax2.hist(df['haversine_km'].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
            ax2.set_xlabel('Distance (km)')
            ax2.set_ylabel('Frequency')
            ax2.set_title('Delivery Distance Distribution')
            ax2.axvline(df['haversine_km'].mean(), color='red', linestyle='--', 
                       label=f'Mean: {df["haversine_km"].mean():.1f}km')
            ax2.legend()
        
        # 3. Planned hour distribution
        ax3 = axes[0, 2]
        if 'planned_hour' in df.columns:
            hour_counts = df['planned_hour'].value_counts().sort_index()
            ax3.bar(hour_counts.index, hour_counts.values, color='lightblue', edgecolor='black')
            ax3.set_xlabel('Hour of Day')
            ax3.set_ylabel('Number of Deliveries')
            ax3.set_title('Delivery Time Distribution')
            ax3.set_xticks(range(0, 24, 2))
        
        # 4. Weekend vs Weekday
        ax4 = axes[1, 0]
        if 'is_weekend' in df.columns:
            weekend_delay = df.groupby('is_weekend')[target_col].mean()
            bars = ax4.bar(['Weekday', 'Weekend'], weekend_delay.values, 
                          color=['lightblue', 'lightcoral'], edgecolor='black')
            ax4.set_ylabel('Delay Rate')
            ax4.set_title('Delay Rate: Weekend vs Weekday')
            ax4.set_ylim(0, 1)
            
            # Add percentage labels on bars
            for bar, rate in zip(bars, weekend_delay.values):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{rate:.1%}', ha='center', va='bottom')
        
        # 5. Weather impact
        ax5 = axes[1, 1]
        if 'rain_flag' in df.columns:
            weather_delay = df.groupby('rain_flag')[target_col].mean()
            bars = ax5.bar(['No Rain', 'Rain'], weather_delay.values,
                          color=['lightgreen', 'lightblue'], edgecolor='black')
            ax5.set_ylabel('Delay Rate')
            ax5.set_title('Delay Rate: Weather Impact')
            ax5.set_ylim(0, 1)
            
            for bar, rate in zip(bars, weather_delay.values):
                height = bar.get_height()
                ax5.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{rate:.1%}', ha='center', va='bottom')
        
        # 6. Lead time vs delay rate
        ax6 = axes[1, 2]
        if 'lead_time_hours' in df.columns:
            # Create bins for lead time
            df['lead_time_bin'] = pd.cut(df['lead_time_hours'], bins=5)
            lead_delay = df.groupby('lead_time_bin')[target_col].mean()
            
            bin_labels = [f'{interval.left:.0f}-{interval.right:.0f}h' 
                         for interval in lead_delay.index]
            ax6.bar(range(len(bin_labels)), lead_delay.values, 
                   color='lightsteelblue', edgecolor='black')
            ax6.set_xticks(range(len(bin_labels)))
            ax6.set_xticklabels(bin_labels, rotation=45)
            ax6.set_ylabel('Delay Rate')
            ax6.set_title('Delay Rate by Lead Time')
            ax6.set_ylim(0, 1)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'data_distribution.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_model_performance(self, y_true: np.ndarray, y_proba: np.ndarray, 
                             y_pred: np.ndarray) -> None:
        """Plot comprehensive model performance metrics"""
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('CargoSmart Delay Prediction Model Performance', fontsize=16, fontweight='bold')
        
        # 1. ROC Curve
        ax1 = axes[0, 0]
        fpr, tpr, _ = roc_curve(y_true, y_proba)
        roc_auc = roc_auc_score(y_true, y_proba)
        
        ax1.plot(fpr, tpr, color='darkorange', lw=2, 
                label=f'ROC Curve (AUC = {roc_auc:.3f})')
        ax1.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', alpha=0.5)
        ax1.set_xlim([0.0, 1.0])
        ax1.set_ylim([0.0, 1.05])
        ax1.set_xlabel('False Positive Rate')
        ax1.set_ylabel('True Positive Rate')
        ax1.set_title('ROC Curve')
        ax1.legend(loc="lower right")
        ax1.grid(True, alpha=0.3)
        
        # 2. Precision-Recall Curve
        ax2 = axes[0, 1]
        precision, recall, _ = precision_recall_curve(y_true, y_proba)
        pr_auc = average_precision_score(y_true, y_proba)
        
        ax2.plot(recall, precision, color='blue', lw=2,
                label=f'PR Curve (AUC = {pr_auc:.3f})')
        ax2.set_xlim([0.0, 1.0])
        ax2.set_ylim([0.0, 1.05])
        ax2.set_xlabel('Recall')
        ax2.set_ylabel('Precision')
        ax2.set_title('Precision-Recall Curve')
        ax2.legend(loc="lower left")
        ax2.grid(True, alpha=0.3)
        
        # 3. Confusion Matrix (styled like example)
        ax3 = axes[0, 2]
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax3,
                    cbar=True, square=True,
                    xticklabels=['false', 'true'],
                    yticklabels=['false', 'true'])
        ax3.set_title('Confusion Matrix')
        ax3.set_xlabel('Predicted Label')
        ax3.set_ylabel('True Label')
        
        # 4. Probability Distribution
        ax4 = axes[1, 0]
        delayed_probs = y_proba[y_true == 1]
        ontime_probs = y_proba[y_true == 0]
        
        ax4.hist(ontime_probs, bins=30, alpha=0.7, label='On Time', 
                color='lightgreen', density=True)
        ax4.hist(delayed_probs, bins=30, alpha=0.7, label='Delayed', 
                color='lightcoral', density=True)
        ax4.axvline(0.5, color='black', linestyle='--', alpha=0.7, label='Threshold')
        ax4.set_xlabel('Predicted Probability')
        ax4.set_ylabel('Density')
        ax4.set_title('Probability Distribution')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. Calibration Plot
        ax5 = axes[1, 1]
        fraction_of_positives, mean_predicted_value = calibration_curve(
            y_true, y_proba, n_bins=10)
        
        ax5.plot(mean_predicted_value, fraction_of_positives, "s-",
                label="Model", color='red')
        ax5.plot([0, 1], [0, 1], "k:", label="Perfectly calibrated")
        ax5.set_xlabel('Mean Predicted Probability')
        ax5.set_ylabel('Fraction of Positives')
        ax5.set_title('Calibration Plot')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        
        # 6. Feature Importance (if available)
        ax6 = axes[1, 2]
        # This would need the model to have feature_importances_ or coef_
        # For now, show a placeholder
        ax6.text(0.5, 0.5, 'Feature Importance\n(Requires model with\nfeature_importances_)', 
                ha='center', va='center', transform=ax6.transAxes, fontsize=12)
        ax6.set_title('Feature Importance')
        ax6.axis('off')
        
        plt.tight_layout()
        # Save main performance panel
        plt.savefig(os.path.join(self.output_dir, 'model_performance.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()

        # Also save confusion matrix as a standalone figure like the example
        fig_cm, ax_cm = plt.subplots(1, 1, figsize=(6, 5))
        cm = confusion_matrix(y_true, y_pred)
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax_cm,
                    cbar=True, square=True,
                    xticklabels=['false', 'true'],
                    yticklabels=['false', 'true'])
        ax_cm.set_title('Confusion Matrix')
        ax_cm.set_xlabel('Predicted Label')
        ax_cm.set_ylabel('True Label')
        plt.tight_layout()
        fig_cm.savefig(os.path.join(self.output_dir, 'confusion_matrix.png'), dpi=300, bbox_inches='tight')
        plt.close(fig_cm)

    def plot_metrics_matrix(self, accuracy: float, precision: float, recall: float, f1: float,
                            filename: str = 'metrics_matrix.png') -> None:
        """Create a 2x2 heatmap styled like a confusion matrix but showing key metrics.

        Layout:
            [ [Accuracy, Precision],
              [Recall,   F1-score ] ]
        """
        data = np.array([[accuracy, precision], [recall, f1]])

        fig, ax = plt.subplots(1, 1, figsize=(6, 5))
        sns.heatmap(
            data,
            annot=False,
            cmap='Blues',
            cbar=True,
            square=True,
            xticklabels=['Accuracy', 'Precision'],
            yticklabels=['Recall', 'F1-score'],
            ax=ax
        )

        # Overlay metric labels with values
        labels = [[f"Acc\n{accuracy:.3f}", f"Prec\n{precision:.3f}"],
                  [f"Rec\n{recall:.3f}",  f"F1\n{f1:.3f}"]]
        for i in range(2):
            for j in range(2):
                ax.text(j + 0.5, i + 0.5, labels[i][j],
                        ha='center', va='center', color='black', fontsize=12)

        ax.set_title('Model Metrics Overview')
        ax.set_xlabel('')
        ax.set_ylabel('')
        plt.tight_layout()
        fig.savefig(os.path.join(self.output_dir, filename), dpi=300, bbox_inches='tight')
        plt.close(fig)
        
    def plot_feature_analysis(self, X: pd.DataFrame, y: pd.Series, 
                            feature_names: List[str]) -> None:
        """Plot feature analysis and correlations"""
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Feature Analysis for Delay Prediction', fontsize=16, fontweight='bold')
        
        # 1. Correlation Heatmap
        ax1 = axes[0, 0]
        # Select only numeric features for correlation
        numeric_features = X.select_dtypes(include=[np.number]).columns
        if len(numeric_features) > 0:
            corr_data = X[numeric_features].copy()
            corr_data['target'] = y
            correlation_matrix = corr_data.corr()
            
            mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
            sns.heatmap(correlation_matrix, mask=mask, annot=True, cmap='coolwarm', 
                       center=0, square=True, ax=ax1, fmt='.2f')
            ax1.set_title('Feature Correlation Matrix')
        
        # 2. Feature vs Target (for top numeric features)
        ax2 = axes[0, 1]
        if len(numeric_features) > 0:
            # Select top 4 most correlated features with target
            target_corr = X[numeric_features].corrwith(y).abs().sort_values(ascending=False)
            top_features = target_corr.head(4).index
            
            for i, feature in enumerate(top_features):
                if i < 4:  # Limit to 4 features
                    ax2.scatter(X[feature], y, alpha=0.6, label=feature, s=20)
            
            ax2.set_xlabel('Feature Value')
            ax2.set_ylabel('Delay (0=On Time, 1=Delayed)')
            ax2.set_title('Top Features vs Target')
            ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
            ax2.grid(True, alpha=0.3)
        
        # 3. Box plots for categorical features
        ax3 = axes[1, 0]
        categorical_features = X.select_dtypes(include=['object', 'category']).columns
        if len(categorical_features) > 0:
            # Take first categorical feature for box plot
            cat_feature = categorical_features[0]
            sns.boxplot(data=X, x=cat_feature, y=y, ax=ax3)
            ax3.set_title(f'Delay Distribution by {cat_feature}')
            ax3.tick_params(axis='x', rotation=45)
        else:
            ax3.text(0.5, 0.5, 'No categorical features\navailable for analysis', 
                    ha='center', va='center', transform=ax3.transAxes)
            ax3.set_title('Categorical Feature Analysis')
        
        # 4. Feature importance (placeholder)
        ax4 = axes[1, 1]
        ax4.text(0.5, 0.5, 'Feature Importance Analysis\n(Requires trained model\nwith feature_importances_)', 
                ha='center', va='center', transform=ax4.transAxes, fontsize=12)
        ax4.set_title('Feature Importance')
        ax4.axis('off')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'feature_analysis.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_training_history(self, train_scores: List[float], 
                            test_scores: List[float], 
                            metric_name: str = "Score") -> None:
        """Plot training history (if using iterative training)"""
        fig, ax = plt.subplots(1, 1, figsize=(10, 6))
        
        epochs = range(1, len(train_scores) + 1)
        ax.plot(epochs, train_scores, 'b-', label=f'Training {metric_name}')
        ax.plot(epochs, test_scores, 'r-', label=f'Validation {metric_name}')
        
        ax.set_xlabel('Epoch')
        ax.set_ylabel(metric_name)
        ax.set_title(f'Training History - {metric_name}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'training_history.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_summary_report(self, model, X_test: pd.DataFrame, y_test: pd.Series, 
                            y_pred: np.ndarray, y_proba: np.ndarray) -> None:
        """Create a comprehensive summary report"""
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        ax.axis('off')
        
        # Calculate metrics
        roc_auc = roc_auc_score(y_test, y_proba)
        pr_auc = average_precision_score(y_test, y_proba)
        
        # Create summary text
        summary_text = f"""
CARGO SMART DELAY PREDICTION MODEL - SUMMARY REPORT

Model Performance Metrics:
• ROC-AUC Score: {roc_auc:.3f}
• Precision-Recall AUC: {pr_auc:.3f}
• Test Set Size: {len(y_test)} samples
• Positive Class Rate: {y_test.mean():.1%}

Model Details:
• Algorithm: {type(model).__name__}
• Features Used: {X_test.shape[1]}
• Training Date: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

Data Insights:
• Total Delays: {y_test.sum()} ({y_test.mean():.1%})
• On-Time Deliveries: {(y_test == 0).sum()} ({(1-y_test.mean()):.1%})

Model Interpretation:
• Higher ROC-AUC indicates better discrimination between delayed and on-time deliveries
• Precision-Recall AUC is important for imbalanced datasets
• Model can be used for proactive delay prevention and route optimization

Next Steps:
• Monitor model performance on new data
• Retrain periodically with fresh data
• Consider ensemble methods for improved accuracy
• Implement real-time prediction pipeline
        """
        
        ax.text(0.05, 0.95, summary_text, transform=ax.transAxes, fontsize=11,
               verticalalignment='top', fontfamily='monospace',
               bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8))
        
        plt.title('CargoSmart ML Model Summary Report', fontsize=16, fontweight='bold', pad=20)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'summary_report.png'), 
                   dpi=300, bbox_inches='tight')
        plt.close()
