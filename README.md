# quad_cad

This repository contains Quadruped Designs using CadQuery.

## Installing CadQuery

1. **Create a conda environment:**
    ```sh
    conda create --name quad_cad
    conda activate quad_cad
    ```

2. **Download the CadQuery repository:**
    ```sh
    git clone https://github.com/CadQuery/cadquery.git
    ```

3. **Install the local repository:**
    ```sh
    cd cadquery
    pip install -e .
    ```

## Installing CQ-editor

Refer to the [CadQuery documentation](https://cadquery.readthedocs.io/en/latest/installation.html#adding-a-nicer-gui-via-cq-editor) for more details.

### Steps

1. **Download the latest CQ-editor installer:**
    ```sh
    curl -LO https://github.com/CadQuery/CQ-editor/releases/download/nightly/CQ-editor-master-Linux-x86_64.sh
    ```

2. **Run the installer:**
    ```sh
    sh CQ-editor-master-Linux-x86_64.sh
    ```

3. **Launch CQ-editor:**
    ```sh
    $HOME/cq-editor/run.sh
    ```