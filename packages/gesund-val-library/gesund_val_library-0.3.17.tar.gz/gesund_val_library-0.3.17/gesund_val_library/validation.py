import json
import bson
import os
from pathlib import Path
from gesund_val_library.utils.io_utils import read_json, save_plot_metrics_as_json, format_metrics
from gesund_val_library.utils.yolo_converter import YOLOConverter
from gesund_val_library.utils.coco_converter import COCOConverter
from gesund_val_library.problem_type_factory import get_validation_creation

def run_metrics(args):
    """Run validation metrics based on the passed arguments."""
    try:
        successful_batch_data = read_json(args['predictions'])
        annotation_data = read_json(args['annotations_json_path'])
        class_mappings = read_json(args['class_mappings'])
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading input files: {e}")
        return None
    
    try:
        meta_data = read_json(args['metadata'])
    except:
        print("Metadata file not provided!")
        meta_data = None

    batch_job_id = str(bson.ObjectId())
    output_dir = os.path.join("outputs", batch_job_id)
    json_outputs_dir = os.path.join(output_dir, "plot_jsons")

    if args['format'] == 'coco':
        converter_annot = COCOConverter(annotations=annotation_data, problem_type=args['problem_type'])
        converter_pred = COCOConverter(successful_batch_data=successful_batch_data, problem_type=args['problem_type'])
        annotation_data = converter_annot.convert_annot_if_needed()
        successful_batch_data = converter_pred.convert_pred_if_needed()

    elif args['format'] == 'yolo':
        yolo_converter = YOLOConverter(annotations=annotation_data, successful_batch_data=successful_batch_data)
        annotation_data = yolo_converter.convert_annot_if_needed()
        successful_batch_data = yolo_converter.convert_pred_if_needed()

    elif args['format'] == 'gesund_custom_format':
        pass

    ValidationCreationClass = get_validation_creation(args['problem_type'])
    validation = ValidationCreationClass(batch_job_id)

    try:
        validation_data = validation.create_validation_collection_data(successful_batch_data, annotation_data, args['format'])
        metrics = validation.load(validation_data, class_mappings)
    except Exception as e:
        print(f"Error calculating metrics: {e}")
        return None

    if args.get('write_results_to_json', False):
        save_plot_metrics_as_json(metrics, json_outputs_dir)

    metrics.update({
        "problem_type": args['problem_type'],
        "batch_job_id": batch_job_id,
        "successful_batch_data": successful_batch_data,
        "annotation_data": annotation_data,
        "meta_data": meta_data,
        "class_mappings": class_mappings,
        "format": args['format'],
        "output_dir": output_dir
    })

    return metrics

def plotting_metrics(metrics, filtering_meta=None):
    """Plot the validation metrics using the stored validation instance."""
    ValidationCreationClass = get_validation_creation(metrics['problem_type'])
    validation = ValidationCreationClass(metrics["batch_job_id"])

    output_dir = metrics["output_dir"]
    json_outputs_dir = os.path.join(output_dir, "plot_jsons")

    if filtering_meta:
        meta_data = read_json(filtering_meta['metadata_file'])
        meta_filtered_validation_data = validation.create_validation_collection_data(
            metrics['successful_batch_data'], 
            metrics['annotation_data'], 
            metrics['format'], 
            meta_data
        )
        meta_filtered_metrics = validation.load(meta_filtered_validation_data, metrics['class_mappings'], filtering_meta['filter_meta'])
        filtered_jsons_outputs_dir = os.path.join(output_dir, "filtered_plot_jsons")
        Path(filtered_jsons_outputs_dir).mkdir(parents=True, exist_ok=True)
        save_plot_metrics_as_json(meta_filtered_metrics, filtered_jsons_outputs_dir)
        
        filtered_plot_outputs_dir = os.path.join(output_dir, "filtered_plots")
        Path(filtered_plot_outputs_dir).mkdir(parents=True, exist_ok=True)
        validation.plot_metrics(meta_filtered_metrics, filtered_jsons_outputs_dir, filtered_plot_outputs_dir)

    else:
        plot_outputs_dir = os.path.join(output_dir, "plots")
        Path(plot_outputs_dir).mkdir(parents=True, exist_ok=True)
        validation.plot_metrics(metrics, json_outputs_dir, plot_outputs_dir)
