import React, { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import g2Logo from '../assets/g2-logo.png'
import { Rating } from 'react-simple-star-rating'
import WorldMap from "react-svg-worldmap";
import {countryCodes, secondaryMetricsMap} from '../components/Mappers'
import axios from 'axios'
import { BACKEND_URL } from '../App';
import MetricCard from '../components/MetricCard';
import CustomChatBot from '../components/CustomChatbot/CustomChatbot'

import Chatbot from 'react-chatbot-kit'
import 'react-chatbot-kit/build/main.css'

// TODO
// Map's scaling issue (tooltip)

const Search = () => {

  const [regionwiseData, setRegionwiseData] = useState([]);
  const [secondaryMetrics, setSecondaryMetrics] = useState(null);
  const [reviewData, setReviewData] = useState([]);

  const getFormattedRegionwiseData = (data)=>{
    let formattedData = [];
    Object.keys(data).forEach((country)=>{
      if (countryCodes[country] === undefined){
        console.log(country)
      }
      formattedData.push({"country": countryCodes[country],
                          "value": data[country]
                          })
    })
    return formattedData
  }

  useEffect(()=>{

    // regionwise rating
    axios.get(BACKEND_URL+'/aggregates/regionwise-rating')
    .then((res)=>{
      setRegionwiseData(getFormattedRegionwiseData(res["data"]));
    })
    .catch(()=>{
      console.error('Failed to fetch regionwise rating.')
    })

    // secondary metrics
    axios.get(BACKEND_URL+'/aggregates/average-secondary-metrics')
    .then((res)=>{
        setSecondaryMetrics(res['data'])
    })
    .catch(()=>{
      console.error('Failed to fetch secondary metrics')
    })

    // review data
    axios.get(BACKEND_URL+'/aggregates/aspect-keywords')
    .then((res)=>{
      setReviewData(res['data']['review_data'])
    })
    .catch(()=>{
      console.error('Failed to fetch review data')
    })


    // polarity keywords
    axios.get(BACKEND_URL+'/aggregates/polarity-keywords')
    .then((res)=>{
      // console.log(res['data'])
      // setReviewData(res['data']['review_data'])
    })
    .catch(()=>{
      console.error('Failed to fetch review data')
    })


  }, [])

  return (
    <main className='flex flex-col items-center gap-8'>
      <Navbar></Navbar>
      <div className='mt-16 py-16 px-8'>
        <div className='flex gap-8'>
          <img src={g2Logo} />
          <div className='w-full bg-blue-50 p-8 flex flex-col gap-2'>
            <h1 className='text-2xl barlow-medium'>G2 Marketing Solutions</h1>
            <Rating
              size={30}
              initialValue={4.5}
              allowFraction={true}
              fillColor='#ff492c'
              SVGclassName={'inline-block'}
              readonly
            ></Rating>
            <p>G2 is the world's largest and most trusted software marketplace. Over 90 million people research, compare, and vet software and services on G2.com annually, based on authentic user reviews. G2 Marketing Solutions enable software and service businesses to build brand presence, drive awareness, and proactively engage with in-market buyers to drive revenue and pipeline.</p>
          </div>
        </div>
      </div>

      {regionwiseData && 
      <div className='w-full flex flex-col items-center scale-[0.9]'>
        <h1 className='barlow-medium text-2xl'>Performance of this product throughout the world</h1>
        <WorldMap
          color='red'
          size="xxl"
          data={regionwiseData}
        ></WorldMap>
      </div>
      }

      <h1 className='barlow-medium text-2xl'>Metrics</h1>
      {secondaryMetrics && 
      <div className='w-[80%] grid grid-cols-3 place-items-center gap-16'>
          {Object.keys(secondaryMetrics).map((metric)=>{
            return (
              <MetricCard key={metric} name={secondaryMetricsMap[metric]} value={secondaryMetrics[metric]}></MetricCard>
            )
          })}
      </div>
      }

      {/* <div>
      <iframe
        src="https://www.chatbase.co/chatbot-iframe/u9WqEL33R2L_quBkBfy09"
        title="Chatbot"
        width="100%"
        className='min-h-96 w-[50vw]'
        // style="height: 100%; min-height: 700px"
        // frameborder="0"
        ></iframe>
      </div> */}
      <div className='w-full flex flex-col gap-8 items-center'>
        <h1 className='barlow-medium text-2xl'>Chat with reviews directly through Monty!</h1>
        <CustomChatBot></CustomChatBot>
      </div>

    </main>
  )
}

export default Search