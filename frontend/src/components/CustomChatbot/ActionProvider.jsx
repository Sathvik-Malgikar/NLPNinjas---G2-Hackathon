import React from 'react';
import Loader from './Loader'
import axios from 'axios'
import { BACKEND_URL } from '../../App';

const ActionProvider = ({ createChatBotMessage, setState, children }) => {

  const handleSubmit = async (message) => {
    // Add Loading before API call

    axios.post(BACKEND_URL+'/rag/query', {
      "query": message
    })
    .then((res)=>{
      const loading = createChatBotMessage(<Loader />)
      setState((prev) => ({ ...prev, messages: [...prev.messages, loading], }))
    })
    .catch((err)=>{
      const errMsg = createChatBotMessage(err['response']['data']['message'])
      setState((prev) => ({ ...prev, messages: [...prev.messages, errMsg], }))
    })

    const polling = setInterval(()=>{
      axios.get(BACKEND_URL+'/rag/get-results')
      .then((res)=>{
        if (res['data']['results'] === undefined){
          console.log('processing', res['data'])
        }
        else {
          const ragResp = res['data']['results']
          console.log(ragResp)
          const processedRagResp = ragResp.split('Answer:')[1];
          const botMessage = createChatBotMessage(processedRagResp)

          setState((prev) => {
              // Remove Loading here
              const newPrevMsg = prev.messages.slice(0, -1)
              return { ...prev, messages: [...newPrevMsg, botMessage], }
          })

          clearInterval(polling)
        }
      })
      .catch((err)=>{
        clearInterval(polling)
      })
    }, 1000)

    // Stop Loading after call is returned
    

}

  return (
    <div>
      {React.Children.map(children, (child) => {
        return React.cloneElement(child, {
          actions: {
            handleSubmit
          },
        });
      })}
    </div>
  );
};

export default ActionProvider;