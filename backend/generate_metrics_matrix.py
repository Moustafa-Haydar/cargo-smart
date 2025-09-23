#!/usr/bin/env python
"""
Generate a metrics matrix visualization similar to confusion matrix
but showing accuracy, precision, recall, and F1-score values.
"""

import os
import sys
import django

# Setup Django
sys.path.append('/app')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cargosmart.settings')
django.setup()

from apps.shipments.management.commands.ml_visualizations import MLVisualizer

def main():
    # Create visualizer
    models_dir = os.path.join(os.getcwd(), "models")
    visualizer = MLVisualizer(os.path.join(models_dir, "plots"))
    
    # Your reported metrics from the test run
    accuracy = 0.750
    precision = 0.860  # From classification report: 0.86 for class 1
    recall = 0.740     # From classification report: 0.74 for class 1  
    f1 = 0.797         # From classification report: 0.80 for class 1
    
    print(f"Generating metrics matrix with:")
    print(f"  Accuracy: {accuracy:.3f}")
    print(f"  Precision: {precision:.3f}")
    print(f"  Recall: {recall:.3f}")
    print(f"  F1-score: {f1:.3f}")
    
    # Generate the metrics matrix
    visualizer.plot_metrics_matrix(
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        f1=f1,
        filename="metrics_matrix.png"
    )
    
    output_path = os.path.join(models_dir, "plots", "metrics_matrix.png")
    print(f"Metrics matrix saved to: {output_path}")

if __name__ == "__main__":
    main()
