from tqdm import tqdm

import utilities


input_file_paths = utilities.load_input_file_paths()
data_sets = utilities.load_depth_data_sets(input_file_paths)

print(f"Creating heatmaps for {len(data_sets)} datasets")

for data_set_path, frames in tqdm(data_sets.items(), desc="Progress: "):
    utilities.create_heatmap(frames, data_set_path)
