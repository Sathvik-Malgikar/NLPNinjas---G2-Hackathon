import { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar'
import {useNavigate} from 'react-router-dom'

function App() {

  const navigate = useNavigate();

  const inputHandler = (event)=>{
    if (event.keyCode == 13){
      navigate('/search')
    }
  }

  return (
    <main className='flex flex-col gap-8 justify-center items-center min-h-screen'>

      <Navbar></Navbar>

      <h1 className=' barlow-bold text-7xl text-[#252530]'>Where you go for software.</h1>
      <h2 className='text-xl'>Find the right software and services based on <span className='barlow-semibold text-[#ff492c]'>2,569,000+</span> real reviews.</h2>
      <input placeholder='Enter the product name, software category, service name...'
            onKeyDown={inputHandler}
            type="text" 
            className='placeholder-black w-[70%] rounded-full barlow-regular text-lg py-4 px-8 border-none outline-none'/>
    </main>
  )
}

export default App
