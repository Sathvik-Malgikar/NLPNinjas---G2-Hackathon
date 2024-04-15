import { createChatBotMessage } from 'react-chatbot-kit';
import Monty from '../../assets/monty.svg';

const config = {
  initialMessages: [createChatBotMessage(`Hey! This is Monty, ask me anything about this product's reviews!`)],
  botName: "Monty",
  customComponents: {
    botAvatar: ()=><img src={Monty} className='w-1/6 h-1/6'></img>,
  },
};

export default config;