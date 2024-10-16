import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from .plots.plot_driver import SemanticSegmentationPlotDriver
from gesund_val_library.metrics.semantic_segmentation.segmentation_metric_plot import Semantic_Segmentation_Plot

class ValidationCreation:
    def __init__(self, batch_job_id, filter_field="image_url", generate_metrics=True):
        self.batch_job_id = batch_job_id
        self.filter_field = filter_field
        self.generate_metrics = generate_metrics

    def create_validation_collection_data(self, successful_batch_data, annotation_data, format=None):
        
        validation_collection_data = []
        
        for image_id in successful_batch_data:
            batch_item = successful_batch_data[image_id]
            annotation_item = annotation_data[image_id]
            image_information_dict = {}
            image_information_dict["batch_job_id"] = self.batch_job_id
            image_information_dict["image_id"] = batch_item["image_id"]
            image_information_dict["shape"] = [
                batch_item["shape"][0],
                batch_item["shape"][1],
            ]
            image_information_dict["meta_data"] = {},  # Placeholder for meta data if needed
            image_information_dict["ground_truth"] = annotation_item["annotation"]
            image_information_dict["objects"] = batch_item["masks"]
            image_information_dict["created_timestamp"] = time.time()
            validation_collection_data.append(image_information_dict)
            
        return validation_collection_data
    
    def load(self, validation_collection_data, class_mappings, study_list=None):

        generate_metrics = True
        
        #study_list = self.validation_cruds.get_study_list_by_batch_job_id(batch_job_id)
        #self.study_list = study_list
        self.study_list = []

        plotting_data = self._load_plotting_data(
            validation_collection_data=validation_collection_data,
            generate_metrics=generate_metrics,
            study_list=study_list,
        )

        # Create per image variables
        ground_truth_dict = plotting_data["per_image"]["ground_truth"]
        prediction_dict = plotting_data["per_image"]["prediction"]

        meta_data_dict = None

        try:
            meta_data_dict = plotting_data["per_image"]["meta_data"]
        except:
            print(
                "Meta Data not found.",
                )

        loss_dict = None

        try:
            loss_dict = plotting_data["per_image"]["loss"]
        except:
            print(
                "Loss not found.",
            )

        self.plot_driver = SemanticSegmentationPlotDriver(
            class_mappings=class_mappings,
            ground_truth_dict=ground_truth_dict,
            prediction_dict=prediction_dict,
            meta_data_dict=meta_data_dict,
            loss_dict=loss_dict,
            batch_job_id=self.batch_job_id,
            study_list=study_list,
        )
        
        overall_metrics = self.plot_driver._calling_all_plots()
        
        return overall_metrics

    def plot_metrics(self, metrics, output_dir, plot_configs):
        file_name_patterns = {
            'violin_graph': ('violin_path', 'plot_{}.json'),
            'plot_by_meta_data': ('plot_by_meta_data', 'plot_metrics_by_meta_data.json'),
            'overall_metrics': ('overall_data', 'plot_highlighted_{}.json'),
            'classbased_table': ('classed_table', 'plot_statistics_{}.json'),
            'blind_spot': ('blind_spot', 'plot_{}_metrics.json')
        }

        for draw_type, config in plot_configs.items():
            arg_name, file_pattern = file_name_patterns.get(draw_type, (None, 'plot_{}.json'))
            if arg_name is None:
                print(f"Warning: Unknown draw type '{draw_type}'. Skipping.")
                continue

            file_name = file_pattern.format(draw_type)
            file_path = os.path.join(output_dir, file_name)

            plot = Semantic_Segmentation_Plot(**{arg_name: file_path})

            save_path = os.path.join(output_dir, f'{draw_type}.png')
            
            if draw_type == 'violin_graph':
                plot.draw('violin_graph', metrics=config.get('metrics'), threshold=config.get('threshold'), save_path=save_path)
            elif draw_type == 'plot_by_meta_data':
                plot.draw('plot_by_meta_data', meta_data_args=config.get('meta_data_args'), save_path=save_path)
            elif draw_type == 'overall_metrics':
                plot.draw('overall_metrics', overall_args=config.get('overall_args'), save_path=save_path)
            elif draw_type == 'classbased_table':
                plot.draw('classbased_table', classbased_table_args=config.get('classbased_table_args'), save_path=save_path)
            elif draw_type == 'blind_spot':
                plot.draw('blind_spot', blind_spot_args=config.get('blind_spot_args'), save_path=save_path)



    def _load_plotting_data(
        self, validation_collection_data=None, generate_metrics=True, study_list=None,
    ):
        """
        Creates data for PlotValidation class(which gives payloads). Similar function in another class will be implemented for ModelValidation.

        :RaiseException: raises error if setup is not initialized.
        :return:  ground_truth_dict, logits_dict, meta_data_dict,loss_dict,img_source_dict
        """
        plotting_data = dict()
        plotting_data["per_image"] = self._craft_per_image_plotting_data(
            validation_collection_data, generate_metrics=generate_metrics, study_list=study_list
        )

        return plotting_data

    def _craft_per_image_plotting_data(
        self, validation_collection_data, generate_metrics, study_list=None
    ):
        """
        Creates data for PlotValidation class(which gives payloads). Similar function in another class will be implemented for ModelValidation.

        :RaiseException: raises error if setup is not initialized.
        :return:  ground_truth_dict, logits_dict, meta_data_dict,loss_dict,img_source_dict
        """
        data = dict()
        validation_df = pd.DataFrame(validation_collection_data)
        # Ground truth dict

        gt_dict = validation_df[["image_id", "ground_truth", "shape"]].values
        ground_truth_dict = {}
        for image_id, ground_truth_list, shape_list in gt_dict:
            shape = shape_list
            rle_dict = {"rles": []}
            if len(ground_truth_list) > 1:
                for item in ground_truth_list:
                    label = item["label"]
                    rle = {
                        "rle": item["mask"]["mask"], 
                        "shape": shape, 
                        "class": label
                    }
                    rle_dict["rles"].append(rle)
                ground_truth_dict[image_id] = rle_dict
                
            else:
                ground_truth = ground_truth_list[0]
                label = ground_truth["label"]
                rles_str = ground_truth["mask"]["mask"]
                rles = {
                    "rles": [{
                        "rle": rles_str, 
                        "shape": shape, 
                        "class": label
                    }]
                }
                ground_truth_dict[image_id] = rles

        # Prediction dict
        pred_dict = validation_df[["image_id", "objects", "shape"]].values
        prediction_dict = {}
        for image_id, objects, shape in pred_dict:
            rles = objects["rles"]
            for rle_dict in rles:
                rle_dict["shape"] = shape
            prediction_dict[image_id] = objects
        
        # Loss dict
        if generate_metrics:
            try:
                loss_dict = (
                    validation_df[["image_id", "loss"]]
                    .set_index("image_id")
                    .to_dict()["loss"]
                )
            except:
                pass

        # Meta Data dict
        try:
            meta_data_dict = validation_df[["image_id", "meta_data"]].values
            meta_data_dict = dict(zip(meta_data_dict[:, 0], meta_data_dict[:, 1]))
        except:
            pass
        # Image Sources dict

        data["ground_truth"] = ground_truth_dict
        data["prediction"] = prediction_dict
        
        try:
            data["meta_data"] = meta_data_dict
        except:
            pass
        if generate_metrics:
            try:
                data["loss"] = loss_dict
            except:
                pass
        return data