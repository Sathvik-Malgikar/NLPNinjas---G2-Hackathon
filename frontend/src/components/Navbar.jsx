import React from 'react'
import g2Logo from '../assets/g2-logo.png'

const Navbar = () => {
  return (
    <nav className='w-full fixed top-0 p-4 grid grid-cols-9 place-items-center'>

        <img src={g2Logo} className='w-12 justify-self-start col-span-4'></img>
        <p className='barlow-medium hover:bg-[#e8f3f9] w-full h-full text-center pt-2'>Software</p>
        <p className='barlow-medium hover:bg-[#e8f3f9] w-full h-full text-center pt-2'>Services</p>
        <p className='barlow-medium hover:bg-[#e8f3f9] w-full h-full text-center pt-2'>G2 for Business</p>
        <p className='barlow-medium hover:bg-[#e8f3f9] w-full h-full text-center pt-2'>$ Deals</p>
        <p className='barlow-medium bg-[#5a39a2] text-white py-2 px-4 rounded-full'>Write a review</p>

    </nav>
  )
}

export default Navbar