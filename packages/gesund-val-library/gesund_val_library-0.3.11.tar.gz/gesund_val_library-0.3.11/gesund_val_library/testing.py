from gesund_val_library.validation import run_metrics

args = {
    'annotations_json_path': '/home/ozkan/gesund_val_library/test_data/semantic_segmentation/coco/coco_annotations_sem_segm.json',
    'predictions': '/home/ozkan/gesund_val_library/test_data/semantic_segmentation/coco/coco_predictions_sem_segm.json',
    'class_mappings': '/home/ozkan/gesund_val_library/test_data/semantic_segmentation/test_class_mappings.json',
    'problem_type': 'semantic_segmentation',
    'format': 'coco',
    'write_results_to_json': True,

    # 'plot_configs': {
    #     'class_distributions': {'metrics': ['normal'], 'threshold': 10},
    #     'blind_spot': {'class_type': 'Average'},
    #     'performance_by_threshold': {'graph_type': 'graph_1', 'metrics': ['F1', 'Sensitivity', 'Specificity', 'Precision'], 'threshold': 0.2},
    #     'roc': {'roc_class': 'normal'},
    #     'precision_recall': {'pr_class': 'normal'},
    #     'confidence_histogram': {'metrics': ['TP', 'FP'], 'threshold': 0.5},
    #     'overall_metrics': {'metrics': ['mean AUC', 'fwIoU']}


    # 'plot_configs': {
    #         'mixed_plot': {'mixed_plot': ['map10', 'map50', 'map75'], 'threshold': 0.5},
    #         'top_misses': {'min_miou': 0.80, 'top_n': 5},
    #         'confidence_histogram': {'confidence_histogram_labels': ['TP', 'FP']},
    #         'classbased_table': {'classbased_table_metrics': ['precision', 'recall', 'f1'], 'threshold': 0.5},
    #         'overall_metrics': {'overall_metrics_metrics': ['map', 'mar'], 'threshold': 0.5},
    #         'blind_spot': {'blind_spot_Average': ['mAP@50', 'mAP@75'],'threshold': 0.6}

    'plot_configs': {
    
        'violin_graph': {'metrics':['Acc', 'Spec'], 'threshold': 0.5},
        'plot_by_meta_data': {'meta_data_args': ['TruePositive', 'TrueNegative']},
        'overall_metrics': {'overall_args': ['mean AUC', 'fwIoU']},
        'classbased_table': {'classbased_table_args': 0.5},
        'blind_spot': {'blind_spot_args': ['fwIoU']},
        }
}

result = run_metrics(args)


