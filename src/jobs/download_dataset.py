# Databricks notebook source
# MAGIC %md
# MAGIC # Download HR Synthetic Dataset into Unity Catalog
# MAGIC
# MAGIC This notebook downloads the [**HR Synthetic Dataset**](https://huggingface.co/datasets/dougtrajano/hr-synthetic-database) from [**Hugging Face**](https://huggingface.co/), convert it into Pandas DataFrames, and write the data as Delta tables into Databricks Unity Catalog for further analysis.

# COMMAND ----------

# DBTITLE 1,Install Dependencies
%pip install datasets==4.1.1 pandas==2.3.3

# COMMAND ----------

# DBTITLE 1,Imports and Env Vars
import os

import pandas as pd
from datasets import load_dataset


os.environ['HF_DATASETS_CACHE'] = '/tmp/.cache'

# COMMAND ----------

# DBTITLE 1,Job Parameters
dbutils.widgets.text('catalog', 'doug')
dbutils.widgets.text('schema', 'agentic_ai_workshop')

catalog = dbutils.widgets.get('catalog')
schema = dbutils.widgets.get('schema')

# COMMAND ----------

# DBTITLE 1,Load Dataset
business_units = load_dataset('dougtrajano/hr-synthetic-database', 'business_units')
departments = load_dataset('dougtrajano/hr-synthetic-database', 'departments')
jobs = load_dataset('dougtrajano/hr-synthetic-database', 'jobs')
employees = load_dataset('dougtrajano/hr-synthetic-database', 'employees')
compensations = load_dataset('dougtrajano/hr-synthetic-database', 'compensations')

# COMMAND ----------

# DBTITLE 1,Convert into Pandas DataFrame
df_business_units = pd.DataFrame(business_units['train'])
df_departments = pd.DataFrame(departments['train'])
df_jobs = pd.DataFrame(jobs['train'])
df_employees = pd.DataFrame(employees['train'])
df_compensations = pd.DataFrame(compensations['train'])

print(f'df_business_units: {df_business_units.shape}')
print(f'df_departments: {df_departments.shape}')
print(f'df_jobs: {df_jobs.shape}')
print(f'df_employees: {df_employees.shape}')
print(f'df_compensations: {df_compensations.shape}')

# COMMAND ----------

# DBTITLE 1,Write UC Delta Tables
spark_df_business_units = spark.createDataFrame(df_business_units)
spark_df_departments = spark.createDataFrame(df_departments)
spark_df_jobs = spark.createDataFrame(df_jobs)
spark_df_employees = spark.createDataFrame(df_employees)
spark_df_compensations = spark.createDataFrame(df_compensations)


spark_df_business_units.write.mode('overwrite').saveAsTable(f'{catalog}.{schema}.business_units')
spark_df_departments.write.mode('overwrite').saveAsTable(f'{catalog}.{schema}.departments')
spark_df_jobs.write.mode('overwrite').saveAsTable(f'{catalog}.{schema}.jobs')
spark_df_employees.write.mode('overwrite').saveAsTable(f'{catalog}.{schema}.employees')
spark_df_compensations.write.mode('overwrite').saveAsTable(f'{catalog}.{schema}.compensations')
