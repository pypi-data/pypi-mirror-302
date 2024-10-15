import boto3

# Create a Textract client
textract_client = boto3.client('textract', region_name='ap-south-1')

def analyze_id_document(bucket_name, document_key):
    """
    Analyze an identity document stored in an S3 bucket using AWS Textract's AnalyzeID operation.
    
    :param bucket_name: Name of the S3 bucket where the document is stored.
    :param document_key: Key of the document in the S3 bucket.
    :return: Response from AWS Textract.
    """
    try:
        response = textract_client.analyze_id(
            DocumentPages=[{
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': document_key
                }
            }]
        )
        return response
    except Exception as e:
        print(f"Error analyzing ID document: {e}")
        return None

def extract_identity_document_fields(response):
    """
    Extract key-value pairs from the AnalyzeID response.
    
    :param response: Response from AWS Textract AnalyzeID operation.
    :return: Dictionary of field names and values with confidence scores.
    """
    if not response:
        return {}

    document_fields = response['IdentityDocuments'][0]['IdentityDocumentFields']
    kv_pairs = {}
    for field in document_fields:
        key = field['Type']['Text']
        value = field['ValueDetection']['Text']
        kv_pairs[key] = value

    return kv_pairs