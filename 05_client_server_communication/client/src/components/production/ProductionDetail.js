import  {useParams, useNavigate } from 'react-router-dom'
import {useEffect, useState} from 'react'
import styled from 'styled-components'
import { useOutletContext } from 'react-router-dom'

function ProductionDetail() {
  const [production, setProduction] = useState()
  const [error, setError] = useState(null)
  const { handleEdit, deleteProduction } = useOutletContext()

  //Student Challenge: GET One 
  const {productionId} = useParams()
  const navigate = useNavigate()

  useEffect(()=>{
    fetch(`/productions/${productionId}`)
    .then(resp => {
      if (resp.status === 200) {
        return resp.json().then(setProduction)
      }
      return resp.json().then(errorObj => setError(errorObj.message))
    })
    .catch(setError)
  }, [productionId]) //! deps

  const handleDelete = (production) => {
    fetch(`/productions/${productionId}`, {
      method: "DELETE"
    })
    .then(res => {
      if (res.status === 204) {
        deleteProduction(production)
        navigate("/")
      } else {
        return res.json().then(errorObj => {debugger})
      }
    })
    .catch(setError)
  }

  
  if(error) return <h2>{error}</h2>
  if(!production) return <h2>Loading</h2>

  const {id, title, genre, image,description, crew_members} = production 
  return (
      <CardDetail id={id}>
        <h1>{title}</h1>
          <div className='wrapper'>
            <div>
              <h3>Genre:</h3>
              <p>{genre}</p>
              <h3>Description:</h3>
              <p>{description}</p>
              <h2>Cast Members</h2>
              <ul>
            {crew_members && crew_members.map(cast => <li key={cast.id}>{`${cast.role} : ${cast.name}`}</li>)}
              </ul>
            </div>
            <img src={image} alt={title}/>
          </div>
      <button onClick={()=> handleEdit(production)} >Edit Production</button>
      <button onClick={()=> handleDelete(production)} >Delete Production</button>

      </CardDetail>
    )
  }
  
  export default ProductionDetail
  const CardDetail = styled.li`
    display:flex;
    flex-direction:column;
    justify-content:start;
    font-family:Arial, sans-serif;
    margin:5px;
    h1{
      font-size:60px;
      border-bottom:solid;
      border-color:#42ddf5;
    }
    .wrapper{
      display:flex;
      div{
        margin:10px;
      }
    }
    img{
      width: 300px;
    }
    button{
      background-color:#42ddf5;
      color: white;
      height:40px;
      font-family:Arial;
      font-size:30px;
      margin-top:10px;
    }
  `