import React, { useEffect, useState } from 'react'
import g2Logo from '../assets/g2-logo.png'
import {useNavigate, useLocation } from 'react-router-dom'

const Navbar = () => {

  const navigate = useNavigate();
  const location = useLocation()['pathname'];
  // const [navbarTransp, setNavbarTransp] = useState(true)


  useEffect(()=>{
    if (location == '/search'){
      let nav = document.getElementById('nav')
      nav.classList.add('bg-white')
    }
    else{
      let nav = document.getElementById('nav')
      nav.classList.remove('bg-white')
    }
  }, [location])

  return (
    <nav id='nav' className='w-full fixed top-0 px-4 grid grid-cols-10 place-items-center z-50'>

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