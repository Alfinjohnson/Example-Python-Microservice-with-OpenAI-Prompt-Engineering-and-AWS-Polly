# Example Python Microservice with OpenAI - Prompt Engineering and AWS Polly

#### "This project seamlessly handles user-input topics using OpenAI and prompt engineering, converting them into audio through AWS Polly, and securely archiving them on AWS S3. It also interfaces with MongoDB to preserve important transcripts and chat data. Utilizing Flask, the project efficiently manages each task within microservices, guaranteeing both scalability and adherence to industry standards. In summary, this project brings together AI, audio conversion, cloud storage, and database integration to streamline content creation and storage."
This project is a prime example of leveraging advanced technologies and techniques to create a versatile application, including:

- **OpenAI Integration**: Harnessing the power of OpenAI's state-of-the-art language models and artificial intelligence to enhance the capabilities of your microservice.

- **Prompt Engineering**: Employing prompt engineering techniques to enable natural language interactions, making your application more intuitive and user-friendly.

- **AWS Polly Integration**: Utilizing Amazon Polly, a cloud-based service, for on-demand text-to-speech conversion, which allows you to generate audio content from text inputs.

- **Data Storage with AWS S3**: Saving and retrieving data in Amazon S3, a scalable and secure object storage service that facilitates efficient storage of various data types, including audio files.

- **MongoDB Connectivity**: Establishing seamless connections with MongoDB, a versatile NoSQL database, for efficient data storage and retrieval. This database integration ensures that you can manage and query data effectively.

- **HTML & CSS**: Use to create sample ui for topic creation.

## Configuration File Management

To enhance security and customization, each microservice directory includes a `config.py` file. Here are the steps to set up your configuration:

1. In each microservice directory, locate the `config.py` file.
2. Replace placeholders with your specific credentials, such as usernames, passwords, and API keys, ensuring that your configuration is secure.
3. Save the changes within the `config.py` file, keeping your credentials confidential.

## Get Started

To prepare your Python development environment for this project, follow these steps:

1. Clone the project repository to your local machine.

   ```bash
   git clone https://github.com/Alfinjohnson/Example-Python-Microservice-with-OpenAI-Prompt-Engineering-and-AWS-Polly.git
   cd Example-Python-Microservice-with-OpenAI-Prompt-Engineering-and-AWS-Polly
   ```

2. Create a virtual environment to isolate project dependencies.

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install the project dependencies from the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

5. Your Python development environment is now configured and ready for use.


end.