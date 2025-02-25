# Read TDMS files
This repository contains a simple script to read TDMS files from a given directory, plot them and save them as csv files.

TDMS (Technical Data Management Streaming) files are a proprietary format from National Instruments, and can be read using the `nptdms` library.

A TDMS file consists of three hierarchical levels:

1. **File Level**: Contains global properties and metadata.
2. **Group Level**: Organizes data into logical groups (e.g., different sensors or signal types).
3. **Channel Level**: Contains actual measurement data and properties related to individual signals.


For reproducibility:

```bash
conda create -n tdms -y python mamba
conda activate tdms
mamba install -y numpy pandas matplotlib ipykernel nptdms
```