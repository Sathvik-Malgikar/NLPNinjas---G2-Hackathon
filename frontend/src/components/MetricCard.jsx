import React from 'react'

const MetricCard = ({name, value}) => {
  value = Math.round(value)
  return (
    <div className='flex flex-col gap-2 items-center'>
      <h1 className='barlow-semibold text-lg'>{name}</h1>
      <input type="range" value={value} readOnly max={10}/>
      <h1 className='text-lg'>{value}/10</h1>
    </div>
  )
}

export default MetricCard