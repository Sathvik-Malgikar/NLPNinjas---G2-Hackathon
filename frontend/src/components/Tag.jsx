import React, { useState } from 'react'

const Tag = ({name, index, filterArray, setFilterArray}) => {

  const handleClick = ()=>{
    let ele = document.getElementById(name)
    ele.classList.toggle('bg-[#ff492c]')

    let p = document.getElementById(name+'p')
    p.classList.toggle('text-white')

    let temp = [];
    for (let i=0; i<filterArray.length; i++){
      if (i == index){
        if (filterArray[i])
          temp.push(false)
        else
          temp.push(true)
      }
      else{
        temp.push(filterArray[i])
      }
    }
    setFilterArray(temp)

  }

  return (
    <div
      id={name}
      className='px-8 py-2 border-solid border-[1px] rounded-full border-black cursor-pointer'
      onClick={handleClick}
    >
      <p id={name+'p'} className='select-none'>{name}</p>
    </div>
  )
}

export default Tag