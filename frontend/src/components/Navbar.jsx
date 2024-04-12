import React from 'react'
import g2Logo from '../assets/g2-logo.png'
import {useNavigate} from 'react-router-dom'

const Navbar = () => {

  const navigate = useNavigate();

  return (
    <nav className='w-full fixed top-0 px-4 grid grid-cols-10 place-items-center'>

        <img 
          src={g2Logo} 
          className='w-12 justify-self-start col-span-4 m-2 cursor-pointer'
          onClick={()=>{navigate('/')}}
          ></img>

        <div className='hover:bg-[#e8f3f9] w-full h-full flex justify-center items-center cursor-pointer'>
          <p className='barlow-medium'>Software</p>
        </div>

        <div className='hover:bg-[#e8f3f9] w-full h-full flex justify-center items-center cursor-pointer'>
          <p className='barlow-medium'>Services</p>
        </div>

        <div className='hover:bg-[#e8f3f9] w-full h-full flex justify-center items-center cursor-pointer'>
          <p className='barlow-medium'>G2 for Business</p>
        </div>

        <div className='hover:bg-[#e8f3f9] w-full h-full flex justify-center items-center cursor-pointer'>
          <p className='barlow-medium'>$ Deals</p>
        </div>

        <p className='barlow-semibold bg-[#5a39a2] col-span-2 text-white py-2 px-8 rounded-full cursor-pointer hover:bg-[#3b2569]'>Write a Review</p>

    </nav>
  )
}

export default Navbar