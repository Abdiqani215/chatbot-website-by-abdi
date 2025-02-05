import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS  # Remove this line

# Now you can import files from the same directory or other directories
from config import *
from handlers import *
from context import context_manager
from nlp import NLPProcessor
from chat_handlers import generate_response, handle_language_selection

from nlp import nlp_processor  # import the global NLPProcessor instance

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Welcome to Jees Hotel Chatbot! Use /chatbot at the end of the url to start chatting"

@app.route('/api', methods=['POST'])
def api_handler():
    try:
        data = request.get_json()
        action = data.get("action")

        if action == "chat":
            user_id = request.remote_addr
            if context_manager.check_rate_limit(user_id):
                return jsonify({"response": "Please wait a moment before sending another message."})
            if not data or 'message' not in data:
                return jsonify({"error": "Invalid request"}), 400
            response = generate_response(user_id, data['message'])
            return jsonify({"response": response})
        else:
            return jsonify({"error": "Invalid action"}), 400

    except Exception as e:
        app.logger.error(f"API error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot_webhook():
    if request.method == 'POST':
        try:
            # Get data from Gupshup's webhook
            data = request.get_json()  # Assuming Gupshup sends a JSON payload
            user_message = data['message']  # Extract the message from the webhook data
            user_id = data['user_id']  # Extract the user ID if available

            # Generate a response using your bot's logic
            response = generate_response(user_id, user_message)
            
            # Send back the response to Gupshup in the expected format
            return jsonify({"response": response})

        except Exception as e:
            app.logger.error(f"Webhook error: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500
    else:
        # This part handles the GET request when you visit /chatbot URL in a browser
        user_id = request.remote_addr
        
        # Reset the user’s chosen language on each page refresh
        profile = context_manager.get_user_profile(user_id)
        profile['preferred_language'] = None
        profile['state'] = 'awaiting_language'

        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=device-width, initial-scale=1.0">
          <title>Jees Hotel AI Chat Support</title>
          <!-- Google Fonts -->
          <link href="https://fonts.googleapis.com/css?family=Roboto:400,500,700&display=swap" rel="stylesheet">
          <style>
            :root {
              --primary-color: #0d6efd;
              --primary-hover: #0056b3;
              --light-color: #f8f9fa;
              --dark-color: #343a40;
              --white: #ffffff;
            }

            /* Keep the page background transparent */
            body {
              margin: 0;
              padding: 0;
              font-family: 'Roboto', sans-serif;
              background: transparent;
            }

            /*
             Chat container with semi-transparent background:
             - 400×600
             - background: rgba(255,255,255,0.5) for 50% white
             - box-shadow for a subtle border
            */
            #chat-container {
              width: 400px;
              height: 600px;
              max-width: 100%;
              background: rgba(255, 255, 255, 0.5); /* 50% white transparency */
              border-radius: 10px;
              box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
              display: flex;
              flex-direction: column;
              overflow: hidden;
              margin: 0 auto;
              animation: fadeIn 0.5s ease-in;
            }
            @keyframes fadeIn {
              from { opacity: 0; transform: translateY(20px); }
              to   { opacity: 1; transform: translateY(0); }
            }

            /*
             Chat box remains transparent so it also blends with the container's background.
             You can adjust if you prefer a different transparency for the messages area.
            */
            #chat-box {
              flex: 1;
              padding: 20px;
              overflow-y: auto;
              background: transparent;
            }

            /*
             The input area at the bottom:
             Slightly more opaque (white) so user can see the input field text more clearly
             but also can be made semi-transparent if you prefer.
            */
            #message-input {
              display: flex;
              padding: 15px;
              background: rgba(255, 255, 255, 0.75); /* 75% opaque for better contrast */
              border-top: 1px solid #dee2e6;
            }
            #message {
              flex: 1;
              padding: 12px;
              border: 1px solid #ced4da;
              border-radius: 30px;
              font-size: 16px;
              outline: none;
              transition: border-color 0.3s ease;
              background: #fff; /* fully opaque background for text clarity */
            }
            #message:focus {
              border-color: var(--primary-color);
            }
            #send-btn {
              background: var(--primary-color);
              border: none;
              color: var(--white);
              padding: 12px 20px;
              margin-left: 10px;
              border-radius: 30px;
              font-size: 16px;
              cursor: pointer;
              transition: background 0.3s ease;
            }
            #send-btn:hover {
              background: var(--primary-hover);
            }

            /*
             Message bubbles styling
            */
            .message {
              margin-bottom: 20px;
              display: flex;
              animation: slideIn 0.3s ease-out;
            }
            @keyframes slideIn {
              from { opacity: 0; transform: translateX(20px); }
              to   { opacity: 1; transform: translateX(0); }
            }
            .user-message {
              justify-content: flex-end;
            }
            .bot-message {
              justify-content: flex-start;
            }
            .message p {
              max-width: 70%;
              padding: 12px 18px;
              border-radius: 20px;
              font-size: 15px;
              margin: 0;
            }
            .user-message p {
              background: var(--primary-color);
              color: var(--white);
              border-bottom-right-radius: 0;
            }
            .bot-message p {
              background: var(--light-color);
              color: var(--dark-color);
              border-bottom-left-radius: 0;
              border: 1px solid #ced4da;
            }
          </style>
        </head>
        <body>
          <div id="chat-container">
            <!-- No header/title here -->
            <div id="chat-box"></div>
            <div id="message-input">
              <input type="text" id="message" placeholder="Type your message..." onkeypress="checkEnter(event)">
              <button id="send-btn" onclick="sendMessage()">Send</button>
            </div>
          </div>

          <script>
            async function sendMessage() {
              const input = document.getElementById("message");
              const message = input.value.trim();
              if (!message) return;
              
              const chatBox = document.getElementById("chat-box");
              // Append the user's message
              chatBox.innerHTML += `<div class="message user-message"><p>${message}</p></div>`;
              
              // Send the message to the Flask server
              const response = await fetch("/api", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ action: "chat", message: message })
              });
              
              const data = await response.json();
              // Append the bot's message
              chatBox.innerHTML += `<div class="message bot-message"><p>${data.response}</p></div>`;
              
              // Clear the input, scroll to the bottom
              input.value = "";
              chatBox.scrollTop = chatBox.scrollHeight;
            }

            function checkEnter(event) {
              if (event.key === "Enter") {
                event.preventDefault();
                sendMessage();
              }
            }
          </script>
        </body>
        </html>
        '''

if __name__ == "__main__":
    app.run(debug=True)
