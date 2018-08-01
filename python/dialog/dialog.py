# Everything needed to converse with dialog flow api
# Based on https://dialogflow-python-client-v2.readthedocs.io/en/latest/ 

# import dialogflow
import dialogflow_v2 as dialogflow
# import dialogflow as dialogflow

# TODO better Errors - raise errors not print 

# Add an intent wrapper
# NOTE currently not used! 
# 
def add_intent(display_name, phrases, messages):
    try:
        create_intent(display_name, phrases, messages)
    except Exception as e:
        print("Error 2:",e)

# Create an intent
# NOTE currently not used! 
# 
def create_intent(display_name, training_phrases_parts,
                  message_texts):
    """Create an intent of the given intent type."""

    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(PROJECT_ID)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.types.Intent.Message.Text(text=message_texts)
    message = dialogflow.types.Intent.Message(text=text)

    intent = dialogflow.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])

    response = intents_client.create_intent(parent, intent)
    return response

    
# Remove an intent wrapper
# NOTE currently not used! 
#
def remove_intent(intent_name):
    try:
        intents_client = dialogflow.IntentsClient()
        parent = intents_client.project_agent_path(PROJECT_ID)
        intents_list = intents_client.list_intents(parent)
        for intent in intents_list:
            # print(intent)
            if intent.display_name == intent_name:
                delete_intent(intent.name)

    except Exception as e:
        print("Error 1:",e)


# Delete an intent
# NOTE currently not used! 
# 
def delete_intent(intent_id):
    """Delete intent with the given intent type and intent value."""
    try:
        intents_client = dialogflow.IntentsClient()
        # intent_path = intents_client.intent_path(PROJECT_ID, intent_id)
        intents_client.delete_intent(intent_id)
    except Exception as e:
        print("Error 3:",e)


# Detect intent based on text
# TODO make this single intent only - no need for list 
# 
def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    # print('Session path: {}\n'.format(session))
  
    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)        

        # print('=' * 20)
        # print('Query text: {}'.format(response.query_result.query_text))
        # print('Detected intent: {} (confidence: {})\n'.format(
        #     response.query_result.intent.display_name,
        #     response.query_result.intent_detection_confidence))
        # print('Fulfillment text: {}\n'.format(
        #     response.query_result.fulfillment_text))
        intent = response.query_result.intent.display_name

    return intent, response

# Detect intent based on audio
# 
def detect_intent_audio(project_id, session_id, audio_file_path,
                        language_code):
    """Returns the result of detect intent with an audio file as input.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    import dialogflow_v2 as dialogflow

    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)
    query_input = dialogflow.types.QueryInput(audio_config=audio_config)

    response = session_client.detect_intent(
        session=session, query_input=query_input,
        input_audio=input_audio)

    print('=' * 20)
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))


# Detect intent based on an audio stream 
# 
def detect_intent_stream(project_id, session_id, audio_file_path,
                         language_code):
    """Returns the result of detect intent with streaming audio as input.

    Using the same `session_id` between requests allows continuation
    of the conversaion."""
    import dialogflow_v2 as dialogflow
    session_client = dialogflow.SessionsClient()

    # Note: hard coding audio_encoding and sample_rate_hertz for simplicity.
    audio_encoding = dialogflow.enums.AudioEncoding.AUDIO_ENCODING_LINEAR_16
    sample_rate_hertz = 16000

    session_path = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session_path))

    def request_generator(audio_config, audio_file_path):
        query_input = dialogflow.types.QueryInput(audio_config=audio_config)

        # The first request contains the configuration.
        yield dialogflow.types.StreamingDetectIntentRequest(
            session=session_path, query_input=query_input)

        # Here we are reading small chunks of audio data from a local
        # audio file.  In practice these chunks should come from
        # an audio input device.
        with open(audio_file_path, 'rb') as audio_file:
            while True:
                chunk = audio_file.read(4096)
                if not chunk:
                    break
                # The later requests contains audio data.
                yield dialogflow.types.StreamingDetectIntentRequest(
                    input_audio=chunk)

    audio_config = dialogflow.types.InputAudioConfig(
        audio_encoding=audio_encoding, language_code=language_code,
        sample_rate_hertz=sample_rate_hertz)

    requests = request_generator(audio_config, audio_file_path)
    responses = session_client.streaming_detect_intent(requests)

    print('=' * 20)
    for response in responses:
        print('Intermediate transcript: "{}".'.format(
                response.recognition_result.transcript))

    # Note: The result from the last response is the final transcript along
    # with the detected content.
    query_result = response.query_result

    print('=' * 20)
    print('Query text: {}'.format(query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        query_result.intent.display_name,
        query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        query_result.fulfillment_text))