import React from 'react'
import config from './config'
import ActionProvider from './ActionProvider'
import MessageParser from './MessageParser'
import Chatbot from 'react-chatbot-kit'
import 'react-chatbot-kit/build/main.css'
import './CustomChatbot.css'

const CustomChatbot = () => {
  return (
    <Chatbot
        config={config}
        messageParser={MessageParser}
        actionProvider={ActionProvider}
      />
  )
}

export default CustomChatbot