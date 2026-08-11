# Bibliometric Normalization System (BNS)

**Bibliometric Normalization System (BNS)** is a Python toolkit for cleaning, normalizing, and disambiguating large-scale bibliometric datasets, with a primary focus on Web of Science (WoS) data.

## Overview

Bibliometric datasets frequently contain inconsistencies in author names, affiliations, keywords, column structures, and bibliometric metadata. These inconsistencies can affect author-level analyses and the reproducibility of bibliometric studies.

BNS provides an end-to-end workflow for:

* Data cleaning
* Web of Science column standardization
* Author name normalization
* Author grouping
* Author similarity analysis
* Author disambiguation
* Merge candidate generation
* Confidence scoring
* Author ID assignment
* Bibliometric indicator calculation
* Structured Excel and CSV export

The system is designed with a modular architecture and automated tests to support reproducible and maintainable bibliometric data processing.

## Key Features

* Automated bibliometric data cleaning
* Web of Science column mapping and standardization
* Author name normalization
* Author grouping
* Fuzzy similarity analysis using RapidFuzz
* Author merge candidate generation
* Confidence-based author disambiguation
* Automatic merge and manual review classification
* Unique Author ID assignment
* Author-level bibliometric indicators
* Excel and CSV export
* Modular Python architecture
* Automated test suite

## Workflow

BNS processes bibliometric data through the following workflow:

1. Load Web of Science dataset
2. Clean raw bibliometric data
3. Standardize column names
4. Normalize author information
5. Build author groups
6. Generate author merge candidates
7. Calculate similarity and confidence scores
8. Classify merge decisions
9. Apply author merges
10. Assign unique Author IDs
11. Calculate author-level bibliometric indicators
12. Export normalized data and analysis results

## Bibliometric Indicators

The current version provides the following author-level indicators:

* Publication count
* Citation count
* Average citations
* h-index
* i10-index
* First publication year
* Last publication year
* Academic age

## Generated Outputs

The BNS pipeline generates the following files:

### `Normalized_WoS_Data.xlsx`

Normalized and processed Web of Science records, including standardized author information and assigned Author IDs.

### `Author_Metrics.xlsx`

Author-level bibliometric indicators including publication count, citation count, average citations, h-index, i10-index, publication years, and academic age.

### `Merge_Report.xlsx`

Author merge candidates, confidence scores, and merge decisions for author disambiguation.

## Project Structure

```text
Bibliometric-Normalization-System/
|-- input/
|-- output/
|-- notebooks/
|-- tests/
|   |-- test_author_id.py
|   |-- test_author_normalization.py
|   |-- test_config.py
|   |-- test_exporter.py
|   |-- test_indicator.py
|   |-- test_merge_engine.py
|   `-- test_similarity.py
|-- src/
|   |-- author_id.py
|   |-- author_normalization.py
|   |-- cleaning.py
|   |-- column_mapping.py
|   |-- config.py
|   |-- exceptions.py
|   |-- exporter.py
|   |-- indicator.py
|   |-- logger.py
|   |-- merge_engine.py
|   |-- similarity.py
|   `-- utils.py
|-- main.py
|-- README.md
|-- LICENSE
|-- requirements.txt
|-- pyproject.toml
`-- .gitignore
```

## Requirements

* Python 3.12 or later
* pandas
* openpyxl
* RapidFuzz

Development and testing additionally require pytest.

## Installation

### Clone the repository

```bash
git clone https://github.com/<your-username>/Bibliometric-Normalization-System.git
cd Bibliometric-Normalization-System
```

### Create a virtual environment

Windows:

```bash
python -m venv .venv
```

Activate:

```bash
.venv\Scripts\activate
```

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
python -m pip install -r requirements.txt
```

For development and testing:

```bash
python -m pip install -e ".[dev]"
```

## Usage

Place the Web of Science Excel dataset in the `input/` directory.

The current example workflow expects:

```text
input/combining yazar listesi.xlsx
```

Run the complete BNS pipeline with:

```bash
python main.py
```

The generated results will be written to the `output/` directory.

## Testing

BNS includes an automated test suite covering configuration, author normalization, similarity analysis, merge logic, Author ID assignment, bibliometric indicators, and output generation.

Run all tests with:

```bash
python -m pytest -v
```

Current test status:

```text
33 passed
```

## Build

The project uses the Python `pyproject.toml` packaging standard and setuptools.

Build the package with:

```bash
python -m build
```

The build generates source and wheel distributions in the `dist/` directory.

## Release

**Version:** 1.0.0

**Status:** Release Ready

The v1.0.0 release includes:

* Complete bibliometric data normalization workflow
* Author name normalization and disambiguation
* Author ID assignment
* Author-level bibliometric indicators
* Excel and CSV export
* Automated test suite
* Python package build configuration
* MIT License

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Author

**Samet UCAK**

Associate Professor of Molecular Biology and Genetics
Istanbul Aydin University
Turkiye
