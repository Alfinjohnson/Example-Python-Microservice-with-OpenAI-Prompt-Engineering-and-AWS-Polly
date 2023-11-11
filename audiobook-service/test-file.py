import json

import boto3
from const import AWS_ACCESS_KEY, AWS_SEC_KEY

# Set up the Amazon Polly client
polly_client = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SEC_KEY,
    region_name='ap-south-1'
).client('polly')

# Set the text to synthesize
text = "MSI is a world leader in gaming, content creation, business & productivity and AIoT solutions. Bolstered by " \
       "its cutting-edge R&D capabilities and customer-driven innovation, MSI has a wide-ranging global presence " \
       "spanning over 120 countries. Its comprehensive lineup of laptops, graphics cards, monitors, motherboards, " \
       "desktops, peripherals, servers, IPCs, robotic appliances, and vehicle infotainment and telematics systems are " \
       "globally acclaimed. Committed to advancing user experiences through the finest product quality, " \
       "intuitive user interface and design aesthetics, MSI is a leading brand that shapes the future of technology. " \
       "For more product information, please go to https://www.msi.com."

# Synthesize the speech
audio_response = polly_client.synthesize_speech(
    OutputFormat='mp3',
    Text=text,
    VoiceId='Joanna'
)

# Save the audio to a file
with open('resources/output.mp3', 'wb') as file:
    file.write(audio_response['AudioStream'].read())

# Synthesize the speech and get the sentence marks
marks_response = polly_client.synthesize_speech(
    OutputFormat='json',
    Text=text,
    VoiceId='Joanna',
    # sentence | ssml | viseme | word
    SpeechMarkTypes=['word']
)

# Parse the JSON response
marks = json.loads('[' + marks_response['AudioStream'].read().decode('utf-8').replace('}\n{', '},\n{') + ']')

# Generate the transcript
transcript = []
for mark in marks:
    start_time = mark['time'] / 1000
    sentence = mark['value']
    transcript.append({
        'start_time': start_time,
        'sentence': sentence
    })

# Write the transcript to a JSON file
with open('resources/transcript.json', 'w') as file:
    json.dump(transcript, file, indent=4)
