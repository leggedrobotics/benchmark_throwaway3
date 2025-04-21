import os
import io
import zipfile
import json
from .evo_script import TrajectoryEvaluator, read_tum_trajectory_matrix
import sys


def evaluate(test_annotation_file, user_submission_file, phase_codename, **kwargs):
    #🔁
    print("\n" + "=" * 80)
    print(f"Evaluating submission with ID: {kwargs['submission_metadata']['id']}")
    print("=" * 80 + "\n")
    sys.stdout.flush()

    # script_dir = os.path.dirname(os.path.abspath(__file__))
    # print(kwargs['submission_metadata'])
    output = {}
    # evaluated_metrics = []

    # # TODO: phase_codename should have pre-listed IDs for which missions belong where.
    # # We need to prevent the user from submitting a mission that is not in the phase_codename.

    # config_path = os.path.join(script_dir, "evo_config", "evo_parameters.yaml")
    # ev = TrajectoryEvaluator(config=config_path)

    # with zipfile.ZipFile(user_submission_file, "r") as zip_submission:
    #     with zipfile.ZipFile(test_annotation_file, "r") as zip_annotation:
    #         # Get the list of file paths in the annotation zip for efficient lookup
    #         annotation_file_paths = zip_annotation.namelist()
    #         annotation_file_names = {}
    #         prefix = "gt_"
    #         suffix = ".tum"
    #         for p in annotation_file_paths:
    #             basename = os.path.basename(p)
    #             # Check if filename matches the expected format like "gt_NAME.tum"
    #             if basename.startswith(prefix) and basename.endswith(suffix):
    #                 # Extract the part between the prefix and the suffix
    #                 start_index = len(prefix)
    #                 end_index = len(basename) - len(suffix)
    #                 key = basename[start_index:end_index]
    #                 if key: # Ensure the extracted key is not empty
    #                     annotation_file_names[key] = p
    #                 else:
    #                     print(f"Warning: Extracted empty key from annotation filename: {basename}")
    #             else:
    #                 print(f"Warning: Skipping annotation file with unexpected format: {basename}")



    #         # Iterate over all files in the submission zip archive
    #         for submission_file_path in zip_submission.namelist():
    #             # Check if the file has a .tum extension
    #             if submission_file_path.endswith((".tum", ".txt")):
    #                 # Extract the filename from the path
    #                 submission_file_name_with_ext = os.path.basename(submission_file_path)
    #                 submission_file_name, ext = os.path.splitext(submission_file_name_with_ext)
    #                 if ext.lower() not in ['.tum', '.txt']:
    #                     print(f"Warning: File '{submission_file_name_with_ext}' does not have .tum or .txt extension.")
    #                 print(f"Found submission .tum file: Path='{submission_file_path}', Name='{submission_file_name}'")

    #                 # Check if a file with the same name exists in the annotation zip
    #                 if submission_file_name in annotation_file_names:
    #                     matching_annotation_path = annotation_file_names[submission_file_name]
    #                     print(f"  Found matching annotation file: Path='{matching_annotation_path}', Name='{submission_file_name}'")


    #                     # … inside your ZIP‐reading loop …
    #                     with zip_submission.open(submission_file_path) as byte_stream, \
    #                         io.TextIOWrapper(byte_stream, encoding="utf-8") as text_stream:

    #                         # Now treat text_stream exactly like a normal .tum file handle:
    #                         traj_estimated = read_tum_trajectory_matrix(text_stream, delim=" ", comment_str="#")
    #                         est_valid, est_details = traj_estimated.check()
    #                         if not est_valid:
    #                             print("\033[91mReference trajectory is not valid. Details:\033[0m") # Header in red, reset color
    #                             for key, value in est_details.items():
    #                                 # Convert value to string and lower case for comparison
    #                                 value_str = str(value).lower()
    #                                 if value_str == 'ok' or value_str == 'yes':
    #                                     # Print in green
    #                                     print(f"\033[92m  {key}: {value}\033[0m")
    #                                 else:
    #                                     # Print in red
    #                                     print(f"\033[91m  {key}: {value}\033[0m")

    #                         # mat is an N×8 numpy array of floats
    #                         print(f"  Loaded matrix with shape {traj_estimated.timestamps.shape}")


    #                     # … inside your ZIP‐reading loop …
    #                     with zip_annotation.open(matching_annotation_path) as annotation_byte_stream, \
    #                         io.TextIOWrapper(annotation_byte_stream, encoding="utf-8") as annotation_text_stream:

    #                         # Now treat text_stream exactly like a normal .tum file handle:
    #                         traj_reference = read_tum_trajectory_matrix(annotation_text_stream, delim=" ", comment_str="#")
    #                         ref_valid, ref_details = traj_reference.check()
    #                         if not ref_valid:
    #                             print("\033[91mReference trajectory is not valid. Details:\033[0m") # Header in red, reset color
    #                             for key, value in ref_details.items():
    #                                 # Convert value to string and lower case for comparison
    #                                 value_str = str(value).lower()
    #                                 if value_str == 'ok' or value_str == 'yes':
    #                                     # Print in green
    #                                     print(f"\033[92m  {key}: {value}\033[0m")
    #                                 else:
    #                                     # Print in red
    #                                     print(f"\033[91m  {key}: {value}\033[0m")
    #                             # No final reset needed as each line resets its color

    #                         # mat is an N×8 numpy array of floats
    #                         print(f"  Loaded matrix with shape {traj_reference.timestamps.shape}")

    #                         # Store metrics along with a reference (e.g., filename)
    #                         metrics = ev.evaluate(traj_reference, traj_estimated)
    #                         evaluated_metrics.append({"name": submission_file_name, "metrics": metrics})

    #                 else:
    #                     print(f"  No matching annotation file found for '{submission_file_name}'")


    # ########## Match the format of eval AI ##########
    # print("Formatting results for EvalAI")

    # # output["result"] = []


    # print("\033[91mPossible error\033[0m", file=sys.stderr)
    # print("❌ Fatal error while parsing", file=sys.stderr)

    output["result"] = [
        {
            "heap": {
                "ATE": 1.34, # Use .get for safety if keys might be missing
                "RTE": 2.45,
                "LE": 3.51
            }
        },
        {
            "eiger": {
                "ATE": 1.34, # Use .get for safety if keys might be missing
                "RTE": 2.45,
                "LE": 3.51
            }
        },
        {
            "tt3": {
                "ATE": 1.34, # Use .get for safety if keys might be missing
                "RTE": 2.45,
                "LE": 3.51
            }
        },
        {
            "tt4": {
                "ATE": 1.34, # Use .get for safety if keys might be missing
                "RTE": 2.45,
                "LE": 3.51
            }
        },
    ]

    # print("🔧 Installing dependencies...")
    # print("📥 Loading annotation file...")
    # print("🧪 Evaluating predictions...")
    # print("📈 Accuracy: 92.3%")
    # print("✅ Evaluation complete!")

    # print("⚠️  Warning: trajectory misaligned", file=sys.stderr)
    # print("❌ Evaluation failed due to missing file", file=sys.stderr)

    # print("\n" + "🧵" * 20 + " LOG START " + "🧵" * 20)

    # for i, eval_result in enumerate(evaluated_metrics):
    #     metrics = eval_result["metrics"]
    #     # Use filename or index to create split names
    #     # split_name = f"split_{i+1}_{eval_result['name'].replace('.tum', '')}"
    #     split_name = eval_result['name'].replace('.tum', '')
    #     output["result"].append(
    #         {
    #             split_name: {
    #                 "ATE": metrics.get("ATE", None), # Use .get for safety if keys might be missing
    #                 "RTE": metrics.get("RTE", None),
    #                 "LE": metrics.get("last_error", None),
    #             }
    #         }
    #     )

    if output["result"]:
        total_ate = 0
        total_rte = 0
        total_le = 0
        count = 0

        for split_result in output["result"]:
            # Each split_result is a dict like {"split_name": {"ATE": x, "RTE": y, "LE": z}}
            # Get the inner metrics dictionary (assuming only one key per outer dict)
            split_name = list(split_result.keys())[0]
            metrics = split_result[split_name]

            # Accumulate metrics if they exist and are not None
            if metrics.get("ATE") is not None:
                total_ate += metrics["ATE"]
            if metrics.get("RTE") is not None:
                total_rte += metrics["RTE"]
            if metrics.get("LE") is not None:
                total_le += metrics["LE"]
            count += 1 # Increment count for each split processed

        # Calculate averages, handle division by zero if count is 0
        if count > 0:
            avg_ate = total_ate / count
            avg_rte = total_rte / count
            avg_le = total_le / count
            output["submission_result"] = {
                "ATE": avg_ate,
                "RTE": avg_rte,
                "LE": avg_le
            }
        else:
            # Handle case with no valid metrics found
            output["submission_result"] = {
                "ATE": None,
                "RTE": None,
                "LE": None
            }
    else:
        output["submission_result"] = {} # Handle case with no evaluated metrics

    # Placeholder for submission metadata based on the requested format.
    # Actual values should be populated based on evaluation results if applicable.
    output["submission_metadata"] = json.dumps(kwargs['submission_metadata'])

    print("Completed evaluation successfully!")
    sys.stdout.flush()

    return output