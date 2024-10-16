# AvahiAI

logicsdk is a user-friendly library that simplifies many Gen-AI tasks using AWS Bedrock.

## current Features
- Summarize plain text.
- Summarize text from local files (`.txt`, `.pdf`, `.docx`).
- Summarize text from S3 files (`.txt`, `.pdf`, `.docx`).
- Extract the entities from plain text.
- Extract the entities from from local files (`.txt`, `.pdf`, `.docx`).
- Extract the entities from from S3 files (`.txt`, `.pdf`, `.docx`).
- Support for custom prompts and different anthropic claude model versions.
- Error handling with user-friendly messages.
- And many more to come...

## Installation

You can install logic just by running:

```sh
pip install logicsdk
```

### AWS CLI Installation (Optional but Recommended)
To configure your AWS credentials easily, you can use the AWS CLI. Install it by following instructions on the [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html).

## Configuration

### AWS Credentials

AvahiAI requires AWS credentials to access AWS Bedrock and S3 services. You can provide your AWS credentials in two ways:

1. **Default AWS Credentials**: Ensure your AWS credentials are configured in the `~/.aws/credentials` file or by using the AWS CLI.
2. **Explicit AWS Credentials**: Pass the AWS Access Key and Secret Key when calling the `summarize` function.

### Configuring AWS Credentials Using AWS CLI

After installing the AWS CLI, run the following command to configure your credentials:

```sh
aws configure
```

You will be prompted to enter your AWS Access Key ID, Secret Access Key, region, and output format. This will create or update the `~/.aws/credentials` file with your credentials.

### Sample `~/.aws/credentials` File:

```ini
[default]
aws_access_key_id = YOUR_ACCESS_KEY
aws_secret_access_key = YOUR_SECRET_KEY
```

## Usage

### Importing logicsdk

```python
import logicsdk
```

### Summarizing Text Strings

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.summarize("This is a test string to summarize.")
print("Summary:", extraction_output)
print("Input Cost:", input_token_cost)
print("Output Cost:", output_token_cost)
print("Cost:", total_cost)
```

## Summarization

### Summarizing Local Files

#### Text File (`.txt`)

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.summarize("path/to/your/file.txt")
print("Summary:", extraction_output)
```

#### PDF File (`.pdf`)

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.summarize("path/to/your/file.pdf")
print("Summary:", extraction_output)
```

#### DOCX File (`.docx`)

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.summarize("path/to/your/file.docx")
print("Summary:", extraction_output)
```

### Summarizing Files from S3

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.summarize("s3://your-bucket-name/your-file.pdf", aws_access_key_id="your_access_key", aws_secret_access_key="your_secret_key")
print("Summary:", extraction_output)
```

### Using a Custom Prompt

```python
custom_prompt = "Please summarize the following document."
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.summarize("path/to/your/file.docx", user_prompt=custom_prompt)
print("Summary:", extraction_output)
```

### Changing the Default Model

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.summarize("path/to/your/file.docx", model_name="haiku-3.0")
print("Summary:", extraction_output)
```


## Extraction

### Extracting from Strings

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.structredExtraction("This is a test string to for the extraction.")
print("Extraction:", extraction_output)
print("Input Cost:", input_token_cost)
print("Output Cost:", output_token_cost)
print("Cost:", total_cost)
```


### Extracting from Local Files

#### Text File (`.txt`)

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.structredExtraction("path/to/your/file.txt")
print("Extraction:", extraction_output)
```

#### PDF File (`.pdf`)

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.structredExtraction("path/to/your/file.pdf")
print("Summary:", extraction_output)
```

#### DOCX File (`.docx`)

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.structredExtraction("path/to/your/file.docx")
print("Summary:", extraction_output)
```

### Extracting from Files in S3

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.structredExtraction("s3://your-bucket-name/your-file.pdf", aws_access_key_id="your_access_key", aws_secret_access_key="your_secret_key")
print("Summary:", extraction_output)
```

### Using a Custom Prompt

```python
custom_prompt = "Please summarize the following document."
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.structredExtraction("path/to/your/file.docx", user_prompt=custom_prompt)
print("Summary:", extraction_output)
```

### Changing the Default Model

```python
extraction_output, input_token_cost, output_token_cost, total_cost = logicsdk.structredExtraction("path/to/your/file.docx", model_name="haiku-3.0")
print("Summary:", extraction_output)
```


## Other more Gen-ai task to come

## Error Handling

AvahiAI provides user-friendly error messages for common issues. Here are some common errors you might encounter:

1. **Invalid AWS Credentials**
```sh
AWS credentials are not set or invalid. Please configure your AWS credentials.
```

2. **File Not Found**
```sh
The file at path/to/your/file.pdf does not exist. Please check the file path.
```

4. **Unexpected Errors**
```sh
An unexpected error occurred: <error message>.
```

## Contributing

Feel free to open issues or submit pull requests if you find bugs or have features to add.

## License
