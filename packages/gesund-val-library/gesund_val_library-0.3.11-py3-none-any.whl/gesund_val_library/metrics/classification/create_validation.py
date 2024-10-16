import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

from .plots.plot_driver import ClassificationPlotDriver
from gesund_val_library.metrics.classification.classification_metric_plot import Classification_Plot

class ValidationCreation:
    def __init__(self, batch_job_id, filter_field="image_url", generate_metrics=True):
        self.batch_job_id = batch_job_id
        self.filter_field = filter_field
        self.generate_metrics = generate_metrics

    def create_validation_collection_data(self, successful_batch_data, annotation_data, format=None):
        """
        Create validation collection data from JSON files.
        
        Args:
        successful_batch_data_file (str): Path to the JSON file with prediction data.
        annotation_data_file (str): Path to the JSON file with annotation data.
        
        Returns:
        list: List of dictionaries with validation collection data.
        """

        validation_collection_data = []

        for item_id in successful_batch_data:
            if item_id not in annotation_data:
                raise ValueError(f"Annotation data for item ID {item_id} is missing")

            batch_item = successful_batch_data[item_id]
            annotation_item = annotation_data[item_id]

            information_dict = {
                "batch_job_id": self.batch_job_id,
                "image_id": batch_item["image_id"],
                "confidence": batch_item["confidence"],
                "logits": batch_item["logits"],
                "prediction_class": batch_item["prediction_class"],
                "loss": batch_item["loss"],
                "ground_truth": annotation_item["annotation"][0]["label"],
                "meta_data": {},  # Placeholder for meta data if needed
                "created_timestamp": time.time()
            }

            validation_collection_data.append(information_dict)            

        return validation_collection_data
    
    def load(self, validation_collection_data, class_mappings):

        generate_metrics = True
        plotting_data = self._load_plotting_data(validation_collection_data)

        # Create per image variables
        ground_truth_dict = plotting_data["per_image"]["ground_truth"]
        meta_data_dict = plotting_data["per_image"]["meta_data"]
        logits_dict = plotting_data["per_image"]["logits"]
        if generate_metrics:
            loss_dict = plotting_data["per_image"]["loss"]

        # Create validation variables
        true = pd.DataFrame(ground_truth_dict, index=[0]).loc[0].astype(int)
        class_mappings = class_mappings
        pred = pd.DataFrame(logits_dict)
        meta = pd.DataFrame(meta_data_dict).T

        loss = None
        if generate_metrics:
            loss = pd.DataFrame(loss_dict, index=[0])
        sample_size = len(true)
        class_order = list(range(len(class_mappings.keys())))
        true.name = "true"
        pred.name = "pred"
        # Check, add breakpoint
        if np.shape(pred.shape)[0] == 1:
            pred_categorical = pred
            pred_categorical.name = "pred_categorical"
            pred_categorical = pred_categorical.astype(int)
        else:
            pred_logits = pred
            pred_categorical = pred.idxmax()
            pred_categorical.name = "pred_categorical"
        meta_pred_true = pd.concat([meta, pred_categorical, true], axis=1)

        self.plot_driver = ClassificationPlotDriver(
            true=true,
            pred=pred,
            meta=meta,
            pred_categorical=pred_categorical,
            pred_logits=pred_logits,
            meta_pred_true=meta_pred_true,
            class_mappings=class_mappings,
            loss=loss,
        )
        
        overall_metrics = self.plot_driver._calling_all_plots()
        
        return overall_metrics
    
    def plot_metrics(self, metrics, output_dir, plot_configs):
        file_name_patterns = {
            'class_distributions': ('class_distributions_path', 'plot_{}.json'),
            'blind_spot': ('blind_spot_path', 'plot_{}_metrics.json'),
            'performance_by_threshold': ('performance_threshold_path', 'plot_class_{}.json'),
            'roc': ('roc_statistics_path', 'plot_{}_multiclass_statistics.json'),
            'precision_recall': ('precision_recall_statistics_path', 'plot_{}_multiclass_statistics.json'),
            'confidence_histogram': ('confidence_histogram_path', 'plot_{}_scatter_distribution.json'),
            'overall_metrics': ('overall_json_path', 'plot_highlighted_{}.json')
        }

        for draw_type, config in plot_configs.items():
            arg_name, file_pattern = file_name_patterns.get(draw_type, (None, 'plot_{}.json'))
            if arg_name is None:
                print(f"Warning: Unknown draw type '{draw_type}'. Skipping.")
                continue

            file_name = file_pattern.format(draw_type)
            file_path = os.path.join(output_dir, file_name)

            plot = Classification_Plot(**{arg_name: file_path})

            save_path = os.path.join(output_dir, f'{draw_type}.png')
            
            if draw_type == 'class_distributions':
                plot.draw('class_distributions', metrics=config.get('metrics'), threshold=config.get('threshold'), save_path=save_path)
            elif draw_type == 'blind_spot':
                plot.draw('blind_spot', class_type=config.get('class_type'), save_path=save_path)
            elif draw_type == 'performance_by_threshold':
                plot.draw('performance_by_threshold', graph_type=config.get('graph_type'), metrics=config.get('metrics'), threshold=config.get('threshold'), save_path=save_path)
            elif draw_type == 'roc':
                plot.draw('roc', roc_class=config.get('roc_class'), save_path=save_path)
            elif draw_type == 'precision_recall':
                plot.draw('precision_recall', pr_class=config.get('pr_class'), save_path=save_path)
            elif draw_type == 'confidence_histogram':
                plot.draw('confidence_histogram', metrics=config.get('metrics'), threshold=config.get('threshold'), save_path=save_path)
            elif draw_type == 'overall_metrics':
                plot.draw('overall_metrics', metrics=config.get('metrics'), save_path=save_path)


    def _load_plotting_data(
        self, validation_collection_data
    ):
        plotting_data = dict()
        plotting_data["per_image"] = self._craft_per_image_plotting_data(
            validation_collection_data
        )
        return plotting_data

    def _craft_per_image_plotting_data(
        self, validation_collection_data
    ):
        data = dict()
        validation_df = pd.DataFrame(validation_collection_data)
        # Ground truth dict
        ground_truth_dict = validation_df[["image_id", "ground_truth"]].values
        ground_truth_dict = dict(zip(ground_truth_dict[:, 0], ground_truth_dict[:, 1]))
        # Loss dict
        loss_dict = (
            validation_df[["image_id", "loss"]]
            .set_index("image_id")
            .to_dict()["loss"]
        )

        # Meta Data dict
        meta_data_dict = validation_df[["image_id", "meta_data"]].values
        meta_data_dict = dict(zip(meta_data_dict[:, 0], meta_data_dict[:, 1]))
        # Logits dict
        logits_dict = validation_df[["image_id", "logits"]].values
        logits_dict = dict(zip(logits_dict[:, 0], logits_dict[:, 1]))

        data["ground_truth"] = ground_truth_dict
        data["meta_data"] = meta_data_dict
        data["logits"] = logits_dict
        data["loss"] = loss_dict

        return data