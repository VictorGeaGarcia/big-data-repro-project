## Running Dataflow job in project A from Composer in project B ##

The idea of this tutorial is to be able to use a Google Cloud Composer environment running in Project B to launch a Dataflow Job in different projects (Project A i.e).

Basically we want to have a central project from where we use Composer to launch Dataflow jobs to different projects.

In this particular use case we have the following requirements:
<ul>
<li> Project B must have Composer API enabled and Dataflow API disabled.</li>
    <li> Project A must have Composer API disabled and Dataflow API enabled.</li>
<li> We don't want to  make use of Project B SA. So we will create a SA in Project A that will be the one used to launch the DF jobs.</li>
<li><a href=https://airflow.apache.org/integration.html#dataflowpythonoperator>We will use DataflowPythonOperator and its gcp_conn_id parameter </a> </li>
</ul>

## STEPS:  ##


1. Create Project B and enable Composer API.  `project-B-id`
2. Create Composer Environment in project B.  `composer-env-name`
3. Create Project A and enable Dataflow API.  `project-A-id`
- Create Bucket inside Project A (to place staging,temp and output files from Dataflow Job). `bucket-A-name`

4. Create SA in project A `SA-name@project-id.iam.gserviceaccount.com` and grant it the appropriate permissions so that it can launch a DF job:
<ul>
<li>Compute Admin</li>
<li>Dataflow Admin</li>
<li>Dataflow worker</li>
<li>Storage Object Admin</li>
</ul>

5. Create a keyjson file for your SA `SA-name@project-id.iam.gserviceaccount.com`, download it and keep it. `your-dataflow-SA-key.json`
6. To use the `gcp_conn_id` parameter in DataflowPythonOperator we need to do the following (https://cloud.google.com/composer/docs/how-to/managing/connections#creating_new_airflow_connections):

- Go to your Airflow UI --> Admin --> Connections
- Click on Create
- Enter the following values:

-- Conn Id: `your-gcp-conn-id-name`

-- Conn Type: Choose Google Cloud Platform

-- Project ID: `project-A-id`
    
-- Keyfile Path or Keyfile JSON: (Either upload the previously generated SA keyfile in step 5 to Composer Cloud Storage bucket path (/home/airflow/gcs/data/<your-dataflow-SA-key.json>) and add the path to Keyfile Path field or add the contents of the file directly to Keyfile JSON).

7. You'll need to load the code file `DAG_using_DFPythonOperator.py` to your DAG folder, but before doing so perform the following changes to the file:
- Change `staging-bucket` with the name of the bucket you created in step 3.
- Change `project-A-id` to your ProjectA id created in Step 3.
- Load the `wordcount.py` file in this repo to your data/ folder in your Cloud Storage bucket associated to your Cloud Composer environment (run `gcloud composer environments describe "your-cloud-composer-env" --location "your-composer-env-location""` to see your bucket name) 
- Change the `your-gcp-conn-id-name` name to the one you have given to the connection created in step 6.

8. This will not work and it should throw some error like the following:

`IOError: Could not upload to GCS path gs://\\<staging-bucket\\>/.../... access denied. Please verify that credentials are valid and that you have write access to the specified path.`

Even everything is correct, your staging bucket is in ProjectA, and the SA which should be used for the connection has been granted StorageAdmin permissions in that project. Still it doesn't work due to <a href=https://issues.apache.org/jira/browse/AIRFLOW-2009>this issue</a>

9. Although not that neat, we can use the following workaround: 

Only using BashOperator to launch the Job without using the DataflowPythonOperator. To use this approach load the file `DAG_using_BashOperator.py` to your DAG folder. Before doing so do:


- Locate the keyjson file created in step 5 to your data/ folder in your Cloud Storage bucket associated to your Cloud Composer environment (we will need to export our `GOOGLE_APPLICATION_CREDENTIALS` to this path). Now change `your-dataflow-SA-key.json` to your KeyJson filename.
- Change `staging-bucket` with the name of the bucket you created in step 3.
- Change `project-A-id` to your ProjectA-id created in Step 3.
