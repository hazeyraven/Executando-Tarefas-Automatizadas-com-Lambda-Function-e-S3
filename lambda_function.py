import json
import boto3
import urllib.parse
import os
from decimal import Decimal 

endpoint_url = os.environ.get('AWS_ENDPOINT_URL', 'http://localhost:4566')

s3_client = boto3.client('s3', endpoint_url=endpoint_url)
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
table = dynamodb.Table('NotasFiscais')

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            bucket_name = record['s3']['bucket']['name']
            file_key = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding='utf-8')

            response = s3_client.get_object(Bucket=bucket_name, Key=file_key)
            file_content = response['Body'].read().decode('utf-8')
            
            notas = json.loads(file_content, parse_float=Decimal)

            for nota in notas:
                table.put_item(Item=nota)
                print(f"Nota {nota.get('id_nota')} gravada com sucesso")

        return {
            'statusCode': 200,
            'body': json.dumps('Processamento e gravacao concluidos com sucesso')
        }
    except Exception as e:
        print(f"Erro no processamento: {e}")
        raise e