#Project Configurations - for flights.py
project_name='sa-pipeline-bakeoff'
zone = 'us-central1-a'
#template_bucket
template_bucket = 'covid-19-bakeoff-data'
#Daily Trigger Dataflow Template Constants
job_name ='flights-pipelie'
#input param name, depends on what you have defined in your dataflow pipeline
input_param_name = input_data
# ValueProviders like source table name and sink table name
input_data ={"sourceTable":"source_table_name", "sinkTable":"sink_table_name"}
#Template's GCS path
template_gcs_path='gs://{bucket}/dataflow/template/Template_Name'.format(bucket=template_bucket)
Temprory path location
temp_location='gs://{bucket}/dataflow/template/user-sync-etl/temp'.format(bucket=template_bucket)