import os
import sys
import json
import boto3
import psycopg2
from dotenv import load_dotenv

def initialize_s3_client():
    """
    Initialize the s3 client
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    endpoint_url = os.environ.get("ENDPOINT_URL")
    s3_client = boto3.client(
        service_name="s3",
        endpoint_url=endpoint_url,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key
    )

    result = s3_client.get_bucket_acl(Bucket=os.environ.get("BUCKET_NAME"))

    return s3_client

def list_s3_files(s3_client):
    """
    Return S3 files for a specific bucket and prefix
    """
    bucket_name = os.environ.get("BUCKET_NAME")
    s3_file_path = os.environ.get("S3_FILE_PATH","")
    s3_files = []
    response = s3_client.list_objects_v2(
        Bucket = bucket_name,
        Prefix = s3_file_path
    )
    if response.get("KeyCount")>0:
        s3_files = response.get("Contents")
    print(s3_files)
    return s3_files

def download_s3_file(s3_client, s3_file, local_file_path):
    """
    Download the file from s3 to local
    """
    bucket_name = os.environ.get("BUCKET_NAME")
    local_folder_path = os.path.split(local_file_path)[0]
    os.makedirs(local_folder_path, exist_ok=True)
    s3_client.download_file(bucket_name, s3_file, local_file_path)

def load_csv_to_sql(local_file_path):
    """
    Load contents of csv file to sql table
    """
    sql_host = os.environ.get("SQL_HOST")
    sql_user = os.environ.get("SQL_USER")
    sql_password = os.environ.get("SQL_PASSWORD")
    sql_db = os.environ.get("SQL_DB")
    sql_table = os.environ.get("SQL_TABLE")

    sql_connection = psycopg2.connect(
        host=sql_host,
        user=sql_user,
        password=sql_password,
        database=sql_db
    )

    sql_cursor = sql_connection.cursor()

    try:
        with open(local_file_path) as json_file:
            data = json.load(json_file)

            print("Type:", type(data))
            i = int(1)
            for node in data:
                print(node)
                path = str(i).zfill(4)
                i = i + 1
                sql = "INSERT INTO cookbook_food (name, description, ignore_shopping, space_id, depth, numchild, path, substitute_children, substitute_siblings) VALUES ('" + str(node) +"', ' ', False, 1, 1, 0, " + path + ", False, False)"
                sql_cursor.execute(sql)
                sql_connection.commit()

    except Exception as load_exception:
        sql_connection.rollback()
        raise Exception("SQL LOAD error: " + str(load_exception)) from load_exception

    sql_cursor.close()
    sql_connection.close()


def main():
    """
    Main function which imports the data from s3 to PostgreSQL database
    """
    load_dotenv()
    print(str(sys.argv[1]))
    data_folder_path = "./data/"
    s3_client = initialize_s3_client()

    local_file_path = os.path.join(data_folder_path, sys.argv[1])

    download_s3_file(s3_client, sys.argv[1], local_file_path)
    load_csv_to_sql(local_file_path)

if __name__ == "__main__":
    main()
