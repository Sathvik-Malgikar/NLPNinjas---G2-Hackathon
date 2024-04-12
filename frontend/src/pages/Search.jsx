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
import ReviewBox from '../components/ReviewBox'

import 'react-chatbot-kit/build/main.css'
import Tag from '../components/Tag';

const Search = () => {

  const [regionwiseData, setRegionwiseData] = useState([]);
  const [secondaryMetrics, setSecondaryMetrics] = useState(null);
  const [reviewData, setReviewData] = useState([]);
  const [reviewMapper, setReviewMapper] = useState({});
  const [keywordInferences, setKeywordInferences] = useState({});
  const [filteredReviews, setFilteredReviews] = useState([]);

  
  const aspects = ["Value for money","Performance","Scalability","Interoperability","Accessibility","Reliablity","Availability","Security","Compliance","Easy setup"]

  const [filterArray, setFilterArray] = useState([true, true, true, true, true, true, true, true, true, true])

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

  function buildBooleanParams(paramList) {
      let params = '';
      paramList.forEach((value, index) => {
          const paramName = `f${index + 1}`;
          if (value){
            const paramValue = value ? 'true' : 'false';
            params += `${paramName}=${aspects[index]}&`;
          }
      });
      // Remove the trailing '&' if there are parameters
      if (params.length > 0) {
          params = params.slice(0, -1);
      }
      return params;
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
      // console.log(res['data']['review_data'])
      
      // setReviewData(res['data']['review_data'])
    })
    .catch(()=>{
      console.error('Failed to fetch review data')
    })


    // polarity keywords
    axios.get(BACKEND_URL+'/aggregates/polarity-keywords')
    .then((res)=>{

      let temp = {};
      // console.log(res['data'])
      res['data']['review_data'].map((review)=>{
        temp[review['id']] = review;
      })
      setReviewMapper(temp);

      // console.log(res['data'])
      setReviewData(res['data']['review_data'])
    })
    // .catch(()=>{
    //   console.error('Failed to fetch review data')
    // })

    // keyword inferences
    axios.get(BACKEND_URL+'/keyword-inferences')
    .then((res)=>{
      setKeywordInferences(res['data'])
    })
    .catch(()=>{
      console.error('Failed to fetch keyword inferences')
    })


  }, [])

  useEffect(()=>{
    // console.log(BACKEND_URL+'?'+buildBooleanParams(filterArray))
    // console.log(filterArray)

    let invCount = 0;
    filterArray.map((e)=>{
      if (e){
        invCount += 1;
      }
    })

    if (invCount == 10){
      setFilteredReviews([]);
      return;
    }

    axios.get(BACKEND_URL+'/filter-reviews?'+buildBooleanParams(filterArray))
    .then((res)=>{
      let temp = []

      Object.keys(res['data']).map((e)=>{
        if (e !== "null"){
          res['data'][e].map(review=>{
            axios.get(BACKEND_URL+`/review-by-id?id=${review['id']}`)
            .then((resp)=>{
              setFilteredReviews((prev)=>{return [...prev, resp['data']['data']]})
              // temp.push(resp['data']['data'])
              // console.log(resp['data']['data'])
            })
          })
        }
      })
      setFilteredReviews(temp)

      // console.log(filteredReviews)
    })

  }, [filterArray])

  return (
    <main className='flex flex-col items-center gap-y-24'>
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

      <div className='w-full flex flex-col gap-16 items-center'>
        <h1 className='barlow-medium text-3xl'>What customers are looking for</h1>
        <div className='w-2/3 grid grid-cols-3 place-items-start gap-8 grid-flow-row'>
          {Object.keys(keywordInferences).length != 0
            && keywordInferences['customer_expectations'].map((e, i)=>{
            return (
              <h1 key={i}
                  className='text-2xl'
              >{e}</h1>
              )
          })}
        </div>
      </div>

      <div className='w-full grid grid-cols-2 gap-12'>

        <h1 className='text-3xl barlow-medium col-span-2 text-center'>How this product scores</h1>

        <div className='flex flex-col gap-8 items-center'>
          <h1 className='barlow-medium text-3xl'>Pros</h1>
          <div className='flex flex-col gap-4 items-center'>
            {Object.keys(keywordInferences).length != 0
              && keywordInferences['pros'].map((e, i)=>{
              return (
                <h1 key={i}
                    className='text-2xl'
                >{e}</h1>
                )
            })}
          </div>
        </div>

        <div className='flex flex-col gap-8 items-center'>
          <h1 className='barlow-medium text-3xl'>Cons</h1>
          <div className='flex flex-col gap-4 items-center'>
            {Object.keys(keywordInferences).length != 0
              && keywordInferences['cons'].map((e, i)=>{
              return (
                <h1 key={i}
                    className='text-2xl'
                >{e}</h1>
                )
            })}
          </div>
        </div>


      </div>

      {regionwiseData && 
      <div className='w-full flex flex-col items-center'>
        <h1 className='barlow-medium text-2xl'>Performance of this product throughout the world</h1>
        <WorldMap
          color='red'
          size={1000}
          data={regionwiseData}
        ></WorldMap>
      </div>
      }

      <div className='w-full flex flex-col items-center gap-y-8'>
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
      </div>

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
      <div className='w-2/3 flex flex-col gap-8 items-center'>
        <h1 className='barlow-medium text-2xl'>Chat with reviews directly through Monty!</h1>
        <div className='w-full grid grid-cols-2 place-items-center gap-4'>

          <h1 className='barlow-medium text-lg' >In house chatbot built with Gemma-2B</h1>
          <h1 className='barlow-medium text-lg' >Chatbot built using Chatbase</h1>

          <div className='h-full min-h-[500px] border-solid border-[1px] border-black p-4'>
            <CustomChatBot className='border-solid border-[1px] border-black'></CustomChatBot>
          </div>
          <iframe
            src="https://www.chatbase.co/chatbot-iframe/D_-F0yu8p0EwL9XIUNmgB"
            title="Chatbot"
            width="100%"
            // style="height: 100%; min-height: 700px"
            className='h-full min-h-[500px] border-solid border-[1px] border-black p-4'
            frameborder="0"
            ></iframe>

        </div>
      </div>


      <div className='w-full flex flex-col gap-8 items-center'>
        <h1 className='barlow-medium text-2xl'>Search Reviews</h1>
        <div className='w-2/3 flex flex-wrap gap-4 justify-center'>
          {aspects.map((e, i)=>{
            return (<Tag key={i} name={e} index={i} filterArray={filterArray} setFilterArray={setFilterArray} />)
          })}
        </div>
      

        <div className='w-[90%]'>
          {filteredReviews && filteredReviews.map((review, i)=>{
            return (
              <ReviewBox review={review} key={i} ></ReviewBox>
            )
          })}
        </div>

      </div>

    </main>
  )
}

export default Search