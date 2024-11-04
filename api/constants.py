#api_nlu_address = 'http://192.168.1.45:9003'
api_nlu_address = 'http://localhost:9003'
api_parse_message = f'{api_nlu_address}/model/parse'
api_get_message = f'{api_nlu_address}/webhooks/rest/webhook'
intent_files = {
            'booking': '../../ai-chatbot-rasa-en/ai-chatbot-rasa-en/data/booking.yml',
            'doctor': '../../ai-chatbot-rasa-en/ai-chatbot-rasa-en/data/doctor.yml',
            'clinic': '../../ai-chatbot-rasa-en/ai-chatbot-rasa-en/data/clinic.yml',
            'hospital': '../../ai-chatbot-rasa-en/ai-chatbot-rasa-en/data/hospital.yml',
            'symptom': '../../ai-chatbot-rasa-en/ai-chatbot-rasa-en/data/symptom.yml',
            'consultant': '../../ai-chatbot-rasa-en/ai-chatbot-rasa-en/data/consultant.yml',
            'patient': '../../ai-chatbot-rasa-en/ai-chatbot-rasa-en/data/patient.yml',
            'health': '../../ai-chatbot-rasa-en/ai-chatbot-rasa-en/data/health.yml',
            'domain': '../../ai-chatbot-rasa-en/ai-chatbot-rasa-en/domain.yml',
            'stories': '../../ai-chatbot-rasa-en/ai-chatbot-rasa-en/data/stories.yml',
        }
