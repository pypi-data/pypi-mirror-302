## Data module

This modules helps to structure the data for the models. General use guidelines are as follows. In the root of the data module there are three folders:

- boundaries: These are boundary conditions for the model
- layers: layer surfaces and their properties
- observations: observation data used, e.g., for model calibration

Additionally, each folder has two subdirectories for storing raw and processed data:

- raw: raw (e.g., unclipped, unfiltered) data
- processed: output data which should be included in the repository and for other people to use to reproduce our results. These files should be clearly named, indluding versioning, etc. Remember that the files put in GitHub should not be too big. If you have big data, perhaps cloud storage like Amazon S3 should be considered.

The structure may appear complex, but in the end the files in each of these directories are imported directly into your script or notebook with `.` notation (from data.boundaries.processed import ghb_layer1)
