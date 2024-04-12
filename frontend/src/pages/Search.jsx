import React, { useEffect, useState } from 'react'
import Navbar from '../components/Navbar'
import g2Logo from '../assets/g2-logo.png'
import { Rating } from 'react-simple-star-rating'
import WorldMap from "react-svg-worldmap";
import {countryCodes, secondaryMetricsMap} from '../components/Mappers'
import axios from 'axios'
import { BACKEND_URL } from '../App';
import MetricCard from '../components/MetricCard';

const Search = () => {

  const [regionwiseData, setRegionwiseData] = useState([]);
  const [secondaryMetrics, setSecondaryMetrics] = useState(null);

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
      console.log(res['data'])
        setSecondaryMetrics(res['data'])
    })
    .catch(()=>{
      console.error('Failed to fetch secondary metrics')
    })

    //

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
      <div className='w-full flex flex-col items-center'>
        <h1 className='barlow-medium text-2xl'>Performance of this product throughout the world</h1>
        <WorldMap
          color='red'
          size="xl"
          data={regionwiseData}
        ></WorldMap>
      </div>
      }

      <h1 className='barlow-medium text-2xl'>Metrics</h1>
      {secondaryMetrics && 
      <div className='w-[80%] grid grid-cols-3 place-items-center gap-16'>
          {Object.keys(secondaryMetrics).map((metric)=>{
            return (
              <MetricCard name={secondaryMetricsMap[metric]} value={secondaryMetrics[metric]}></MetricCard>
            )
          })}
      </div>
      
      }

    </main>
  )
}

export default Search