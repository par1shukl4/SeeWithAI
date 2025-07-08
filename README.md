# SeeWithAI
This is the repository for a team project, SeeWithAI which works as a tool to battle inaccessibility faced by differently abled people

## Problem Statement

According to the World Health Organization, more than 285 million people worldwide live with some form of visual impairment. In India alone, this number exceeds 50 million. Despite the growing reliance on visual information in daily life, most public infrastructure, products, and services lack accessibility features tailored to non-visual interaction.

Challenges faced by visually impaired individuals include:
- Limited access to contextual information in public spaces (e.g., markets, bus stations, retail stores)
- Inability to interpret signs, prices, gestures, and faces in real time
- Over-reliance on human assistance, especially in unfamiliar environments
- Limited adoption of Braille and inadequate presence of tactile or audio indicators in most environments

Traditional assistive devices (e.g., white canes, screen readers) offer minimal help in interpreting surroundings beyond immediate obstacles. SeeWithAI aims to solve this by leveraging mobile AI, speech interfaces, and computer vision to deliver detailed, real-time environmental feedback.

## Solution Summary

SeeWithAI is a mobile application that:
- Captures the user's surroundings using the device’s camera
- Processes the visual data using AI-based scene understanding and object recognition models
- Delivers contextual descriptions as clear, natural speech
- Offers a hands-free experience using voice commands
- Provides location-based and emergency assistance features

## Core Features

1. **Voice Command Interface**
   - Users initiate actions by speaking natural commands (e.g., "What’s in front of me?", "Read this sign", "Click photo")
   - No touch input required for core functionality

2. **Real-Time Image-to-Voice Conversion**
   - Captures images through the camera and translates visual elements into spoken descriptions
   - Describes people, objects, scene layout, and spatial relationships

3. **Object Recognition**
   - Identifies common items (e.g., fruits, vehicles, signboards, doors, bags) using computer vision models
   - Provides orientation and direction (e.g., "A man is standing two meters to your left")

4. **Text Recognition**
   - Reads printed text such as signboards, price tags, menus, or product labels using OCR
   - Extracted text is processed and spoken aloud to the user

5. **Contextual Q&A (Ask Me Anything)**
   - Users can ask environment-specific questions
   - Responses are generated based on current visual input and location (if permitted)

6. **Emergency Support**
   - Voice-triggered access to emergency helplines
   - Stores location-specific emergency contacts

7. **Memory Recall**
   - Allows the user to retrieve descriptions of previously captured scenes

8. **Optional Location Awareness**
   - Provides environmental context (e.g., “You are in a marketplace”)
   - Uses basic GPS and scene classification

## Technical Architecture

### System Flow

1. User initiates voice command
2. Speech is converted to text via on-device or cloud-based STT
3. Application captures an image using the rear camera
4. Visual data is passed through:
   - Object Detection Model (e.g., YOLOv8)
   - Scene Captioning Model (e.g., Vision-Language Transformer)
   - OCR module for text extraction
5. Processed information is structured into human-readable responses
6. Text is converted to audio using a TTS engine
7. Audio output is played back to the user

### Tech Stack (Modular)

| Component                  | Description                                                                |
|----------------------------|-----------------------------------------------------------------------------|
| Mobile Framework           | Flutter or Kotlin (Android-first development)                              |
| Voice Input (STT)          | Speech-to-text conversion for hands-free commands                          |
| Voice Output (TTS)         | Converts AI-generated responses to spoken audio                            |
| Image Capture              | Uses device camera with autofocus                                          |
| Object Detection           | YOLOv8 or TensorFlow Lite for on-device or edge object recognition         |
| Scene Understanding        | Vision-language models (e.g., GPT-4o Vision or Google Vision)              |
| OCR                        | Text extraction from images                                                |
| Context-Aware NLP Layer    | Converts raw detections into natural language feedback                     |
| Location Module (Optional) | Basic GPS-based context for coarse location awareness                      |
| Backend (Optional)         | FastAPI or Firebase for emergency data, logs, analytics                    |

## Installation Guide

### Prerequisites

- Android smartphone with camera and microphone
- Flutter SDK or Android Studio (for development)
- Internet access (for cloud-based models and TTS/STT services)
- API access to computer vision and NLP models (if using cloud inference)
