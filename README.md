# Genomic Data Transformation Project
This project is part of the course "Diseño y Gestión de Sistemas de Información Genómicos" for the Spring 2024 semester. 
The goal of this project is to facilitate the efficient storage, retrieval, and management of genomic data using relational databases.
This involves transforming genomic data from CSV files and loading them into a MySQL database hosted on Clever Cloud.

The aim is to showcase the transformation of genomic data from raw sequences to a unified model, facilitating efficient data management and analysis. 
The project is segmented into several tasks: downloading genomic datasets, annotating genetic variants, transforming the data into a common format, 
and finally storing it in a relational database for scalability and complex querying.



## Project Structure
GenomicDataTransformation/
│
├── src/
│   ├── annotate.py                 # Script for annotating genomic data
│   ├── download.py                 # Script to download necessary data
│   ├── store.py                    # Script to store data into the database
│   ├── storeVariant.py             # Script specifically for storing variant data
│   ├── transform.py                # Script for data transformation
│   └── database_loader.py          # Main script to load data into the database
│
├── data/
│   ├── Annotation.csv              # Annotations for genomic variants
│   ├── ChromosomeSequence.csv      # Chromosome sequence data
│   ├── Disease.csv                 # Disease information
│   ├── DiseaseVariantLink.csv      # Links between diseases and variants
│   ├── HGVSExpression.csv          # HGVS expressions of genetic variants
│   ├── Interpretation.csv          # Clinical interpretations of variants
│   ├── LocationInfo.csv            # Genomic location information
│   └── LocationInfoVariantLink.csv # Links between locations and variants
│
├── snpEff/
│   ├── snpEff.jar                  # snpEff program for genomic annotations
│   ├── SnpSift.jar                 # SnpSift tool for variant data manipulation
│   ├── snpEff_genes.txt            # Gene data for snpEff
│   ├── snpEff.config               # Configuration for snpEff
│   └── snpEff_summary.html         # Summary output from snpEff
│
├── exec/
│   └── files                       # Directory for executable files and scripts 
│
├── test/
│   ├── test_annotated.vcf          # Test annotated VCF file - currently not done
│   └── test.vcf                    # Test VCF file  - not done
│
└── README.md                       # Documentation for using this project





This project requires Python and several libraries and tools to manage and transform genomic data. 
- Here's how to set up your environment:

## How To Run
