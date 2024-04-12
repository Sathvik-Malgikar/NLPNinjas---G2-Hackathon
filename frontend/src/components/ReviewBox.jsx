import React from 'react'
import { Rating } from 'react-simple-star-rating'

const ReviewBox = ({review}) => {

  const {title, star_rating, user_name} = review['attributes']
  console.log(review)

  return (
    <div className='flex flex-col w-full m-4 p-8 border-black border-[1px] rounded-lg'>
      <h1 className='text-base barlow-medium'>{user_name}</h1>
      <h1 className='text-2xl barlow-medium'>{title}</h1>
      <Rating
        size={20}
        initialValue={star_rating}
        allowFraction={true}
        fillColor='#ff492c'
        SVGclassName={'inline-block'}
        readonly
      ></Rating>
    </div>
  )
}

export default ReviewBox